from repositories.topic_repo import count_trending_news, flag_fail
from dotenv import load_dotenv

load_dotenv()

import trafilatura

def read_article():
    count_undone_trending_news = count_trending_news()

    if count_undone_trending_news:
        link_article = count_undone_trending_news[0]

    if not link_article:
        return None

    downloaded = trafilatura.fetch_url(link_article)

    if not downloaded:
        print(f"failed to download the content. maybe the url no more valid. ion know")
        flag_fail(link_article)
        return None

    content_article = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_images=False,
        include_tables=False,
        include_links = False,
        no_fallback= False
    )

    return content_article[:1000], link_article

