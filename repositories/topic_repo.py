from connect_db import get_db

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
        raise ValueError(f"Harus login dulu")

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

def create_topic(
        title: str,
        created_by:str,
        model_name : str,
        category: str,
        bot_a: str,
        bot_b: str,
        status: str = "scheduled"

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