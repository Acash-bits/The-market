from playwright.sync_api import sync_playwright
import yfinance as yf
import mysql.connector
from dotenv import load_dotenv
import os
import time

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
        self.company_data = {} # Empty dictionary to store company related data
        self.pages_link = [] # Empty dictionary to store page links

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
            # Getting the number of total pages
            total_pages = self.get_total_pages()
            
            for page_number in range(1,total_pages+1):
                page_link = f"{self.link}page/{page_number}/"
                print(page_link)
                self.pages_link.append(page_link)
            
        except Exception as e:
            print(f"Error scraping page number {page_number}: {e}")

    def get_company_data(self, page_link):
        """Scraping the company name & ticker from the website"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Navigate to the target URL with timeout of 60 seconds
                page.goto(page_link, timeout=60000)
                # Scraping company name and ticker
                selector = f"div.{self.tags['Name']}, div.{self.tags['Ticker']}"
                # Wait for elements to appear
                page.wait_for_selector(selector)

                # Extract data: Find all elements of company_name and ticker class
                names = page.locator(f'div.{self.tags["Name"]}').all_text_contents()
                tickers = page.locator(f'div.{self.tags["Ticker"]}').all_text_contents()
                self.tickers = tickers

                # Print the results # Uncomment to print details getting scrapped
                for i, (name, ticker) in enumerate(zip(names, tickers), 1):
                    print(f"\n{i}.Company Name : {name.strip()}")
                    print(f"\tCompany Ticker: {ticker.strip().upper()}")
                
                # Making the scraping sleep for 10 seconds
                print()
                print("="*50)
                print('Holding the ticker extraction process for 10 seconds')
                print("="*50)
                time.sleep(30)
                
                browser.close()
                return tickers
        except Exception as e:
            print(f"ERROR OCCURRED DURING SCRAPING: {e} ")

    def get_financial_details(self):
        """Getting the financial details of the company using yfinance"""
        try:
            
            for i, ticker in enumerate(self.tickers,1):
                dat = yf.Ticker(f"{ticker}")
                info = dat.info
                
                if i % 10 == 0:
                    print('\nHolding the yfinance API for 10 seconds')
                    time.sleep(10)
                
                if not info or 'longName' not in info or info.get('totalRevenue') is None or info.get('marketCap') is None:
                    print(f"\n{i}. No valid data for {ticker}, skipping...")
                    continue
                else:
                    # Getting the details of the company
                    company_name = dat.info.get('longName', 'N/A')
                    revenue = int(dat.info.get('totalRevenue', 'N/A'))
                    market_cap = int(dat.info.get('marketCap', 'N/A'))
                    hq_city = dat.info.get('city', "N/A")
                    hq_state = dat.info.get('state', 'N/A')
                    hq_country = dat.info.get('country', 'N/A')
                    sector = dat.info.get('sector', 'N/A')
                    industry = dat.info.get('industry', 'N/A')

                    revenue_in_million = revenue / 10 ** 6
                    market_cap_in_billion = market_cap / 10 ** 9

                    # Printing the details of the ticker
                    print(f"\n{i}. Gathering data for company {ticker}")
                    print(f"Company Name: {company_name}")
                    print(f"Revenue: {revenue_in_million}")
                    print(f"Market Cap: {market_cap_in_billion}")
                    print(f"Company HQ City: {hq_city}")
                    print(f"Company HQ State: {hq_state}")
                    print(f"Company HQ Country: {hq_country}")
                    print(f"Company Sector: {sector}")
                    print(f"Company Industry: {industry}")
                    
                    # Appending data in a dictionary
                    self.company_data[ticker] = [
                        company_name, revenue_in_million,
                        market_cap_in_billion, hq_city,
                        hq_state,hq_country,
                        sector, industry
                        ]
                    print("Data stored in dictionary 'company_data'")
                
            return self.company_data
        except Exception as e:
            print(f"\nYahoo Finance Error: {e}")

    def store_data_in_sql(self):
        """Storing the information received through yfinance"""
        try:
            # Establish the connection with data using environment variables
            db_config = mysql.connector.connect(
                host = os.getenv('MYSQL_HOST'),
                database = os.getenv('MYSQL_DATABASE'),
                user = os.getenv("MYSQL_USER"),
                password = os.getenv("MYSQL_PASS")
            )

            if db_config.is_connected():
                print("\nSucessfully connected to the database")

            # Creating a cursor object to execute SQL
            cursor = db_config.cursor()
            sql = "Insert into usa_listed_companies" \
            "(Ticker, Company_name, Revenue, Market_Cap,HQ_City, HQ_State," \
            "HQ_Country, Sector, Industry) " \
            "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            for ticker in self.company_data.keys():
                print(f"Adding value of {ticker} in database")
                company_info = self.company_data[ticker]
                val = (
                    ticker, company_info[0], company_info[1],
                    company_info[2], company_info[3], 
                    company_info[4], company_info[5],
                    company_info[6], company_info[7]
                       )
                cursor.execute(sql,val)
                db_config.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print(f"Error with database: {err}")
    
    def main(self):
        """Running the full method to scrape and get data from yfinance"""
        try:
            print("Starting the scraper to get financial data\n")
            # Total pages for the link
            total_pages = self.get_total_pages()
            print(f"Total Pages = {total_pages}")
            # Creating page links
            self.get_all_page_links()

            # Scraping the ticker from every page
            page_counter = 1
            
            for page_link in self.pages_link:
                print(f"\nScraping page link: {page_link}")
                tickers_scraped = self.get_company_data(page_link)
                page_counter += 1

                # Getting financial data for the ticker from yfinance
                self.get_financial_details()
                self.store_data_in_sql() # Storing data in sql
                
                # Printing data to check
                print()
                print(f"="*50)
                print(f"Succesfully Scraped page number {page_counter}")
                print(f"Number of tickers scraped: {len(tickers_scraped)}")
                print("="*50)
            
            
        except Exception as e:
            print(f"Error while running final code: {e}")

scrape_website = CompanyData(WEBSITE_LINK, COMPANY_TAGS)
scrape_website.main()