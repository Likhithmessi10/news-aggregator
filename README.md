# 📰 News Aggregator with Flask + MongoDB  

A simple **News Aggregator** that:  
- Scrapes latest articles from **BBC, CNN, and Al Jazeera**  
- Categorizes and runs **sentiment analysis** on each article  
- Stores results in **MongoDB** and **CSV**  
- Provides a **Flask web frontend** with filters and a **Refresh button** to fetch fresh news anytime  

---

## 📦 Features
- Scraping from BBC (HTML), CNN & Al Jazeera (RSS)  
- NLP-based **Sentiment Analysis** (Positive / Neutral / Negative)  
- Basic **Category Detection** (Technology, Politics, Sports, etc.)  
- Stores data in:
  - MongoDB (`news_db.articles`)  
  - `news_output.csv`  
- Flask frontend:
  - Dropdown filters for Source, Category, Sentiment  
  - 🔄 **Refresh News** button  

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/news-aggregator.git
cd news-aggregator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

### 3. Install & Start MongoDB
- Install **MongoDB Community Server**  
- Make sure MongoDB is running:  
  ```bash
  mongod
  ```

### 4. Run the App
```bash
python app.py
```

- First, it will **scrape fresh news** and save to MongoDB + CSV  
- Then launch Flask server at 👉 `http://127.0.0.1:5000`  

---

## 🗄️ Checking Data in MongoDB

Open Mongo shell:
```bash
mongosh
use news_db
db.articles.countDocuments()
db.articles.find().pretty()
```

### Example Queries:
- Only BBC articles:
  ```js
  db.articles.find({ source: "BBC" }).pretty()
  ```
- Positive sentiment only:
  ```js
  db.articles.find({ sentiment: "Positive" }).pretty()
  ```
- By category (Technology):
  ```js
  db.articles.find({ category: "Technology" }).pretty()
  ```

---

## 🎨 Frontend

- Access 👉 `http://127.0.0.1:5000`  
- Filter by:
  - Source (BBC, CNN, Al Jazeera)  
  - Sentiment (Positive, Neutral, Negative)  
  - Category (Politics, Tech, Sports, etc.)  
- Click **🔄 Refresh News** to scrape fresh articles anytime.  

---

## 📂 Project Structure
```
news-aggregator/
│── scrapers/
│   ├── bbc_scraper.py
│   ├── cnn_scraper.py
│   ├── aljazeera_scraper.py
│── templates/
│   └── index.html
│── app.py
│── requirements.txt
│── README.md
│── news_output.csv   (auto-generated)
```

---

## 🚀 Future Improvements
- Add more sources (NYTimes, The Verge, TechCrunch)  
- Advanced ML for category classification  
- Deploy on cloud (Heroku, Render, or Railway)  
- User accounts & saved news  
