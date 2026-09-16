from connect_db import get_db

def count_trending_news():
    with get_db as cur:
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
    with get_db as cur:
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

def insert_data(
        url: str,
        title: str,
        model_name : str,
        category: str = "nasional",
        status: str = "scheduled",
        created_by:str = "AI"
):
    with get_db as cur:
        cur.execute(
            """--sql
            INSERT INTO debate_topics (title, category, model_name, status, created_by)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (title, category, model_name, status, created_by)
        )

        cur.execute(
            """--sql
            UPDATE trending_news
            SET is_done = TRUE
            WHERE url = %s
            """,
            (url,)
        )