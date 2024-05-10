import logging
import pandas as pd
from get_company_data import get_company_data
import json
import requests
from bs4 import BeautifulSoup

from sector_keywords import sector_keywords

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='scrape.log', filemode='a')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

def group_by_sector(df):
    return df.groupby('Sector')
def validate_website(url):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.ok or response.status_code == 403:  # Check for status code being 200-399 or 403
            return True
        else:
            logging.warning(f"Invalid website URL: {url} (status code {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Error validating website URL: {url} - {e}")
        return False

def log_classification_data(keywords, weights, correct):
    # Log the classification data for future model training
    logging.info(f"Classification data: keywords={keywords}, weights={weights}, correct={correct}")

def search_company_website_wikipedia(company_name):
    """
    Search for a company website using Wikipedia.
    """
    search_url = f"https://en.wikipedia.org/w/index.php?search={company_name}"
    try:
        response = requests.get(search_url)
        if response.ok:  # Simplified check for response status code being 200-399
            soup = BeautifulSoup(response.text, 'html.parser')
            link = soup.find('a', href=True, text='Official website')
            if link:
                website_url = link['href']
                return website_url
            else:
                logging.warning(f"No official website link found on Wikipedia for {company_name}")
                return None
        else:
            logging.warning(f"Failed to retrieve company information from Wikipedia (status code {response.status_code})")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error searching for company website on Wikipedia: {e}")
        return None
def parse_redirected_page_content(url):
    """
    Parse the content of the redirected page and extract relevant information.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            logging.warning(f"Failed to retrieve page content from {url} (status code {response.status_code})")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving page content from {url} - {e}")
        return None

df = get_company_data()
if df.empty:
    logging.error("No data retrieved.")
else:
    grouped_data = group_by_sector(df)
    report_text = ""
    report_json = {}
    for name, group in grouped_data:
        sector_details = {'Companies': []}
        for _, row in group.iterrows():
            company_info = {'Name': row['Name'], 'Website': row['Website']}
            if not validate_website(row['Website']):
                # Search for the website using Wikipedia
                website_url = search_company_website_wikipedia(row['Name'])
                if website_url:
                    company_info['Website'] = website_url
                else:
                    logging.warning(f"Skipping company {row['Name']} due to invalid website URL: {row['Website']}")
            if validate_website(company_info['Website']):
                # Parse the content of the redirected page
                page_content = parse_redirected_page_content(company_info['Website'])
                if page_content:
                    pass
                sector_details['Companies'].append(company_info)
            else:
                logging.warning(f"Skipping company {row['Name']} due to invalid website URL: {company_info['Website']}")
            # Log the classification data
            keywords = [{'keyword': key, 'weight': value} for sector in sector_keywords.values() for key, value in sector.items()]
            weights = [keyword['weight'] for keyword in keywords]
            correct = True  # Assume correct classification for now
            log_classification_data(keywords, weights, correct)
        report_json[name] = sector_details
        sector_info = f"Sector: {name}\n"
        for company in sector_details['Companies']:
            sector_info += f"Name: {company['Name']}, Website: {company['Website']}\n"
        print(sector_info)
        report_text += sector_info
    try:
        with open('sector_report.txt', 'w') as text_file:
            text_file.write(report_text)
        with open('sector_report.json', 'w') as json_file:
            json.dump(report_json, json_file, indent=4)
        logging.info("Reports generated in both text and JSON formats.")
    except Exception as e:
        logging.error(f"Error writing reports: {e}")

