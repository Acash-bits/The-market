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
        self.countries_name = [] # Empty list to store countries name in it
        self.countries_link = [] # Empty list to store countires limk in it

    def get_countries_name(self):
        """Getting the Country name and link of that country"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page=browser.new_page()
                # Set the default timeout to 90 seconds
                page.set_default_timeout(90000)

                # Navigate to target URL with timeout of 60 seconds
                page.goto(self.countries_page, wait_until="domcontentloaded")

                # Wait for elements to appear
                target_countries = self.countries_tag["Country_name"]
                page.wait_for_selector(target_countries)

                # Extract data: Find all elements of Country Name
                countries = page.locator(target_countries).all_text_contents()
                # Storing the names of the countries inself attribute
                # Removing the whitespaces in country name
                self.countries_name = [c.strip() for c in countries]

                # Print the countries name
                print("Countries available to choose from")
                for country_count, country in enumerate(countries, start=1):
                    print(f"{country_count}. {country}")
        
        except Exception as e:
            print(f"\nERROR OCCURED WHILE SCRAPING COUNTRY NAME")
            print(f"ERROR: {e}")


    def get_countries_link(self):
        """Getting the countries link"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Navigate to target URL with timeout of 60 seconds
                page.goto(self.countries_page, wait_until="domcontentloaded", timeout=90000)

                # Wait for elements to appear
                target_links = self.countries_tag["Country_name"]
                page.wait_for_selector(target_links)

                # Read the href attribute from every matching <a>
                # Extract the date
                links = page.locator(target_links).evaluate_all(
                    "els => els.map(e => e.getAttribute('href'))"
                )

                # Print the Countries Link
                print("\nCountries Link to choose from")
                for links_count, link in enumerate(links, start=1):
                    full_url = urljoin(self.countries_page, link)
                    print(f"{links_count}. {full_url}")
                    self.countries_link.append(full_url)
        except Exception as e:
            print("ERROR OCCURED WHILE SCRAPING COUNTRY LINK")
            print(f"ERROR: {e}")


if __name__ == "__main__":
    country_scraper = CountryLinks()
    country_scraper.get_countries_name()
    country_scraper.get_countries_link()