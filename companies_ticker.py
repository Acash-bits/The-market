from playwright.sync_api import sync_playwright
import yfinance as yf
import mysql.connector
from dotenv import load_dotenv
import os

# Load envrionment variables
load_dotenv()

# Website Link
WEBSITE_LINK = "https://companiesmarketcap.com/"
COMPANY_TAGS = {
    "Name" : "company-name",
    "Ticker" : "company-code",
    "Company_count" : 'span[class="companies-count font-weight-bold"]'
}

class CompanyData:
    """Getting data of listed companies and storing them in sql based on link"""

    def __init__(self, link, tags):
        """Initialize the link and tags attributes """
        self.link = link
        self.tags = tags
        self.tickers = [] # Empty list to store ticker symbols in it

    def get_total_pages(self):
        """Getting total number of pages from the website"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to target url
                page.goto(self.link)
                
                # Wait for elements to appear
                target = self.tags['Company_count']
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

    def get_all_page_links(self):
        """Scraping every page of the website till final page"""
        try:
            # List to store page links
            page_links = []
            
            # Getting the number of total pages
            total_pages = self.get_total_pages()
            
            for page_number in range(1,total_pages+1):
                page_link = f"{self.link}page/{page_number}/"
                print(page_link)
                page_links.append(page_link)
            return page_links
        except Exception as e:
            print(f"Error scraping page number {page_number}: {e}")

    def get_company_data(self, page_link):
        """Scraping the company name & ticker from the website"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Navigate to the target URL
                page.goto(page_link)
                # Scraping company name and ticker
                selector = f"div.{self.tags['Name']}, div.{self.tags['Ticker']}"
                # Wait for elements to appear
                page.wait_for_selector(selector)

                # Extract data: Find all elements of company_name and ticker class
                names = page.locator(f'div.{self.tags["Name"]}').all_text_contents()
                self.tickers = page.locator(f'div.{self.tags["Ticker"]}').all_text_contents()
                
                # Print the results # Uncomment to print details getting scrapped
                # for i, (name, ticker) in enumerate(zip(names, tickers), 1):
                #     print(f"\n{i}.Company Name : {name.strip()}")
                #     print(f"\tCompany Ticker: {ticker.strip().upper()}")
                
                browser.close()
                return self.tickers
        except Exception as e:
            print(f"ERROR OCCURRED DURING SCRAPING: {e} ")

    def get_financial_details(self,tickers):
        """Getting the financial details of the company using yfinance"""
        try:
            # Creating list to store data
            company_data = {}
            
            
            for i, ticker in enumerate(tickers,1):
                dat = yf.Ticker(f"{ticker}")
                # Getting the details of the company
                company_name = dat.info.get('longName', 'N/A')
                revenue = dat.info.get('totalRevenue', 'N/A')
                market_cap = dat.info.get('marketCap', 'N/A')
                hq_city = dat.info.get('city', "N/A")
                hq_state = dat.info.get('state', 'N/A')
                hq_country = dat.info.get('country', 'N/A')
                sector = dat.info.get('sector', 'N/A')
                industry = dat.info.get('industry', 'N/A')

                # Printing the details of the ticker
                print(f"\n{i}. Gathering data for company {ticker}")
                print(f"Company Name: {company_name}")
                print(f"Revenue: {revenue}")
                print(f"Market Cap: {market_cap}")
                print(f"Company HQ City: {hq_city}")
                print(f"Company HQ State: {hq_state}")
                print(f"Company HQ Country: {hq_country}")
                print(f"Company Sector: {sector}")
                print(f"Company Industry: {industry}")
                
                # Appending data in a dictionary
                company_data[ticker] = [
                    company_name, revenue, market_cap, hq_city, hq_state,
                    hq_country, sector, industry
                    ]
                print("Data stored in dictionary 'Company_data'")
            
            return company_data
        except Exception as e:
            print(f"Yahoo Finance Error: {e}")

    def store_data_in_sql():
        """Storing the information received through yfinance"""
        try:
            # Establish the connection with data using environment variables
            db_config = mysql.connector.connect(
                host = os.getenv('MYSQL_HOST'),
                database = os.getenv('MYSQL_DATABASE'),
                user = os.getenv("MYSQL_USER"),
                password = int(os.getenv("MYSQL_PASS"))
            )

            if db_config.is_connected():
                print("Sucessfully connected to the database")

            # Creating a cursor object to execute SQL
            cursor = db_config.cursor()
        
        except mysql.connector.Error as err:
            print(f"Error with database: {err}")
    
    def main(self):
        """Running the full method to scrape and get data from yfinance"""
        try:
            # Total pages for the link
            total_pages = self.get_total_pages()
            print(f"Total Pages = {total_pages}")

            # Creating link for every page 
            pages_links = self.get_all_page_links()

            # List to store tickers
            company_tickers = []

            # Scraping the ticker from every page
            for page_link in pages_links:
                tickers = self.get_company_data(page_link)
                company_tickers.extend(tickers)
                
                # Printing data to check 
                print(company_tickers)
                print(tickers)
            
                # Getting financial data for the ticker from yfinance
                self.get_financial_details(tickers)
            
        except Exception as e:
            print(f"Error while running final code: {e}")

scrape_website = CompanyData(WEBSITE_LINK, COMPANY_TAGS)
scrape_website.main()