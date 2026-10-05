import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM

def create_user_token(user_id:int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)

    return token