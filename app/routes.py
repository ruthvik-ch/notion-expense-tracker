from flask import Blueprint, request, jsonify
from app.services.notion import fetch_category_map, add_expense_page
from app.services.gpt import parse_text
from app.services.transformer import build_notion_payload
from app.utils.validators import validate_categories

api = Blueprint("api", __name__)

@api.route("/expense/text", methods=["POST"])
def add_expense_from_text():
    text = request.json.get("text")
    if not text:
        return {"error": "text is required"}, 400

    category_map = fetch_category_map()
    parsed = parse_text(text, list(category_map.keys()))
    validate_categories(parsed, category_map)

    payload = build_notion_payload(parsed, category_map)
    result = add_expense_page(payload)

    return jsonify({
        "status": "success",
        "page_id": result["id"],
        "parsed": parsed
    })
