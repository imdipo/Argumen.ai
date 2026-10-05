import re

from langdetect import DetectorFactory, detect, LangDetectException

DetectorFactory.seed = 0
ALLOWED_LANGUAGES = {"id", "en"}

BANNED_WORDS = {"kontol"} # I bet si abdan, would use this one particular word

def validate_language(topic):
    """
    cuman boleh indo atau inggris. target gweh cuman 2 bahasa ini sih (ntar modelnya pake Mixtral, padahal dari prancis wkwk yodahlah ya)
    """
    try:
        detected_language = detect(topic)
        if detected_language not in ALLOWED_LANGUAGES:
            raise ValueError(f"Please only use indonesia/english")

        return True

    except LangDetectException:
        raise ValueError("if u see this error, means we cant validate what the hell u tryin to say. please use formal words")


def validate_topic(topic):

    validate_language(topic)

    if len(topic.strip()) < 10:
        raise ValueError("The title too short son")
    if len(topic.strip()) > 200:
        raise ValueError("the title too long son, i aint got no money")

    if re.search(r"([a-zA-Z])\1{2,}", topic):
        raise ValueError("please make sure the title formal, no spam/gubberish/cute words please")

    unique_words = set(topic.lower().split())
    if unique_words.intersection(BANNED_WORDS):
        raise ValueError("haha got u dan")

    return True

