from api.repositories.connect_db import get_db

BOT_ID = 0
BOT_USERNAME = "BOT_FOR_TOPIC"
BOT_AVATAR = "avatar_url"


def insert_bot():
    with get_db() as cur:
        cur.execute(
            """--sql
            INSERT INTO users ("roblox_user_id", "roblox_username", "avatar_url")
            VALUES (%s, %s, %s)
            ON CONFLICT("roblox_user_id") DO NOTHING;
            """,
            (BOT_ID, BOT_USERNAME, BOT_AVATAR)
        )

if __name__ == "__main__":
    insert_bot()