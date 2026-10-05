from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from api.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/roblox/login")
def roblox_login():
    # URL resmi Roblox untuk minta izin login
    roblox_oauth_url = (
        "https://apis.roblox.com/oauth/v1/authorize"
        "?client_id=08122600960",
        "&response_type=code"
        "&redirect_uri=http://localhost:8000/auth/roblox/callback" # Musti sama persis!
        "&scope=openid profile"
    )
    # Lempar user ke Roblox
    return RedirectResponse(url=roblox_oauth_url)

@router.get("/roblox/callback")
def roblox_callback(roblox_code:str = Query(..., alias="code")):
    try:
        user_profile = AuthService.process_roblox_callback(roblox_code)
        print(user_profile)
        return {"status": "success", "user": user_profile}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))