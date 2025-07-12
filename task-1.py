import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime

today_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
data = []

async def scrape_100_pages():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for page_num in range(1, 101):  # 1 to 100
            url = f"https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&page={page_num}"
            print(f"🔎 Scraping page {page_num}...")
            try:
                await page.goto(url, timeout=60000)
                await page.wait_for_selector(".brh-rfq-item", timeout=20000)

                cards = await page.query_selector_all(".brh-rfq-item")
                print(f" Found {len(cards)} RFQs")

                for card in cards:
                    try:
                        # Basic selectors
                        title_el = await card.query_selector(".brh-rfq-item__subject-link")
                        title = await title_el.inner_text() if title_el else ""
                        href = await title_el.get_attribute("href") if title_el else ""
                        rfq_url = "https:" + href if href and href.startswith("//") else href
                        rfq_id = rfq_url.split("p=")[-1] if "p=" in rfq_url else ""

                        buyer_name_el = await card.query_selector(".brh-rfq-item__other-info .text")
                        buyer_name = await buyer_name_el.inner_text() if buyer_name_el else ""

                        country_el = await card.query_selector(".brh-rfq-item__country")
                        country = await country_el.inner_text() if country_el else ""

                        quantity_el = await card.query_selector(".brh-rfq-item__quantity-num")
                        quantity = await quantity_el.inner_text() if quantity_el else ""

                        quotes_el = await card.query_selector(".brh-rfq-item__quote-left span")
                        quotes_left = await quotes_el.inner_text() if quotes_el else ""

                        date_el = await card.query_selector(".brh-rfq-item__publishtime")
                        date_posted = await date_el.inner_text() if date_el else ""

                        # Tags: Email Confirmed, etc.
                        tag_elements = await card.query_selector_all(".brh-rfq-item__buyer-tag .next-tag-body")
                        tags = [await el.inner_text() for el in tag_elements]

                        email_confirmed = "Yes" if "Email Confirmed" in tags else "No"
                        complete_order = "Yes" if "Complete order via RFQ" in tags else "No"
                        experienced_buyer = "Yes" if "Experienced buyer" in tags else "No"
                        interactive_user = "Yes" if "Interactive user" in tags else "No"

                        data.append({
                            "RFQ ID": rfq_id,
                            "Title": title,
                            "Buyer Name": buyer_name,
                            "Country": country,
                            "Quantity Required": quantity,
                            "Quotes Left": quotes_left,
                            "Date Posted": date_posted,
                            "Email Confirmed": email_confirmed,
                            "Complete Order via RFQ": complete_order,
                            "Experienced Buyer": experienced_buyer,
                            "Interactive User": interactive_user,
                            "RFQ URL": rfq_url,
                            "Scraping Date": datetime.now().strftime("%Y-%m-%d")
                        })

                    except Exception as e:
                        print(f" Error parsing RFQ: {e}")

            except Exception as e:
                print(f" Page {page_num} failed: {e}")

        await browser.close()
        print(f" Done! Total RFQs scraped: {len(data)}")

# Run it
await scrape_100_pages()

# Save to CSV
columns_order = [
    "RFQ ID", "Title", "Buyer Name", "Country", "Quantity Required", "Quotes Left",
    "Date Posted", "Email Confirmed", "Complete Order via RFQ", "Experienced Buyer",
    "Interactive User", "RFQ URL", "Scraping Date"
]

df = pd.DataFrame(data)[columns_order]
filename = f"alibaba_rfq_{today_str}.csv"
df.to_csv(filename, index=False)
print(f" File saved: {filename}")
