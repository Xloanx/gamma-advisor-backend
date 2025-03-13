from app.services.scraper_service import scrape_all
import logging

logging.basicConfig(level=logging.INFO)

print("Starting scheduled scraping test...")
scrape_all()
print("✅ Scraping completed successfully.")
