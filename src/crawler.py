import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://quotes.toscrape.com"
DELAY = 6
REQUEST_TIMEOUT = 10

def crawl():
    urls = [BASE_URL]
    visited = set()
    pages = {}

    while urls:
        url = urls.pop(0)
        if url in visited:
            continue

        try:
            print(f"Crawling: {url}")
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            pages[url] = soup.get_text(separator=" ")

            visited.add(url)

            next_page = soup.find("li", class_="next")
            if next_page:
                next_link = next_page.find("a")["href"]
                full_url = BASE_URL + next_link
                if full_url not in visited:
                    urls.append(full_url)

            time.sleep(DELAY)

        except requests.exceptions.RequestException as error:
            print(f"Error fetching {url}: {error}")

    return pages