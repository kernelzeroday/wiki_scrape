import asyncio
import concurrent.futures
import logging
import pandas as pd
from get_company_data import get_company_data
import json
import aiohttp
from bs4 import BeautifulSoup
from tqdm import tqdm
from sector_keywords import sector_keywords

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='scrape.log', filemode='a')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

def group_by_sector(df):
    return df.groupby('Sector')

async def validate_website(url, max_depth=5, current_depth=0):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        async with aiohttp.ClientSession() as session:
            async with session.head(url, headers=headers, allow_redirects=True) as response:
                if response.status == 200 or response.status == 403:
                    return url, True
                else:
                    logging.warning(f"Invalid website URL: {url} (status code {response.status})")
                    return url, False
    except aiohttp.ClientError as e:
        logging.error(f"Error validating website URL: {url} - {e}")
        return url, False

async def search_company_website_wikipedia(company_name, max_depth=5, current_depth=0):
    if current_depth >= max_depth:
        logging.warning(f"Maximum recursion depth reached for {company_name}")
        return company_name, None

    search_url = f"https://en.wikipedia.org/w/index.php?search={company_name}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    link = soup.find('a', href=True, text='Official website')
                    if link:
                        website_url = link['href']
                        return company_name, website_url
                    else:
                        logging.warning(f"No official website link found on Wikipedia for {company_name}")
                        return company_name, None
                else:
                    logging.warning(f"Failed to retrieve company information from Wikipedia (status code {response.status})")
                    return company_name, None
    except aiohttp.ClientError as e:
        logging.error(f"Error searching for company website on Wikipedia: {e}")
        return company_name, None

async def parse_redirected_page_content(url, max_depth=5, current_depth=0):
    if current_depth >= max_depth:
        logging.warning(f"Maximum recursion depth reached for {url}")
        return None

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    return soup
                else:
                    logging.warning(f"Failed to retrieve page content from {url} (status code {response.status})")
                    return None
    except aiohttp.ClientError as e:
        logging.error(f"Error retrieving page content from {url} - {e}")
        return None

def log_classification_data(keywords, weights, correct):
    logging.info(f"Classification data: keywords={keywords}, weights={weights}, correct={correct}")

async def process_sector(sector_name, sector_group):
    sector_details = {'Sector': sector_name, 'Companies': []}
    for row in sector_group.itertuples():
        url, is_valid = await validate_website(row.Website)
        if not is_valid:
            logging.warning(f"Skipping company {row.Name} due to invalid website URL: {url}")
            company_name, website_url = await search_company_website_wikipedia(row.Name)
            if website_url:
                url, is_valid = await validate_website(website_url)
                if not is_valid:
                    logging.warning(f"Skipping company {row.Name} due to invalid website URL after Wikipedia search: {website_url}")
                    continue
            else:
                continue
        company_info = {'Name': row.Name, 'Website': url}
        sector_details['Companies'].append(company_info)
    return sector_details

async def main():
    logging.info("Starting main function")
    df = await get_company_data()
    print("Data fetched", df.head())
    if df.empty:
        logging.error("No data retrieved.")
    else:
        logging.info("Data retrieved successfully")
        grouped_data = group_by_sector(df)
        logging.info("Data grouped by sector")
        report_text = ""
        report_json = {}

        # Prepare a list of coroutines for asyncio.gather
        tasks = [process_sector(name, group) for name, group in grouped_data]
        sector_details_list = await asyncio.gather(*tasks)

        for sector_details in sector_details_list:
            logging.info(f"Processed sector: {sector_details['Sector']}")
            report_json[sector_details['Sector']] = sector_details
            sector_info = f"Sector: {sector_details['Sector']}\n"
            for company in sector_details['Companies']:
                sector_info += f"Name: {company['Name']}, Website: {company['Website']}\n"
            report_text += sector_info

        try:
            with open('sector_report.txt', 'w') as text_file:
                text_file.write(report_text)
            with open('sector_report.json', 'w') as json_file:
                json.dump(report_json, json_file, indent=4)
            logging.info("Reports generated in both text and JSON formats.")
        except Exception as e:
            logging.error(f"Error writing reports: {e}")

if __name__ == "__main__":
    asyncio.run(main())

