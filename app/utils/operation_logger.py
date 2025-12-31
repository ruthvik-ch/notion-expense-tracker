import json
import os
from datetime import datetime
from threading import Lock

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "expense_operations.log")

_counter_lock = Lock()
_operation_counter = 0


def _ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def _next_operation_id() -> int:
    global _operation_counter
    with _counter_lock:
        _operation_counter += 1
        return _operation_counter


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
        f.write("=" * 60 + "\n")
        f.write(f"Operation #{operation_id} — Expense Submission\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("=" * 60 + "\n\n")

        f.write("Input (raw text):\n")
        f.write(f"{input_text}\n\n")

        f.write("Parsed Output (intent extracted by AI):\n")
        f.write(json.dumps(parsed_json, indent=2) if parsed_json else "N/A")
        f.write("\n\n")

        f.write("Notion Payload (API-ready format):\n")
        f.write(json.dumps(notion_payload, indent=2) if notion_payload else "N/A")
        f.write("\n\n")

        f.write("Notion Response (summary):\n")
        if notion_result:
            f.write(json.dumps(notion_result, indent=2))
        else:
            f.write("N/A")
        f.write("\n\n")

        if success:
            f.write("Outcome: Operation completed successfully\n")
        else:
            f.write("Outcome: Operation failed\n")
            if error_message:
                f.write(f"Error: {error_message}\n")

        f.write("=" * 60 + "\n")
