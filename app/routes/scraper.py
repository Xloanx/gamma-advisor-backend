from fastapi import APIRouter
from app.models.url_model import URL 
from app.services.web_scraper import scrape_and_store  # Import the scraper function
import logging


router = APIRouter()

@router.post("/scrape")
def trigger_scraping():
    """Manually trigger scraping."""
    logging.info("Manual scraping initiated...")
    return scrape_and_store()










