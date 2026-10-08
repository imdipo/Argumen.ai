from repositories.topic_repo import scheduled_count
from api.services.llm_create_topic import topic_maker
from api.services.scrap_top_news import save_scrapped_news

def main():
    total_sched = scheduled_count()

    if total_sched == 0:
        save_scrapped_news()

    topic_maker()