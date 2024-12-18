from playwright.sync_api import sync_playwright
import browser_cookie3
import json
import time

def get_chrome_cookies(domain):
    """Extract cookies from Chrome for a specific domain"""
    cookies = browser_cookie3.chrome(domain_name=domain)
    # print(cookies[0].name)
    cookie_dict = []
    for cookie in cookies:
        cookie_dict.append({
            'name': cookie.name,
            'value': cookie.value,
            'domain': cookie.domain,
            'path': cookie.path
        })
    return cookie_dict

def scrape_wisetechacademy():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Set headless=True in production
        context = browser.new_context()
        page = context.new_page()

        # Get cookies from Chrome
        cookies = get_chrome_cookies('wisetechacademy.com')
        context.add_cookies(cookies)

        # Navigate to the website
        page.goto('https://wisetechacademy.com/explore/product-learning/')
        
        # Wait for the page to load
        page.wait_for_selector('.accordion-item')

        # Find and click the Quickstarts section
        quickstarts = page.locator("text=Quickstarts").first
        quickstarts.click()

        # Wait for the content to load
        page.wait_for_selector('.search-result-title')

        # Extract quickstart information
        quickstarts_data = []
        
        # Get all quickstart items
        items = page.locator('.main-container').all()
        
        for item in items:
            try:
                title = item.locator('.search-result-title').inner_text()
                description = item.locator('.summary-text').inner_text()
                
                # Get metadata (if available)
                metadata = {
                    'product': item.locator('.card-heading').inner_text(),
                    'type': item.locator('.quickstart-learning-type').inner_text(),
                    'published_date': item.locator('.footer-info').inner_text()
                }
                
                quickstarts_data.append({
                    'title': title,
                    'description': description,
                    'metadata': metadata
                })
            except:
                continue

        # Save the results
        with open('quickstarts.json', 'w', encoding='utf-8') as f:
            json.dump(quickstarts_data, f, indent=2, ensure_ascii=False)

        # Close the browser
        browser.close()

if __name__ == "__main__":
    scrape_wisetechacademy()