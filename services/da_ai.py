from core.groq_client import groq
from rag_pre_debate import search_supporting_article
from repositories.topic_repo import take_topic_research

client = groq()

history_debate = []

class BotDebate:
    def __init__(self, id_topic, model_name, topic, position):
        self.model_name = model_name
        self.topic = topic
        self.position = position
        self.id_topic = id_topic
        self.list_article = []
        self.has_searched = False
        self.is_talk_first = False

    def take_support_article(self):
        if self.has_searched == False:
            id_debate_topic, position = take_topic_research()
            articles = search_supporting_article(self.position, self.topic)
            for article in articles:
                self.list_article.append({
                        "title": article["title"],
                        "content": article["content"]})
            self.has_searched = True

    def prepare_first_argument(self):
        self.search_support_article()
        article_text = "\n\n".join([f"- {i['title']}: {i["content"]}" for i in self.list_article])
        special_prompt = f"""Manfaatkan rujukan berikut bila relevan:
                {article_text}"""
        prompt = f"""
                Kamu adalah ahli debat, sebagai seorang debater handal yang sedang membahas topic berupa '{self.topic}' dengan posisimu adalah {self.position.upper()}.
                Tugasmu menyampaikan argumen persuasif dan logis dalam bahasa Indonesia.""" + special_prompt

        respone = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.6
        )
        completion = respone.choices[0].message.content.strip()
        history_debate.append({
            "role": self.position,
            "content": completion
        })



    def battle(self):
        if len(history_debate) == 0 and self.is_talk_first == True:
            self.prepare_first_argument()

        next_prompt = f"""

            """



def start_argue()







