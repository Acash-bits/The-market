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
        self.sectors_name = {}

    def get_sectors_name(self):
        """Scraping Sector Names from the website"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                # Set the default timeout to 90 seconds
                page.set_default_timeout(90000)

                # Navigate to the target URL with timeout of 90 seconds
                page.goto(self.all_sectors_page, wait_until="domcontentloaded")

                # Wait for the elements to appear
                target = self.sectors_tag["Sector_tag"]
                page.wait_for_selector(target)

                # Extract data: Find all elements of Sector Name
                sectors = page.locator(target).all_text_contents()

                # Printing the scraped data using loop
                for sector_count, sector in enumerate(sectors, start=1):
                    print(f"{sector_count}. {sector.title()}")
                    # Removing the whitespaces from the sector name
                    sector.strip()
                    self.sectors_name[sector.title()] = None
        except Exception as e:
            print("ERROR OCCURED WHILE SCRAPING SECTORS NAME")
            print(f"ERROR CODE: {e}")


if __name__ == "__main__":
    sector_scraper = SectorLinks()
    sector_scraper.get_sectors_name()