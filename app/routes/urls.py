from fastapi import APIRouter
from app.models.url_model import URL 
from app.db.database import add_url, remove_url, get_all_urls
import logging


router = APIRouter()


@router.get("/urls")
def get_urls():
    """Get the list of stored URLs."""
    return {"urls": get_all_urls()}

@router.post("/urls/add")
def add_new_url(url: str):
    """Add a new URL to scrape."""
    if add_url(url):
        logging.info(f"Added URL: {url}")
        return {"message": f"Added {url}"}
    return {"message": "URL already exists"}

@router.delete("/urls/remove")
def delete_url(url: str):
    """Remove a URL from the scraping list."""
    remove_url(url)
    logging.info(f"Removed URL: {url}")
    return {"message": f"Removed {url}"}










