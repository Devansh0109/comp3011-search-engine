import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"

def crawl():
    urls = [BASE_URL]
    visited = set()
    pages = {}

    while urls:
        url = urls.pop(0)
        if url in visited:
            continue

        print(f"Crawling: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text()
        pages[url] = text

        visited.add(url)

        next_page = soup.find("li", class_="next")
        if next_page:
            next_link = next_page.find("a")["href"]
            urls.append(BASE_URL + next_link)

    return pages