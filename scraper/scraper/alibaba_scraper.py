import csv
from bs4 import BeautifulSoup
from utils import fetch_url

BASE_URL = "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText="

CATEGORIES = {
    "industrial machinery": "industrial+machinery",
    "electronics": "electronics",
    "textiles": "textiles"
}

def parse_product_list(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    products = soup.select("div.J-offer-wrapper")  # Adjust selectors to actual Alibaba site
    for product in products:
        name_tag = product.select_one("h2.title a")
        location_tag = product.select_one("div.supplier-location span")
        if not name_tag or not location_tag:
            continue
        name = name_tag.get_text(strip=True)
        link = name_tag['href']
        location = location_tag.get_text(strip=True)
        results.append({
            "name": name,
            "url": link,
            "location": location
        })
    return results

def scrape_category(category):
    print(f"Scraping Alibaba category: {category}")
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
    with open("../data/alibaba_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_results)
    print(f"Saved Alibaba data: {len(all_results)} records")

if __name__ == "__main__":
    main()
