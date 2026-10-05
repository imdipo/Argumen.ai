from repositories.topic_repo import scheduled_count
from api.jobs.llm_create_topic import topic_maker

"""
simple DAG
                         ---- if not available ---- take hottest news from db ---- run create topic by LLM based on the news ---- RAG
                        |
check debate schedule ---
                        |
                         ---- if avail ---- RAG

humm i think thtats how it works

"""

def take_news():
    topic_maker()


def check_debate_sched():
    total_sched = scheduled_count()

    return total_sched



######################






