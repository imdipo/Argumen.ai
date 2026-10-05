from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import SECRET_KEY, ALGORITHM
import jwt

security = HTTPBearer()
 # they said it for HTTPBearer to read the header "Authorization: Bearer <token>" automatically

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
       payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

       user_id = payload.get("sub")
       if user_id is None:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Token tidak memiliki identitas user"
           )

       return {"user_id": int(user_id)}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Silakan login ulang"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau telah dimanipulasi"
        )