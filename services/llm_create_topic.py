import os
import time

from repositories.topic_repo import scheduled_count, insert_data
from groq import Groq
from scrap_content_news import read_article

DEFAULT_MODELS = "qwen/qwen3.8-27b"

def topic_maker(model_name:str = DEFAULT_MODELS):
    total_antrian = scheduled_count()

    while total_antrian < 3:
        client = Groq(api_key=os.getenv("GROQ"))

        # start_time = time.time() # i was wanna see on average how much time it needs, but idk dont need it

        new_content, link = read_article()

        message = client.chat.completions.create(
            model= model_name,
            messages=[
                {"role": "system",
                 "content": (
                    "Kamu adalah pembuat topik debat. Berdasarkan artikel yang diberikan, "
                    "buatlah SATU judul mosi debat yang kontroversial dan memicu kubu pro-kontra. "
                    "Hanya berikan judul mosinya saja tanpa kalimat pembuka atau tanda kutip."
                ),},
                {"role": "user", "content": new_content}
            ],
            temperature=0.6,
            max_tokens= 60
        )

        # latency_ms = int((time.time() - start_time) * 1000)
        # token_used = message.usage.total_tokens
        debate_title_content = message.choices[0].message.content.strip()

        insert_data(link, debate_title_content, model_name)

        total_antrian += 1

