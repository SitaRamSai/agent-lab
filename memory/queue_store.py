import json
from pathlib import Path

QUEUE_FILE = Path("pending_queue.json")

def save_queue(queue: list):
    QUEUE_FILE.write_text(json.dumps(queue, indent=2))

def load_queue() -> list:
    if not QUEUE_FILE.exists():
        return []
    return json.loads(QUEUE_FILE.read_text())
