from flask import Blueprint, request, jsonify, render_template

from app.services.notion import fetch_category_map, add_expense_page
from app.services.gpt import parse_text
from app.services.transformer import build_notion_payload
from app.utils.validators import validate_categories
from app.utils.operation_logger import log_operation



expense_controller = Blueprint("expense_controller", __name__)

# ---------- VIEW CONTROLLER ----------

@expense_controller.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# ---------- API CONTROLLER ----------

@expense_controller.route("/expense/text", methods=["POST"])
def add_expense_from_text():
    data = request.get_json()
    text = data.get("text") if data else None

    parsed = None
    payload = None
    notion_summary = None

    try:
        if not text:
            raise ValueError("Input text is required")

        category_map = fetch_category_map()
        parsed = parse_text(text, list(category_map.keys()))
        validate_categories(parsed, category_map)

        payload = build_notion_payload(parsed, category_map)
        result = add_expense_page(payload)

        notion_summary = {
            "status": "success",
            "page_id": result["id"],
            "notion_url": result.get("url")
        }

        log_operation(
            input_text=text,
            parsed_json=parsed,
            notion_payload=payload,
            notion_result=notion_summary,
            success=True
        )

        return jsonify({
            "status": "success",
            "page_id": result["id"],
            "parsed": parsed
        })

    except Exception as e:
        log_operation(
            input_text=text or "",
            parsed_json=parsed,
            notion_payload=payload,
            notion_result=None,
            success=False,
            error_message=str(e)
        )

        return jsonify({"error": str(e)}), 400
