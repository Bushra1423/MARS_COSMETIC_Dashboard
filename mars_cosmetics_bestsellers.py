import pandas as pd
import requests
from bs4 import BeautifulSoup

Product_name = []
Prices = []
Product_links = []

print("Libraries imported successfully!")

page = 1

while True:
    url = f"https://marscosmetics.in/collections/bestsellers?page={page}"
    r = requests.get(url)
    print(f"Fetching: {url} -> {r.status_code}")

    if r.status_code != 200:
        print("Stopped - Page not found.")
        break

    soup = BeautifulSoup(r.text, 'lxml')

    names = soup.find_all("a", class_="card_titl_height card__title caption")
    prices = soup.find_all("span", class_="price-item price-item--regular")
    

    # Stop when no products are found
    if not names:
        print("No more products found. Stopping...")
        break

    for i in names:
        name = i.text.strip()
        link = "https://marscosmetics.in" + i.get("href")
        Product_name.append(name)
        Product_links.append(link)

    for i in prices:
        cp = i.text.strip().replace("₹", "").replace(",", "")
        try:
            cp = float(cp)
        except:
            pass
        Prices.append(cp)


    page += 1  # move to next page

# Trim lists to same length
min_len = min(len(Product_name), len(Prices), len(Product_links))

df = pd.DataFrame({
    "Product Name": Product_name[:min_len],
    "Price (INR)": Prices[:min_len],
    "Product URL": Product_links[:min_len]
})

print(df)

df.to_csv("mars_cosmetics_bestsellers.csv", index=False, encoding="utf-8-sig")
print("✅ Data saved to mars_cosmetics_bestsellers.csv")
