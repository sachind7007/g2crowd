import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_company_details(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            await page.goto(url)

            # Wait for the required elements to appear on the page
            await page.wait_for_selector('h1')
            await page.wait_for_selector('//div[contains(@class, "css-u003cdiv")]', timeout=10000)  

            # Scrape the required information from the page
            company_name = await page.text('h1')
            company_description = await page.text('//div[contains(@class, "css-u003cdiv")]')
            # ... Add more fields to scrape as per your requirement

            # Create a dictionary to store the scraped data
            company_details = {
                'Company Name': company_name,
                'Company Description': company_description,
                # ... Add more fields as per your requirement
            }

            return company_details

        except Exception as e:
            print(f"An error occurred while scraping company details: {e}")

        finally:
            await browser.close()

async def main():
    # Provide the path to your CSV file containing G2Crowd URLs
    csv_file_path = r'E:\thinkbridge\g2crowd_urls.csv'
    output_file_path = 'output.json'

    # Read the CSV file and extract the URLs
    urls = []
    with open(csv_file_path, 'r') as file:
        for line in file:
            urls.append(line.strip())

    scraped_data = []
    for url in urls:
        data = await scrape_company_details(url)
        scraped_data.append(data)

    # Save the scraped data to a JSON file
    with open(output_file_path, 'w') as file:
        json.dump(scraped_data, file, indent=4)

    print("Scraping completed and data saved to output.json")

if __name__ == '__main__':
    asyncio.run(main())
