from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import pandas as pd
from textblob import TextBlob
from scrapers.bbc_scraper import scrape_bbc
from scrapers.cnn_scraper import scrape_cnn
from scrapers.aljazeera_scraper import scrape_aljazeera

# ---------------------------
# Helper functions
# ---------------------------
def categorize(title):
    title_lower = title.lower()
    if any(word in title_lower for word in ["tech", "ai", "software", "app", "gadget"]):
        return "Technology"
    elif any(word in title_lower for word in ["politics", "election", "government", "law"]):
        return "Politics"
    elif any(word in title_lower for word in ["war", "conflict", "military"]):
        return "World"
    elif any(word in title_lower for word in ["sport", "football", "cricket", "game"]):
        return "Sports"
    else:
        return "General"

def detect_sentiment(title):
    score = TextBlob(title).sentiment.polarity
    if score > 0.1:
        return "Positive"
    elif score < -0.1:
        return "Negative"
    else:
        return "Neutral"

# ---------------------------
# Scrape + Save to DB + CSV
# ---------------------------
def scrape_and_store():
    print("🔄 Scraping fresh news...")

    articles = []
    articles.extend(scrape_bbc())
    articles.extend(scrape_cnn())
    articles.extend(scrape_aljazeera())

    for article in articles:
        article["category"] = categorize(article["title"])
        article["sentiment"] = detect_sentiment(article["title"])

    df = pd.DataFrame(articles)
    if not df.empty:
        df.to_csv("news_output.csv", index=False)
        print(f"✅ Saved {len(df)} articles to news_output.csv")

    # MongoDB store
    client = MongoClient("mongodb://localhost:27017/")
    db = client["news_db"]
    collection = db["articles"]

    # Clear old entries (optional)
    collection.delete_many({})

    if articles:
        collection.insert_many(articles)
        print(f"✅ Inserted {len(articles)} articles into MongoDB (news_db.articles)")

# ---------------------------
# Flask App
# ---------------------------
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["news_db"]
collection = db["articles"]

@app.route("/")
def index():
    sources = sorted(collection.distinct("source"))
    sentiments = sorted(collection.distinct("sentiment"))
    categories = sorted(collection.distinct("category"))

    source = request.args.get("source")
    sentiment = request.args.get("sentiment")
    category = request.args.get("category")

    query = {}
    if source:
        query["source"] = source
    if sentiment:
        query["sentiment"] = sentiment
    if category:
        query["category"] = category

    articles = list(collection.find(query).limit(50))

    return render_template(
        "index.html",
        articles=articles,
        sources=sources,
        sentiments=sentiments,
        categories=categories,
        selected_source=source,
        selected_sentiment=sentiment,
        selected_category=category
    )

@app.route("/refresh")
def refresh():
    scrape_and_store()
    return redirect(url_for("index"))

if __name__ == "__main__":
    scrape_and_store()
    app.run(debug=True)
