import json
import uuid
from datetime import datetime
from confluent_kafka import Producer

from repositories.topic_repo import scheduled_count

from kafka.producer import send_event

def trigger_check_schedule():
    total = scheduled_count()

    today_str = datetime.now().strftime("%Y-%m-%d")
    created_at = datetime.now().isoformat()
    topic_name = "schedule.checked"
    tag = today_str.replace("-", "")

    if total != 0:
        session_id = f"session-rag-topic-{today_str}-{uuid.uuid4().hex[:6]}",
        event_type = "TRIGGER_RAG_INITIATED",
        status =  "AVAILABLE",
        log_msg = f"Schedule found, triggering pipeline with Session ID: {session_id}"

    else:
        session_id = f"session-create-topic-{today_str}-{uuid.uuid4().hex[:6]}",
        event_type = "SCHEDULE_EMPTY",
        status =  "NOT AVAILABLE",
        log_msg = f"Schedule empty, triggering news-to-topic creator with Session ID: {session_id}"

    payload = {
        "session_id": session_id,
        "event_type": event_type,
        "trace_id" : f"cron_batch_{tag}",
        "created_at": created_at,
        "status": status,
        "metadata": {
            "requested_by": "DAILY_CRONJOB_SCHEDULER",
        }}

    print(log_msg)


    send_event(
        topic=topic_name,
        key=session_id,
        value=json.dumps(payload).encode('utf-8'),
    )






