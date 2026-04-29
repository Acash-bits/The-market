from playwright.sync_api import sync_playwright

def run():
    """Scraping the company ticker from the website"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the target URL
        page.goto("https://companiesmarketcap.com")

        # Wait for elements to appear
        page.wait_for_selector('div[class="company-name"]')
        # Extract data: Find all elements of company_name class
        company_names = page.locator('div[class="company-name"]').all_text_contents()
        # Print the results
        for i, company_name in enumerate(company_names, 1):
            print(f"\n{i}.Company Name : {company_name}")
        
        browser.close()

if __name__ == "__main__":
    run()