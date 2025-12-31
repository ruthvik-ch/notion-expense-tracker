from app.config import EXPENSES_DB_ID

def build_notion_payload(data: dict, category_map: dict):
    relations = [{"id": category_map[c]} for c in data["categories"]]

    return {
        "parent": {"database_id": EXPENSES_DB_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": data["name"]}}]},
            "Date": {"date": {"start": data["date"]}},
            "Amount": {"number": data["amount"]},
            "Categories": {"relation": relations}
        }
    }
