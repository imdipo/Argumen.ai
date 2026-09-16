import feedparser
import sys
from pathlib import Path

from psycopg2.extras import execute_values

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from repositories.connect_db import get_db

def get_newest_article():
    url = "https://www.cnnindonesia.com/nasional/rss"
    feed = feedparser.parse(url)

    newests_news_list = []

    for news in feed.entries[:5]:
        newests_news_list.append((
            news.title,
            news.link,
            "cnn",
            news.published
        ))
    print(newests_news_list)

    return newests_news_list

def save_news():
    da_list = get_newest_article()
    print(len(da_list))
    with get_db() as cur:
        execute_values(
            cur,
            """--sql
            INSERT INTO trending_news (title, url, source, published_at)
            VALUES %s
            ON CONFLICT (url) DO NOTHING;
            """,
            da_list
        )


if __name__ == "__main__":
    save_news()