from api.repositories.connect_db import get_db

def roblox_user(roblox_id:int, username:str, avatar_url:str, refresh_token:str):
    query= """--sql
INSERT INTO users (roblox_user_id, roblox_username, avatar_url, last_seen, refresh_token)
VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s)
ON CONFLICT (roblox_user_id)
DO UPDATE SET
    roblox_username = EXCLUDED.roblox_username,
    avatar_url = EXCLUDED.avatar_url,
    last_seen = CURRENT_TIMESTAMP,
    refresh_token = EXCLUDED.refresh_token
RETURNING id, roblox_user_id, roblox_username, avatar_url, refresh_token;
"""
    with get_db() as cur:
        cur.execute(
            query, (roblox_id, username, avatar_url, refresh_token))
        data_row = cur.fetchone()
        return {"id":data_row[0], "roblox_id": data_row[1], "username":data_row[2], "avatar_url":data_row[3], "refresh_token": data_row[4]}

