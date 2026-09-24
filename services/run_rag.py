from repositories.topic_repo import check_debate_schedule
from llm_create_topic import topic_maker
from rag_pre_debate import search_supporting_article


def check_schedule():
    debate_shedule= check_debate_schedule()

    if not debate_shedule:
        topic_maker()
        return

    id, title, _, _ = debate_shedule
    position = ["PRO", "KONTRA"]

    for posisi in position:
        search_supporting_article(id_topic_article=id, topic_article=title, position=posisi)










