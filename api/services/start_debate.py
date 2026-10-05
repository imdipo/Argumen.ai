from api.core.groq_client import groq
from api.repositories.topic_repo import check_debate_schedule
from api.services.rag_pre_debate import search_supporting_article
from api.services.da_ai import BotDebate

import random

client = groq()

def random_start(bot_pro, bot_kontra):
    talk_first = random.choice([bot_pro, bot_kontra])

    if talk_first == bot_pro:
        bot_pro.is_talk_first = True
        bot_kontra.is_talk_first = False
    else:
        bot_pro.is_talk_first = False
        bot_kontra.is_talk_first = True

    return talk_first.position




def prepare_debate():
    id, title, bot_a, bot_b = check_debate_schedule()

    bot_pro = BotDebate(id_topic=id, topic=title, model_name=bot_a, position="PRO")
    bot_kontra = BotDebate(id_topic=id, topic=title, model_name=bot_b, position="KONTRA")

    who_talk_first = random_start(bot_pro=bot_pro, bot_kontra=bot_kontra)

    print(f"debate begin with argument from {who_talk_first} side")













def bot_a(bot_a_name, role, message):
    client = groq()
    message = client.chat.completions.create(
        model= bot_a_name,
        messages=[
            {"role": "system",
             "content": (
                f"tugas mu adalah {role} terhadap pernyataan beserta argumen yang dibawakan oleh lawan bicaramu"
            ),},
            {"role": "user", "content": message}
        ],
        temperature=0.6,
        max_tokens= 60
    )




