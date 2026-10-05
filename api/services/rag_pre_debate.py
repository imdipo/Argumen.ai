import trafilatura
from duckduckgo_search import DDGS
from api.core.groq_client import groq
import json

from api.repositories.topic_repo import insert_topic_research, insert_topic_research, take_title_and_title_id

client = groq

def create_query(position, topic_article):
    prompt = f"""
    Topik debat: "{topic_article}"
    Posisi kamu: {position.upper()}

    Buat maksimal 3 kata kunci pencarian Google (bahasa Indonesia) yang paling efektif
    untuk mencari data, berita, atau statistik pendukung posisimu.

    Balas HANYA dalam format JSON array of string tanpa teks pengantar apapun, contoh:
    ["query 1", "query 2", "query 3"]
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user", "content":prompt}],
        temperature=0.2
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        queries = json.loads(raw_output)
        if isinstance(queries, list):
            return queries[:3]

    except Exception:
        pass

    return [
        f"fakta mengenai topic {topic_article}",
        f"{position} mengenai {topic_article}"
    ]

# i change it to this flow, because i want the rag process done before the match begin


def search_supporting_article(id_topic_article:str, topic_article:str, position:str):
    queries = create_query(position=position, topic_article=topic_article)

    # id_title = take_title_id(topic_article)

    seen_urls = set()

    batching_article=[]

    with DDGS() as ddgs:
        for qry in queries:
            print(f"mencari {qry}")
            try:
                query_results = list(ddgs.text(qry, region="id-id", max_results=1))

                for urls in query_results:
                    url = urls.get("href")

                    if not url or url in seen_urls:
                        continue

                    seen_urls.add(url)

                    downloaded_article = trafilatura.fetch_url(url)
                    if downloaded_article:
                        text_content = trafilatura.extract(
                            downloaded_article,
                            include_images= False,
                            include_comments= False,
                            include_tables= False
                        )

                        if text_content and len(text_content) > 150:
                            batching_article.append( {
                                "id_debate_topic": id_topic_article,
                                "position": position,
                                "search_query_used":qry,
                                "research_urls": url,
                                "research_title": urls.get("title"),
                                "research_content": text_content[:1200]
                            })

            except Exception as e:
                print(f"Error while searching about '{qry}':{e}")

    insert_topic_research(batching_data=batching_article)
