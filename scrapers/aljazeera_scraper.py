import feedparser
from time import mktime
from datetime import datetime

def _dt_from_entry(e):
    try:
        return datetime.fromtimestamp(mktime(e.published_parsed)).isoformat()
    except Exception:
        return None

def scrape_aljazeera(limit=None):
    """Scrape Al Jazeera via RSS.
Returns list of dicts: {source,title,link,published}
"""
    FEED = "https://www.aljazeera.com/xml/rss/all.xml"
    feed = feedparser.parse(FEED)
    articles = []
    for e in feed.entries:
        title = getattr(e, "title", "").strip()
        link = getattr(e, "link", "").strip()
        articles.append({
            "source": "Al Jazeera",
            "title": title,
            "link": link,
            "published": _dt_from_entry(e),
        })
        if limit and len(articles) >= limit:
            break
    return articles
