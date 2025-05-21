import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/90.0.4430.212 Safari/537.36"
}

def fetch_url(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        time.sleep(2)  # polite delay to avoid rate-limiting
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
