import json
import asyncio
import threading
from collections import deque

import pika
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse

app = FastAPI()

RABBITMQ_HOST = "localhost"
RABBITMQ_QUEUE = "task_notifications"

# A queue to hand off new messages from RabbitMQ to FastAPI for SSE
message_queue = asyncio.Queue()

# A rotating in-memory buffer that keeps only the last N messages
# We'll store each message in the form: {"id": int, "payload": {...}}
MAX_BUFFER_SIZE = 500
message_store = deque(maxlen=MAX_BUFFER_SIZE)

# We'll keep a simple monotonic counter for assigning IDs to messages
last_id_counter = 0

def process_notification(ch, method, properties, body):
    """
    Callback for a message from RabbitMQ.
    This method runs in a separate thread (the BlockingConnection thread).
    """
    global last_id_counter

    # Parse the raw message
    raw_msg = json.loads(body)
    print(f"Received notification: {raw_msg}")

    # Acknowledge the message so RabbitMQ won't re-deliver it
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # Assign a new monotonic ID
    last_id_counter += 1
    event_id = last_id_counter

    # Wrap the original message with our ID
    wrapped_msg = {"id": event_id, "payload": raw_msg}

    # Store in the rotating buffer
    message_store.append(wrapped_msg)

    # Push into the asyncio queue so SSE endpoint can immediately stream it
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(asyncio.ensure_future, message_queue.put(wrapped_msg))


def start_consumer():
    """
    Connect to RabbitMQ and start consuming messages in a blocking manner.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=process_notification)
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


@app.on_event("startup")
def startup_event():
    """
    On application startup, spin up the RabbitMQ consumer in a separate thread.
    """
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()


@app.get("/sse")
async def sse_endpoint(request: Request):
    """
    SSE endpoint. Clients connect here and possibly send Last-Event-ID.
    The server replays any missed events still in the rotating buffer,
    then continues streaming new events as they arrive.
    """
    # 1. Check if there's a 'Last-Event-ID' header
    last_event_id = request.headers.get("Last-Event-ID")
    if last_event_id is not None:
        try:
            last_event_id = int(last_event_id)
        except ValueError:
            # If it's not an integer, ignore it
            last_event_id = None

    async def event_generator():
        # 2. REPLAY from the rotating buffer (for events still stored)
        if last_event_id is not None:
            for msg in message_store:
                if msg["id"] > last_event_id:
                    yield format_sse(msg)

        # 3. Then STREAM new messages from the queue
        while True:
            new_msg = await message_queue.get()
            yield format_sse(new_msg)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


def format_sse(msg_dict) -> str:
    """
    Convert our internal message dict into SSE format:
      id: <id>
      data: <json>
      
    Followed by two newlines.
    """
    event_id = msg_dict["id"]
    payload_json = json.dumps(msg_dict["payload"])
    return f"id: {event_id}\ndata: {payload_json}\n\n"
