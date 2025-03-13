from app.services.web_scraper import fetch_page_content

# Test scraping a real webpage
url = "https://www.ft.com/"
content = fetch_page_content(url)

if content:
    print(f"Extracted content from {url}:\n{content[:500]}...")  # Show first 500 chars
else:
    print(f"Failed to scrape {url}")
