from api.repositories.connect_db import get_db
from psycopg2.extras import execute_values


def check_user(user_id):
    with get_db() as cur:
        cur.execute(
            """--sql
            SELECT id
            FROM users
            WHERE roblox_user_id = %s;
            """,
            (user_id,)
        )

        id_user = cur.fetchone()

    if not id_user:
        raise ValueError("Harus login dulu")

    return id_user[0]

def count_trending_news():
    with get_db() as cur:
        cur.execute(
            """--sql
            SELECT url FROM trending_news
            WHERE is_done = FALSE
            ORDER BY published_at ASC
            LIMIT 1;
            """
        )
        row = cur.fetchone()

    return row[0]

def flag_fail(link):
    with get_db() as cur:
        cur.execute(
            """--sql
            UPDATE trending_news
            SET is_done = TRUE
            WHERE url = %s;
            """,
            (link,)
        )

def scheduled_count():
    with get_db() as cur:
        cur.execute(
            """--sql
            SELECT COUNT(*) status
            FROM debate_topics
            WHERE status = 'scheduled'
            """
        )
        total_antrian = cur.fetchone()


    return total_antrian[0]

def insert_trending_news(list_article:list):
    with get_db() as cur:
        execute_values(
            cur,
            """--sql
            INSERT INTO trending_news (title, url, source, published_at)
            VALUES %s
            ON CONFLICT (url) DO NOTHING;
            """,
            list_article
        )

# a for pro, b for contra
# shi why didnt i simply use bot_pro n bot_kontra

def create_topic(
        title: str,
        created_by:str,
        category: str,
        bot_a: str,
        bot_b: str,
        status: str = "scheduled",
        model_name : str="None"

):
    with get_db() as cur:
        cur.execute(
        """--sql
        INSERT INTO debate_topics (title, category, bot_a, bot_b, model_name, created_by, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (title, category, bot_a, bot_b, model_name, status, created_by)
        )



def create_topic_llm(
        url: str,
        title: str,
        model_name : str,
        bot_a: str,
        bot_b: str,
):
    with get_db() as cur:
        create_topic(
            title = title,
            category= "nasional",
            model_name=model_name,
            bot_a=bot_a,
            bot_b=bot_b,
            created_by=1,
            status = "scheduled"
        )

        cur.execute(
            """--sql
            UPDATE trending_news
            SET is_done = TRUE
            WHERE url = %s
            """,
            (url,)
        )

        return

def take_title_and_title_id(title:str):
    with get_db() as cur:
        cur.execute(
            """--sql
                SELECT id, title
                FROM debate_topics
                WHERE title: %s
            """,
            (title)
        )

    return cur.fetchone[0]

def insert_topic_research(batching_data:list):
    with get_db() as cur:
        execute_values(
            cur,
            """--sql
            INSERT INTO debate_research_topic (topic_title_id, position, search_query_used, source_title, source_url, raw_content)
            VALUES %s
            """,
            batching_data
        )

def take_topic_research(
        id_debate_topic:int,
        position:str,
):
    with get_db() as cur:
        cur.execute("""--sql
        SELECT source_title, raw_content
        FROM debate_research_topic
        WHERE topic_title_id = %s AND position = %s
        """,
        (id_debate_topic, position)
        )

        topic_research = cur.fetchall()

        if not topic_research:
            return "tidak ditemukan artikel pendukung. semangat!"

        context_text = "\n\n".join([f"Judul: {title}\nIsi: {content}" for title, content in topic_research])

        return context_text


def check_debate_schedule():
    with get_db() as cur:
        cur.execute(
        """--sql
        SELECT id, title, bot_a, bot_b
        FROM debate_topics
        WHERE status = 'scheduled'
        ORDER BY created_at ASC
        LIMIT 1
        """
        )

        new_schedule = cur.fetchone()

        if not new_schedule:
            return None

        id, title, bot_a, bot_b = new_schedule


    return id, title, bot_a, bot_b



        # cur.execute(
        # """--sql
        # UPDATE INTO debate_topics
        # SET status = 'done'
        # WHERE id = %s
        # """
        # (id,)
        # )



