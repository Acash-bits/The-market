# Storing counties link to let the user choose from
from playwright.sync_api import sync_playwright
import time

class CountryLinks:
    """Getting links of countries available on the website"""

    def __init__(self):
        """Initialize the link and tag attributes"""
        # Main link of the website to pull countires link 
        self.countries_page = "https://companiesmarketcap.com/all-countries/"
        # Predefined tags to scrape from
        self.countries_tags = {
            "Country_name" : "td[data-sort] a",
            "Country_link" : "href"
        }
        self.countries_name = [] # Empty list to store countries name in it
        self.countries_link = [] # Empty list to store countires limk in it

    def get_countries_name(self):
        """Getting the Country name and link of that country"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page=browser.new_page()

                # Navigate to target URL with timeout of 60 seconds
                page.goto(self.countries_page, timeout=60000)

                # Wait for elements to appear
                target_countries = self.countries_tags["Country_name"]
                page.wait_for_selector(target_countries)

                # Extract data: Find all elements of Country Name
                countries = page.locator(target_countries).all_text_contents()

                # Print the countries name
                for country in countries:
                    print(country)
                    # Adding the countries in the countries_name attribute
                    self.countries_name.append(country)
        
        except Exception as e:
            print(f"\nERROR OCCURED DURING SCRAPING COUNTRY NAME AND LINK")
            print(f"ERROR: {e}")


    def get_countries_link(self):
        """Getting the countries link"""

if __name__ == "__main__":
    country_scraper = CountryLinks()
    country_scraper.get_countries_name()