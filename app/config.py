import os
from dotenv import load_dotenv

load_dotenv()

NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EXPENSES_DB_ID = os.getenv("EXPENSES_DB_ID")
CATEGORIES_DB_ID = os.getenv("CATEGORIES_DB_ID")

NOTION_API_VERSION = "2022-06-28"
