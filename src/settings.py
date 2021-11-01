import os

from dotenv import load_dotenv

load_dotenv()

NOTION_BASE_URL = "https://api.notion.com/"

NOTION_TOKEN = os.getenv("NOTION_TOKEN")

LINKS_DB_ID = os.getenv("LINKS_DB_ID")

PAGE_ID = os.getenv("PAGE_ID")

PROPERTY_ID = os.getenv("PROPERTY_ID")
