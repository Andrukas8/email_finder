import re
import requests
import requests.exceptions
from urllib.parse import urlsplit
from bs4 import BeautifulSoup


def get_links(url):
    urls = []

    base_url = url
    if base_url not in urls:
        urls.append(base_url)

    for next_url in urls:
        response = requests.get(next_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all("a")

        for link in links:
            if link.get("href"):

                if ((next_url not in link.get("href")) & ("http" not in link.get("href")) & ("www" not in link.get("href"))):
                    page_url = base_url.strip(
                        "/") + "/" + link.get("href").strip("/")
                    if page_url not in urls:
                        urls.append(page_url)
                        print(f"Adding: {page_url} Number Added: {len(urls)}")
    print(f"Total number of URLs: {len(urls)}")
    return urls


def get_emails(urls):
    emails = set()
    print("Searching for emails started...")
    while len(urls):
        url = urls.pop()
        print(f"Crawling URL {url}")
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        print(f"Found: {new_emails}")
        emails.update(new_emails)
    return emails


url = "https://www.scrapethissite.com/"
emails = get_emails(get_links(url))

print(f"Number of emails = {len(emails)}")
for email in emails:
    print(print(email))
