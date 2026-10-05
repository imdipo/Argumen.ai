from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.repositories.topic_repo import create_topic

from api.services.auth_security import get_current_user

router = APIRouter(prefix="/debate", tags=["Debates"])

class CreateTopicRequest(BaseModel):
    title: str
    category: str
    bot_pro: str
    bot_kontra: str

@router.post("/topics")
def create_topics(
    body_topic: CreateTopicRequest,
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]

    create_topic(title=body_topic.title, created_by=user_id, category=body_topic.category, bot_a=body_topic.bot_pro, bot_b=body_topic.bot_kontra)

    return {
        "status": "success",
        "message": "Topic created by user",
        "topic": body_topic.title
    }


