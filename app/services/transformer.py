from app.config import (
    EXPENSES_DB_ID,
    REXPENSES_DB_ID
)

def build_notion_payload(data: dict, category_map: dict, db_context="public"):
    """
    Build Notion payload with appropriate database ID based on context.
    Automatically adds the "AI Added" category to all expenses.
    
    Args:
        data: Expense data dict
        category_map: Category to ID mapping
        db_context: "public" or "private" to determine which database to use
    
    Returns:
        Notion API payload with correct database ID and AI Added category
    """
    expenses_db_id = REXPENSES_DB_ID if db_context == "private" else EXPENSES_DB_ID
    
    # Build relations from parsed categories
    relations = [{"id": category_map[c]} for c in data["categories"]]
    
    # Always add "AI Added" category if it exists in the map
    if "AI Added" in category_map:
        relations.append({"id": category_map["AI Added"]})

    return {
        "parent": {"database_id": expenses_db_id},
        "properties": {
            "Name": {"title": [{"text": {"content": data["name"]}}]},
            "Date": {"date": {"start": data["date"]}},
            "Amount": {"number": data["amount"]},
            "Categories": {"relation": relations}
        }
    }
