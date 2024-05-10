import pandas as pd
import aiohttp
from bs4 import BeautifulSoup
import logging
from deduce_sector import deduce_sector
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import asyncio
from typing import List,Dict,Any
from functools import wraps
import colorlog
log_format='%(log_color)s%(asctime)s-%(levelname)s-%(message)s'
log_colors={'DEBUG':'cyan','INFO':'green','WARNING':'yellow','ERROR':'red','CRITICAL':'red,bg_white',}
formatter=colorlog.ColoredFormatter(log_format,log_colors=log_colors)
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler=logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
file_handler_pretty=logging.FileHandler('get_company_data_pretty.log')
file_handler_pretty.setFormatter(formatter)
logger.addHandler(file_handler_pretty)
file_handler_grep=logging.FileHandler('get_company_data_grep.log')
file_handler_grep.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s-%(message)s'))
logger.addHandler(file_handler_grep)
def log_input(func):
 @wraps(func)
 def wrapper(*args,**kwargs):
  logger.debug(f"Entering {func.__name__} with args: {args}, kwargs: {kwargs}")
  result=func(*args,**kwargs)
  logger.debug(f"Exiting {func.__name__} with result: {result}")
  return result
 return wrapper
def log_output(func):
 @wraps(func)
 def wrapper(*args,**kwargs):
  result=func(*args,**kwargs)
  logger.debug(f"{func.__name__} returned: {result}")
  return result
 return wrapper
@log_input
@log_output
async def get_company_data()->pd.DataFrame:
 url='https://en.wikipedia.org/wiki/Category:Companies_in_the_S%26P_400'
 stopwords_set=set(stopwords.words('english'))
 data=[]
 async with aiohttp.ClientSession() as session:
  response=await session.get(url)
  if response.status!=200:
   logger.error(f"Failed to retrieve data from {url}")
   return pd.DataFrame()
  soup=BeautifulSoup(await response.text(),'html.parser')
  companies=soup.find_all("div",class_="mw-category-group")
  for company in companies:
   links=company.find_all('a')
   for link in links:
    company_page_url=f"https://en.wikipedia.org{link['href']}"
    logger.info(f"Processing company page: {company_page_url}")
    try:
     company_page=await session.get(company_page_url)
     company_soup=BeautifulSoup(await company_page.text(),'html.parser')
     website_tag=company_soup.find(string='Website')
     website=website_tag.find_next('a').get('href') if website_tag else "Not available"
    except Exception as e:
     website="Not available"
     logger.warning(f"Website not found for {link.text}: {e}")
    page_text=company_soup.get_text() if company_page.status==200 else ""
    tokens=[token for token in word_tokenize(page_text) if token.isalpha() and token not in stopwords_set]
    filtered_text=' '.join(tokens)
    sectors=await deduce_sector(filtered_text)
    for sector in sectors:
     data.append({'Name':link.text,'Website':website,'Sector':sector})
 return pd.DataFrame(data)
