from flask import Blueprint, request, jsonify, render_template, session

from app.services.notion import fetch_category_map, add_expense_page
from app.services.gpt import parse_text
from app.services.transformer import build_notion_payload
from app.utils.validators import validate_categories
from app.utils.operation_logger import log_operation



expense_controller = Blueprint("expense_controller", __name__)

# Helper function to get database context
def get_db_context():
    """
    Returns appropriate database configuration based on login status.
    If logged in, uses R-prefixed vars (private database).
    Otherwise uses regular vars (public database).
    """
    logged_in = session.get("logged_in", False)
    return "private" if logged_in else "public"

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
    db_context = get_db_context()

    try:
        if not text:
            raise ValueError("Input text is required")

        category_map = fetch_category_map(db_context)
        parsed = parse_text(text, list(category_map.keys()))
        validate_categories(parsed, category_map)

        payload = build_notion_payload(parsed, category_map, db_context)
        result = add_expense_page(payload, db_context)

        notion_summary = {
            "status": "success",
            "page_id": result["id"],
            "notion_url": result.get("url"),
            "database": "private" if db_context == "private" else "public"
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
            "parsed": parsed,
            "database": "private" if db_context == "private" else "public"
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
