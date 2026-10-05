from fastapi import FastAPI
from api.routers.auth import router as auth_router
from api.routers.topic_debate import router as debate_router

app = FastAPI()

# Daftarkan router ke server utama
app.include_router(auth_router)
app.include_router(debate_router)