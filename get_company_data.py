import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
from deduce_sector import deduce_sector
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def get_company_data():
    url = 'https://en.wikipedia.org/wiki/Category:Companies_in_the_S%26P_400'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    companies = soup.find_all("div", class_="mw-category-group")

    data = []

    for company in companies:
        links = company.find_all('a')
        for link in links:
            company_page_url = f"https://en.wikipedia.org{link['href']}"
            logging.info(f"Processing company page: {company_page_url}")
            company_page = requests.get(company_page_url)
            company_soup = BeautifulSoup(company_page.content, 'html.parser')
            try:
                website = company_soup.find(string='Website').find_next('a').get('href')
                logging.info(f"Website found: {website}")
            except:
                website = "Not available"
                logging.warning("Website not found.")

            page_text = company_soup.get_text()
            # Filter out special characters and non-words
            tokens = word_tokenize(page_text)
            tokens = [token for token in tokens if token.isalpha() and token not in stopwords.words('english')]
            filtered_text = ' '.join(tokens)
            sectors = deduce_sector(filtered_text)
            for sector in sectors:
                data.append({'Name': link.text, 'Website': website, 'Sector': sector})

    return pd.DataFrame(data)
