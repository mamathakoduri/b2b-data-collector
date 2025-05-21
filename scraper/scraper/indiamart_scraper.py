import csv
from bs4 import BeautifulSoup
from utils import fetch_url

BASE_URL = "https://dir.indiamart.com/search.mp?ss="

CATEGORIES = {
    "industrial machinery": "industrial+machinery",
    "electronics": "electronics",
    "textiles": "textiles"
}

def parse_product_list(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    # Example parsing - real selectors may differ
    products = soup.select("div.comp-name > a")  # adjust selector based on site structure
    locations = soup.select("span.loc")
    for i in range(min(len(products), len(locations))):
        name = products[i].get_text(strip=True)
        link = products[i]['href']
        location = locations[i].get_text(strip=True)
        results.append({
            "name": name,
            "url": link,
            "location": location
        })
    return results

def scrape_category(category):
    print(f"Scraping IndiaMART category: {category}")
    url = BASE_URL + CATEGORIES[category]
    html = fetch_url(url)
    if html:
        return parse_product_list(html)
    return []

def main():
    all_results = []
    for category in CATEGORIES:
        data = scrape_category(category)
        for item in data:
            item["category"] = category
        all_results.extend(data)

    keys = ["name", "url", "location", "category"]
    with open("../data/indiamart_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_results)
    print(f"Saved IndiaMART data: {len(all_results)} records")

if __name__ == "__main__":
    main()
