#Storing the sector links for user to choose
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

class SectorLinks:
    """Getting Sector Name and Links available on the website"""

    def __init__(self):
        """Initlialize the link and tag attirbutes"""
        # Main link of sectors listing on the website
        self.all_sectors_page = "https://companiesmarketcap.com/all-categories"
        self.sectors_tag = {
            "Sector_tag" : "td[data-sort] a"
        }
        # Empty dictionary to store sectors name and links in it
        self.sectors_data = {}

    def fetch_sectors_data(self):
        """Fetching the sector name and it's page link in one rum"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # Set default timeout to 90 seconds
                page.set_default_timeout(90000)

                # Navigate to the target URL
                print("Navigating to the target URL of 'ALL SECTORS'")
                page.goto(self.all_sectors_page, wait_until="domcontentloaded")
                print("URL Navigated")

                # Wait for the elements to appear
                print("\nWaiting for the elements of Sectors to appear")
                sector_tag = self.sectors_tag["Sector_tag"]
                page.wait_for_selector(sector_tag)
                print("Elements Appeared")

                # Extracting the Country Name and Country Link
                # Read the href attribute from every matching <a>
                print("\nExtracting the Sector name and it's page link")
                print("Extracting Links")
                sectors_href = page.locator(sector_tag).evaluate_all(
                    "els => els.map(e => e.getAttribute('href'))"
                )
                print("Links Extracted")
                # Read the countries name
                print("Extracting Sectors Name")
                sectors_name = page.locator(sector_tag).all_text_contents()
                print("Sectors Name Extracted")

                # Storing the data in attributs and creating full link
                print("Storing Company name and it's full link")
                for sector, href in zip(sectors_name, sectors_href):
                    sector_full_url = urljoin(self.all_sectors_page, href)
                    self.sectors_data[sector.strip()] = [sector_full_url]
                    print(f"Link for the Sector {sector} STORED!!")
                    browser.close()
                return

        except Exception as e:
            print("ERROR OCCURED WHILE SCRAPING COUNTRY NAME AND IT'S LINK")
            print(f"ERROR CODE : {e}")
            return

    def main(self):
        """Running the full simulation to scrape sector name and link"""
        try:
            print("Scraping the Sector Name and it's link")
            # Fetching Sector Name and it's respective page link
            self.fetch_sectors_data()

        except Exception as e:
            print("ERROR OCCURED WHILE FETCHING SECTOR DATA")
            print(f"ERROR CODE: {e}")



if __name__ == "__main__":
    sector_scraper = SectorLinks()
    sector_scraper.main()
