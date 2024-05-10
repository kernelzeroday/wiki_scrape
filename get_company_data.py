import pandas as pd
import aiohttp
from bs4 import BeautifulSoup
import logging
from deduce_sector import deduce_sector
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import asyncio

async def get_company_data():
    url = 'https://en.wikipedia.org/wiki/Category:Companies_in_the_S%26P_400'
    stopwords_set = set(stopwords.words('english'))  # Load stopwords once
    data = []
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status != 200:
            logging.error(f"Failed to retrieve data from {url}")
            return pd.DataFrame()  # Return empty DataFrame on failure
        soup = BeautifulSoup(await response.text(), 'html.parser')
        companies = soup.find_all("div", class_="mw-category-group")

        for company in companies:
            links = company.find_all('a')
            for link in links:
                company_page_url = f"https://en.wikipedia.org{link['href']}"
                logging.info(f"Processing company page: {company_page_url}")
                try:
                    company_page = await session.get(company_page_url)
                    company_soup = BeautifulSoup(await company_page.text(), 'html.parser')
                    website_tag = company_soup.find(string='Website')
                    website = website_tag.find_next('a').get('href') if website_tag else "Not available"
                except Exception as e:
                    website = "Not available"
                    logging.warning(f"Website not found for {link.text}: {e}")

                page_text = company_soup.get_text() if company_page.status == 200 else ""
                tokens = [token for token in word_tokenize(page_text) if token.isalpha() and token not in stopwords_set]
                filtered_text = ' '.join(tokens)
                sectors = await deduce_sector(filtered_text)
                for sector in sectors:
                    data.append({'Name': link.text, 'Website': website, 'Sector': sector})

    return pd.DataFrame(data)

