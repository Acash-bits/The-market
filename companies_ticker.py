from playwright.sync_api import sync_playwright
import yfinance as yf

def scrape_company_data(link,**tag):
    """Scraping the company name & ticker from the website"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the target URL
        page.goto(link)

        # Wait for elements to appear
        selector = f"div.{tag['Name']}, div.{tag['Ticker']}"
        page.wait_for_selector(selector)

        # Extract data: Find all elements of company_name class
        names = page.locator(f"div.{tag["Name"]}").all_text_contents()
        tickers = page.locator(f"div.{tag["Ticker"]}").all_text_contents()

        # Print the results
        for i, (name, ticker) in enumerate(zip(names, tickers), 1):
            print(f"\n{i}.Company Name : {name.strip()}")
            print(f"\tCompany Ticker: {ticker.strip().upper()}")
        
        browser.close()

# Website Link
website_link = "https://companiesmarketcap.com/"
company_tags = {
    "Name" : "company-name",
    "Ticker" : "company-code"
}

scrape_company_data(website_link, **company_tags)