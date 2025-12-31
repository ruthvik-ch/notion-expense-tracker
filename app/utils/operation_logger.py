import json
import os
from datetime import datetime
from threading import Lock

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "expense_operations.log")
COUNTER_FILE = os.path.join(LOG_DIR, "operation_counter.txt")

_counter_lock = Lock()


def _ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def _read_last_operation_id() -> int:
    if not os.path.exists(COUNTER_FILE):
        return 0

    try:
        with open(COUNTER_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except Exception:
        return 0

def _write_last_operation_id(op_id: int):
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        f.write(str(op_id))


def _next_operation_id() -> int:
    with _counter_lock:
        last_id = _read_last_operation_id()
        next_id = last_id + 1
        _write_last_operation_id(next_id)
        return next_id

def log_operation(
    input_text: str,
    parsed_json: dict | None,
    notion_payload: dict | None,
    notion_result: dict | None,
    success: bool,
    error_message: str | None = None
):
    _ensure_log_dir()
    operation_id = _next_operation_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n")
        f.write("=" * 72 + "\n")
        f.write(f"Operation #{operation_id} — Expense Ingestion\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("=" * 72 + "\n\n")

        f.write("Raw Input:\n")
        f.write(f"{input_text}\n\n")

        f.write("Parsed Intent (AI output):\n")
        f.write(json.dumps(parsed_json, indent=2) if parsed_json else "N/A")
        f.write("\n\n")

        f.write("Prepared Notion Payload:\n")
        f.write(json.dumps(notion_payload, indent=2) if notion_payload else "N/A")
        f.write("\n\n")

        f.write("Notion Result Summary:\n")
        f.write(json.dumps(notion_result, indent=2) if notion_result else "N/A")
        f.write("\n\n")

        if success:
            f.write("Outcome: SUCCESS — Expense recorded successfully\n")
        else:
            f.write("Outcome: FAILURE — Expense was not recorded\n")
            if error_message:
                f.write(f"Reason: {error_message}\n")

        f.write("=" * 72 + "\n")
