from core.groq_client import groq
from repositories.topic_repo import take_topic_research

client = groq()


class BotDebate:
    def __init__(self, id_topic, model_name, topic, position):
        self.model_name = model_name
        self.topic = topic
        self.position = position
        self.id_topic = id_topic
        self.list_article = []
        self.has_searched = False
        self.is_talk_first = False

        self.history_debate = []


    def take_support_article(self):

        support_article = take_topic_research(id_debate_topic=self.id_topic, position=self.position)
        self.has_searched = True

        return support_article

    def prepare_first_argument(self):
        self.article_text = self.take_support_article()

        system_prompt = f"""Kamu adalah ahli debat, sebagai seorang debater handal yang sedang membahas topic berupa '{self.topic}' dengan posisimu adalah {self.position.upper()}.
                Tugasmu menyampaikan argumen persuasif dan logis dalam bahasa Indonesia.

                Manfaatkan rujukan berikut bila relevan: {self.article_text}"""

        self.history_debate.append({
            "role": "system",
            "content": system_prompt
        })

        if self.is_talk_first == True:
            respone = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.6
        )
            completion = respone.choices[0].message.content.strip()
            self.history_debate.append({
                "role": "assistant",
                "content": completion
            })
            self.is_talk_first == False


    def talk(self, opponent_argument:None):
        if self.has_searched == False:
            self.prepare_first_argument()

        if opponent_argument:
            self.history_debate.append({
                "role": "user",
                "content": opponent_argument
            })

            respone = client.chat.completions.create(
                model=self.model_name,
                messages=self.history_debate,
                temperature=0.6
            )
            completion = respone.choices[0].message.content.strip()
            self.history_debate.append({
                "role": "assistant",
                "content": completion
            })

        return completion








