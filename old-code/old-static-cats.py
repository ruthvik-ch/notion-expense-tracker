
import os
import requests
from dotenv import load_dotenv
from typing import List, Dict

# =========================
# CONFIGURATION
# =========================


load_dotenv()

NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_API_VERSION = "2022-06-28"
EXPENSES_DB_ID = "2d9a381d3e0581aea691d74b3f1a3fb2"
CATEGORIES_DB_ID = "2d9a381d3e0581c29310dc28b9f39ce1"

NOTION_PAGES_ENDPOINT = "https://api.notion.com/v1/pages"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Notion-Version": NOTION_API_VERSION,
    "Content-Type": "application/json"
}

# Category Name → Page ID Map
CATEGORY_MAP: Dict[str, str] = {
    "Fuel": "2d9a381d-3e05-8101-b2f7-fc7eff7c8955",
    "car": "2d9a381d-3e05-8115-8817-e813e58286ba",
    "Fun": "2d9a381d-3e05-8131-8200-fbdb7b0a937e",
    "Misc": "2d9a381d-3e05-8143-b432-c4a3b692bb20",
    "Investments": "2d9a381d-3e05-814e-834a-efd2c78f7608",
    "Transport": "2d9a381d-3e05-814f-82e1-ff7437cbe66d",
    "Groceries & Food": "2d9a381d-3e05-815d-9631-e26952f7aec4",
    "Shopping": "2d9a381d-3e05-81b6-875c-f52604736a59",
    "Others": "2d9a381d-3e05-81b6-b607-fa243bd2c964",
    "Insurance": "2d9a381d-3e05-81bc-923d-ce5d105d5c07",
    "car purchase": "2d9a381d-3e05-81bc-ab7c-cb47fb96c1b1",
    "Home": "2d9a381d-3e05-81e4-bec3-e0ee05704c97",
    "Bills & fees": "2d9a381d-3e05-81eb-ab47-c242e27b3995",
    "bike": "2d9a381d-3e05-81f6-919f-c9de637c0ae7",
    "Health & Wellness": "2d9a381d-3e05-81f6-b858-f18f08097be6",
    "Travel & Explore": "2d9a381d-3e05-81ff-9835-fcd9fc76cce6"
}

# =========================
# CORE LOGIC
# =========================

def resolve_category_ids(category_names: List[str]) -> List[Dict[str, str]]:
    relations = []

    for name in category_names:
        if name not in CATEGORY_MAP:
            raise ValueError(f"Unknown category: '{name}'")

        relations.append({"id": CATEGORY_MAP[name]})

    return relations


def build_notion_payload(input_data: Dict) -> Dict:
    category_relations = resolve_category_ids(input_data["categories"])

    payload = {
        "parent": {
            "database_id": EXPENSES_DB_ID
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": input_data["name"]
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": input_data["date"]
                }
            },
            "Amount": {
                "number": input_data["amount"]
            },
            "Categories": {
                "relation": category_relations
            }
        }
    }

    return payload


def add_expense(input_data: Dict) -> None:
    payload = build_notion_payload(input_data)

    response = requests.post(
        NOTION_PAGES_ENDPOINT,
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        raise RuntimeError(f"Notion API error: {response.text}")

    print("✅ Expense added successfully")
    print("Page ID:", response.json().get("id"))


# =========================
# EXAMPLE USAGE
# =========================

if __name__ == "__main__":
    expense_input = {
        "name": "Bus tkts10",
        "amount": 128760,
        "date": "2025-12-12",
        "categories": ["Transport", "Travel & Explore"]
    }

    add_expense(expense_input)
