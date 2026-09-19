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
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # Set the default timeout to 90 seconds
                page.set_default_timeout(90000)

                # Navigate to the target URL
                page.goto(self.all_sectors_page, wait_until="domcontentloaded")

                # Wait for the elements to appear
                target = self.sectors_tag["Sector_tag"]
                page.wait_for_selector(target)

                # Extract data: Find all elements of Sector Name
                sectors = page.locator(target).all_text_contents()

                # Printing the scraped data using loop
                for sector_count, sector in enumerate(sectors, start=1):
                    # print(f"{sector_count}. {sector.title()}") # Uncomment to print
                    # Removing the whitespaces from the sector name
                    sector.strip()
                    self.sectors_name[sector.title()] = None

        # Printing the ERROR if it happens
        except Exception as e:
            print("ERROR OCCURED WHILE SCRAPING SECTORS NAME")
            print(f"ERROR CODE: {e}")

    def get_sectors_link(self):
        """Scraping sector page link from the website"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # Set the default timeout to 90 seconds
                page.set_default_timeout(90000)

                # Navigate to the target URL
                page.goto(self.all_sectors_page, wait_until="domcontentloaded")

                # Wait for the elements to appear
                sector_target = self.sectors_tag["Sector_tag"]
                page.wait_for_selector(sector_target)

                # Read the href attribute from every matching <a>
                # Extract the data (links)
                sector_links = page.locator(sector_target).evaluate_all(
                    "els => els.map(e=> e.getAttribute('href'))"
                )
                # List to store full urls of the sectors
                full_links = []

                # Looping to create the full URL of the sector page
                counter = 0 # To count sectors
                for sector_link in sector_links:
                    full_url = urljoin(self.all_sectors_page, sector_link)
                    full_links.append(full_url)

                # Adding the scraped link in the attribute dictionary with keys
                # Printing the links and the sector name through key and value
                print("Sector available on the website")
                for key, value in zip(self.sectors_name.keys(), full_links):
                    counter +=1 # Incrementing with every run
                    self.sectors_name[key] = value
                    print(f"{counter}. Link of the sector {key}: {value}")

        # Printing the ERROR if it happens
        except Exception as e:
            print("Error OCCURED WHILE SCRAPING THE LINK")
            print(f"ERROR CODE: {e}")



if __name__ == "__main__":
    sector_scraper = SectorLinks()
    sector_scraper.get_sectors_name()
    sector_scraper.get_sectors_link()