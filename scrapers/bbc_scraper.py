import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0 Safari/537.36"
    )
}

def scrape_bbc(limit=None):
    """Scrape BBC News front page titles & links.
    Returns list of dicts: {source,title,link,published}
    """
    url = "https://www.bbc.com/news"
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    seen = set()
    articles = []

    # BBC often renders headings within <a><h2|h3>...</h2></a>
    for node in soup.select("a h2, a h3"):
        title = node.get_text(strip=True)
        a = node.find_parent("a")
        if not a:
            continue
        link = a.get("href") or ""
        if not title or not link:
            continue
        if not link.startswith("http"):
            link = "https://www.bbc.com" + link
        if "/news" not in link:
            continue
        if link in seen:
            continue

        seen.add(link)
        articles.append({
            "source": "BBC",
            "title": title,
            "link": link,
            "published": None
        })
        if limit and len(articles) >= limit:
            break

    return articles
