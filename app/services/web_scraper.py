'''
Manually scrapes via API (/scrape/ endpoint)
'''

import requests
from bs4 import BeautifulSoup
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.database import get_all_urls, store_scraped_data

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

def scrape_and_store():
    """Scrape all stored URLs and save extracted content in MongoDB."""
    urls = get_all_urls()
    logging.info("Starting scraping process...")

    for url in urls:
        content = fetch_page_content(url)
        if content:
            if store_scraped_data(url, content):  # Store only if new
                logging.info(f"Stored content from {url}")
                return (f"Stored content from {url}")
            else:
                logging.info(f"Duplicate content from {url}, skipping storage.")

    logging.info("Scraping process completed.")

# Scheduler to run scraping every 6 hours
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_and_store, "interval", hours=6)
scheduler.start()

logging.info("Web Scraper Initialized...")
