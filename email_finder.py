import re
import requests
import requests.exceptions
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import warnings
from bs4 import GuessedAtParserWarning, MarkupResemblesLocatorWarning


def main():
    warnings.filterwarnings('ignore', category=GuessedAtParserWarning)
    warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)

    url = "https://www.scrapethissite.com/"

    emails = get_emails(url)

    print(f"Number of emails = {len(emails)}")
    for email in emails:
        print(print(email))


def get_emails(url):
    urls = []
    emails = set()
    base_url = url
    if base_url not in urls:
        urls.append(base_url)

    for next_url in urls:
        try:
            response = requests.get(next_url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue
        print(f"Crawling URL =================== {next_url} ")
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all("a")
        new_emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))

        if len(new_emails) > 0:
            print(f"Found: {new_emails}")
            emails.update(new_emails)

        for link in links:
            if link.get("href"):

                if ((next_url not in link.get("href")) & ("http" not in link.get("href")) & ("www" not in link.get("href"))):
                    page_url = base_url.strip(
                        "/") + "/" + link.get("href").strip("/")
                    if page_url not in urls:
                        urls.append(page_url)
                        print(f"Adding page # {len(urls)}: {page_url}")

                elif (next_url in link.get("href")):
                    page_url = link.get("href")
                    if page_url not in urls:
                        urls.append(page_url)
                        print(f"Adding: {page_url} Number Added: {len(urls)}")
    print(f"Total number of URLs:   {len(urls)}")
    print(f"Total number of Emails: {len(emails)}")

    return emails


if __name__ == "__main__":
    main()
