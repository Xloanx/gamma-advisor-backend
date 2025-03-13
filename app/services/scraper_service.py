'''
Automatically scrapes all inputed URLs 6-hourly via API (/scrape/ endpoint)
'''

import requests
from bs4 import BeautifulSoup
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.database import get_all_urls, store_scraped_data
from app.db.vector_store import store_data_faiss

logging.basicConfig(level=logging.INFO)

def fetch_page_content(url):
    """Fetch and extract text content from a webpage."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        logging.info(f"Fetching content from {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text_content = "\n".join([tag.get_text() for tag in soup.find_all(["p", "div", "span"])])
        if text_content.strip():
            logging.info(f"Successfully extracted content from {url}")
            return text_content
        else:
            logging.warning(f"No relevant content found on {url}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def scrape_all():
    """Automatically scrape all stored URLs, save to MongoDB, and store embeddings in FAISS."""
    urls = get_all_urls()
    if not urls:
        logging.warning("No URLs found for scraping.")
        return

    logging.info("Starting scheduled scraping process...")
    for url in urls:
        content = fetch_page_content(url)
        if content:
            # Store in MongoDB first
            store_scraped_data(url, content)
            logging.info(f"Stored content in Database for {url}")

    # After saving in MongoDB, store in FAISS
    store_data_faiss()  # Process all newly stored data
    logging.info("All scraped content has been processed into FAISS.")

    logging.info("Scheduled scraping process completed.")

# Scheduler to run scraping every 6 hours
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_all, "interval", hours=6)
scheduler.start()

logging.info("Scraper Service Initialized...")
