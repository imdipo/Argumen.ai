from repositories.topic_repo import check_user, create_topic
from validate_topic import validate_topic

def user_topic(user,
               topic_title:str,
               category:str,
               bot_a: str,
               bot_b: str,
               model_name:str="user",
               ):
    id_user = check_user(user)

    is_valid=validate_topic(topic_title)

    if not is_valid:
        raise ValueError("son please be polite")

    create_topic(
        title = topic_title,
        created_by=id_user,
        model_name=model_name,
        category=category,
        bot_a=bot_a,
        bot_b=bot_b
        )

