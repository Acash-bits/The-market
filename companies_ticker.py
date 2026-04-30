from playwright.sync_api import sync_playwright
import yfinance as yf

def get_total_pages(link):
    """Getting total number of pages from the website"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navigate to target url
            page.goto(link)
            
            # Wait for elements to appear
            target = 'span[class="companies-count font-weight-bold"]'
            page.wait_for_selector(target)
            
            # Extract data: Find the count of companies
            company_count = page.locator(target).all_text_contents()
            # Replacing comma from company count number
            count = int(company_count[0].replace(",",""))
            # Counting total pages adding 1 to round off 
            total_pages = int(count/100 +1)
            return total_pages
    except Exception as e:
        print(f"Error Code: {e}")

def get_all_page_links(link,total_pages):
    """Scraping every page of the website till final page"""
    try:
        for page_number in range(1,total_pages+1):
            page_link = f"{link}{page_number}/"
            print(page_link)
    except Exception as e:
        print(f"Error scraping page number {page_number}: {e}")

def get_company_data(link,**tag):
    """Scraping the company name & ticker from the website"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to the target URL
            page.goto(link)

            # Wait for elements to appear
            selector = f"div.{tag['Name']}, div.{tag['Ticker']}"
            page.wait_for_selector(selector)

            # Extract data: Find all elements of company_name and ticker class
            names = page.locator(f'div.{tag["Name"]}').all_text_contents()
            tickers = page.locator(f'div.{tag["Ticker"]}').all_text_contents()
            
            # Print the results # Uncomment to print details getting scrapped
            # for i, (name, ticker) in enumerate(zip(names, tickers), 1):
            #     print(f"\n{i}.Company Name : {name.strip()}")
            #     print(f"\tCompany Ticker: {ticker.strip().upper()}")
            
            browser.close()
            return names, tickers
    except Exception as e:
        print(f"ERROR OCCURRED: {Exception} ")

def get_financial_details(tickers):
    """Getting the financial details of the company using yfinance"""
    try:
        for i, ticker in enumerate(tickers,1):
            dat = yf.Ticker(f"{ticker}")
            # Printing the details of the ticker
            print(f"\n{i}. Gathering data for company {ticker}")
            print(f"Company Name: {dat.info.get('longName', 'N/A')}")
            print(f"Revenue: {dat.info.get('totalRevenue', 'N/A')}")
            print(f"Market Cap: {dat.info.get('marketCap', 'N/A')}")
            print(f"Company HQ City: {dat.info.get('city', 'N/A')}")
            print(f"Company HQ State: {dat.info.get('state', 'N/A')}")
            print(f"Company HQ Country: {dat.info.get('country', 'N/A')}")
    except Exception as e:
        print(f"Yahoo Finance Error: {Exception}")

# Website Link
website_link = "https://companiesmarketcap.com/"
company_tags = {
    "Name" : "company-name",
    "Ticker" : "company-code"
}

pages = get_total_pages(website_link)
print(pages)

page_link = (get_all_page_links(website_link,pages))
print(page_link)