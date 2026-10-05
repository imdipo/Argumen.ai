import httpx
from config import ROBLOX_CLIENT_ID, ROBLOX_CLIENT_SECRET, ROBLOX_REDIRECT_URI
from api.repositories.user_repositories import roblox_user
from api.services.create_token import create_user_token
import urllib.parse

class AuthService():
    @staticmethod
    def process_roblox_callback(code:str):
        # print(code)
        token_res = httpx.post(
            "https://apis.roblox.com/oauth/v1/token",
            data={
                "client_id": urllib.parse.quote_plus(ROBLOX_CLIENT_ID),
                "client_secret": urllib.parse.quote_plus(ROBLOX_CLIENT_SECRET),
                "grant_type": urllib.parse.quote_plus("authorization_code"),
                "code": code,
                "redirect_uri": urllib.parse.quote_plus(ROBLOX_REDIRECT_URI)
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(token_res.json())

        token_data = token_res.json()

        # print(token_data)
        refresh_token = token_data.get("refresh_token")

        access_token = token_data.get("access_token")
        if not access_token:
            raise ValueError("failed to get the access token from da roblox")

        userinfo_res = httpx.get(
            "https://apis.roblox.com/oauth/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        user_info = userinfo_res.json()
        print(f"user infooooooooooo {user_info}")

        user = roblox_user(
            roblox_id=int(user_info["sub"]),
            username=user_info["preferred_username"],
            avatar_url=user_info.get("picture"),
            refresh_token = refresh_token
        )

        session_token = create_user_token(user_id=user["id"])


        return {
            "user": user,
            "access_token": session_token,
            "token_type": "bearer"}



    # somehow ini harus diambil, cuman let save it for later