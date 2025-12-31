import requests
from app.config import (
    NOTION_API_TOKEN,
    NOTION_API_VERSION,
    EXPENSES_DB_ID,
    CATEGORIES_DB_ID
)

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Notion-Version": NOTION_API_VERSION,
    "Content-Type": "application/json"
}

def fetch_category_map():
    url = f"https://api.notion.com/v1/databases/{CATEGORIES_DB_ID}/query"
    res = requests.post(url, headers=HEADERS, json={})
    res.raise_for_status()

    category_map = {}
    for page in res.json()["results"]:
        title = page["properties"]["Name"]["title"]
        if title:
            category_map[title[0]["plain_text"]] = page["id"]

    return category_map


def add_expense_page(payload: dict):
    url = "https://api.notion.com/v1/pages"
    res = requests.post(url, headers=HEADERS, json=payload)
    res.raise_for_status()
    return res.json()
