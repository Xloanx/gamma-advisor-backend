from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

# Collections
urls_collection = db["urls"]
scraped_data_collection = db["scraped_data"]

# ----------------- URL MANAGEMENT ----------------- #

def add_url(url: str) -> bool:
    """
    Add a new URL to MongoDB if it doesn't already exist.
    Returns True if added, False if the URL already exists.
    """
    if not urls_collection.find_one({"url": url}):
        urls_collection.insert_one({"url": url})
        return True  # URL was successfully added
    return False  # URL already exists

def get_all_urls() -> list:
    """
    Retrieve all stored URLs.
    Returns a list of URLs.
    """
    return [doc["url"] for doc in urls_collection.find({}, {"_id": 0, "url": 1})]

def remove_url(url: str) -> bool:
    """
    Remove a URL from MongoDB.
    Returns True if deleted, False if not found.
    """
    result = urls_collection.delete_one({"url": url})
    return result.deleted_count > 0  # True if something was deleted

# ----------------- SCRAPED DATA MANAGEMENT ----------------- #

def store_scraped_data(url: str, content: str) -> bool:
    """
    Store scraped content in MongoDB.
    Avoids duplicates by checking if the URL already exists.
    Returns True if stored, False if the URL already exists.
    """
    if not scraped_data_collection.find_one({"url": url}):
        scraped_data_collection.insert_one({"url": url, "content": content})
        return True  # Successfully stored
    return False  # Data already exists

def get_all_scraped_data() -> list:
    """
    Retrieve all scraped content from MongoDB.
    Returns a list of dictionaries [{ "url": ..., "content": ... }].
    """
    return list(scraped_data_collection.find({}, {"_id": 0, "url": 1, "content": 1}))
