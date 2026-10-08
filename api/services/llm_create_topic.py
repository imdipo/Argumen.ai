import os
import time
import random

from api.core.groq_client import groq
from api.repositories.topic_repo import create_topic_llm
from groq import Groq
from api.services.scrap_content_news import read_article

DEFAULT_MODELS = "qwen/qwen3.8-27b"

models_available = ["qwen/qwen3-32b", "groq/compound-mini", "llama-3.3-70b-versatile", "qwen/qwen3.8-27b"] # would like to add another in the future

def pick_random_model():
    total_model = len(models_available)
    bot_a = models_available[random.randint(1, total_model)]
    bot_b = models_available[random.randint(1, total_model)]

    return bot_a, bot_b

def topic_maker(new_content, link, total_antrian, model_name:str = DEFAULT_MODELS):
    while total_antrian < 3:
        client = groq()
        bot_a, bot_b = pick_random_model()

        # start_time = time.time() # i was wanna see on average how much time it needs, but idk dont need it

        # new_content, link = read_article() # change the flow to usin kafka

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

        create_topic_llm(link, debate_title_content, model_name, bot_a, bot_b)

        total_antrian += 1
