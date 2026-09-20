# Storing counties link to let the user choose from
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

class CountryLinks:
    """Getting links of countries available on the website"""

    def __init__(self):
        """Initialize the link and tag attributes"""
        # Main link of the website to pull countires link 
        self.countries_page = "https://companiesmarketcap.com/all-countries/"
        # Predefined tags to scrape from
        self.countries_tag = {
            "Country_name" : "td[data-sort] a"
        }
        self.countries_data = {} # To store country name and link

    def fetch(self):
        """Fetching the country name and it's page link in one run"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # Set default timeout to 90 seconds
                page.set_default_timeout(90000)

                # Navigate to the target URL
                print("Navigating to the URL")
                page.goto(self.countries_page,wait_until="domcontentloaded")
                print("URL Navigated")

                # Wait for the elements to appear
                print("\nWaiting for the elements to appear")
                target_tag = self.countries_tag["Country_name"]
                page.wait_for_selector(target_tag)
                print("Elements Appeared")

                # Extracting the Country Name and Country Link
                # Read the href attribute from every matching <a>
                print("\nExtracting the Country name and it's page link")
                print("Extracting Links")
                hrefs = page.locator(target_tag).evaluate_all(
                    "els => els.map(e => e.getAttribute('href'))"
                )
                print("Links Extracted")
                # Read the countries name
                print("Extracting Countries Name")
                countries_name = page.locator(target_tag).all_text_contents()
                print("Companies Name Extracted")

                # Storing the data in attributs and creating full link
                print("Storing Company name and it's full link")
                for country, href in zip(countries_name, hrefs):
                    full_url = urljoin(self.countries_page, href)
                    self.countries_data[country.strip()] = [full_url]
                    # Uncomment to print the data
                    # print(f"Added {country} link ({full_url}) to dictionary")
                    print(f"Link for the Country {country} STORED!!")
                    browser.close()
                return

        except Exception as e:
            print("ERROR OCCURED WHILE SCRAPING COUNTRY NAME AND IT'S LINK")
            print(f"ERROR CODE : {e}")

    def main(self):
        """Running the full simulation to get the country name and links"""
        try:
            print("Starting the scraper\n")
            # Fetching Country name and link
            self.fetch()
        
        except Exception as e:
            print("ERROR OCCURED WHILE SCRAPING THE DATA")
            print(f"ERROR CODE: {e}")
            return

if __name__ == "__main__":
    country_scraper = CountryLinks()
    country_scraper.fetch()