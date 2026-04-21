from bs4 import BeautifulSoup
import requests

# Link from which data is extracted
def check_link(link):
    """Checking the status of link"""
    response = requests.get(link)
    return response

def scrape_website():
    """Scraping the data from the link"""
    try:
        soup = BeautifulSoup(check_link(link).text, 'html.parser')
        company_names = soup.find_all('div', class_ = 'company_name')
        ticker_items = soup.find_all('div', class_ = 'company_code')
        print(soup.prettify()[:2000])
        for company_name, ticker_item in zip(company_names, ticker_items):
            print(f"\nCompany Name: {company_name.text}")
            print(f"Ticker Name : {ticker_item.text}")
    except Exception as e:
        print(f"ERROR: {e}")

link = "https://companiesmarketcap.com/"
print(check_link(link))
scrape_website()