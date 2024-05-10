import asyncio
import concurrent.futures
import logging
import pandas as pd
from get_company_data import get_company_data
import json
import aiohttp
from bs4 import BeautifulSoup
from tqdm import tqdm
from tqdm.asyncio import tqdm as async_tqdm
from sector_keywords import sector_keywords
from typing import List, Tuple, Dict, Any
from functools import wraps
import os
import sys
import colorlog
from urllib.parse import urlparse
log_format='%(log_color)s%(asctime)s-%(levelname)s-%(message)s'
log_colors={'DEBUG':'cyan','INFO':'green','WARNING':'yellow','ERROR':'red','CRITICAL':'red,bg_white',}
formatter=colorlog.ColoredFormatter(log_format,log_colors=log_colors)
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler=logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
file_handler_pretty=logging.FileHandler('scrape_pretty.log')
file_handler_pretty.setFormatter(formatter)
logger.addHandler(file_handler_pretty)
file_handler_grep=logging.FileHandler('scrape_grep.log')
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
def group_by_sector(df:pd.DataFrame)->pd.core.groupby.generic.DataFrameGroupBy:
 return df.groupby('Sector')
@log_input
def validate_website(url:str)->Tuple[str,bool]:
 parsed_url=urlparse(url)
 if parsed_url.scheme and parsed_url.netloc:
  return url,True
 else:
  logger.warning(f"Invalid website URL: {url}")
  return url,False
@log_input
def validate_multiple_websites(urls:List[str])->List[Tuple[str,bool]]:
 results=[validate_website(url) for url in urls]
 return results
@log_input
async def search_company_website_wikipedia(company_name:str,max_depth:int=5,current_depth:int=0)->Tuple[str,str]:
 if current_depth>=max_depth:
  logger.warning(f"Maximum recursion depth reached for {company_name}")
  return company_name,None
 search_url=f"https://en.wikipedia.org/w/index.php?search={company_name}"
 try:
  headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
  async with aiohttp.ClientSession() as session:
   async with session.get(search_url,headers=headers) as response:
    if response.status==200:
     soup=BeautifulSoup(await response.text(),'html.parser')
     link=soup.find('a',href=True,string='Official website')
     if link:
      website_url=link['href']
      return company_name,website_url
     else:
      logger.warning(f"No official website link found on Wikipedia for {company_name}")
      return company_name,None
    else:
     logger.warning(f"Failed to retrieve company information from Wikipedia (status code {response.status})")
     return company_name,None
 except aiohttp.ClientError as e:
  logger.error(f"Error searching for company website on Wikipedia: {e}")
  return company_name,None
@log_input
async def parse_redirected_page_content(url:str,max_depth:int=5,current_depth:int=0)->BeautifulSoup:
 if current_depth>=max_depth:
  logger.warning(f"Maximum recursion depth reached for {url}")
  return None
 try:
  headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
  async with aiohttp.ClientSession() as session:
   async with session.get(url,headers=headers) as response:
    if response.status==200:
     soup=BeautifulSoup(await response.text(),'html.parser')
     return soup
    else:
     logger.warning(f"Failed to retrieve page content from {url} (status code {response.status})")
     return None
 except aiohttp.ClientError as e:
  logger.error(f"Error retrieving page content from {url} - {e}")
  return None
@log_input
def log_classification_data(keywords:List[str],weights:List[float],correct:bool)->None:
 logger.info(f"Classification data: keywords={keywords}, weights={weights}, correct={correct}")
@log_input
async def process_sector(sector_name:str,sector_group:pd.DataFrame)->Dict[str,Any]:
 sector_details={'Sector':sector_name,'Companies':[]}
 async with asyncio.Semaphore(10):
  tasks=[asyncio.create_task(process_company(row)) for row in sector_group.itertuples()]
  async for result in async_tqdm(asyncio.as_completed(tasks),total=len(tasks)):
   if result:
    sector_details['Companies'].append(result)
 return sector_details
@log_input
async def process_company(row:pd.Series)->Dict[str,str]:
 url,is_valid=validate_website(row.Website)  # Removed await as validate_website is not an async function
 if not is_valid:
  logger.warning(f"Skipping company {row.Name} due to invalid website URL: {url}")
  company_name,website_url=await search_company_website_wikipedia(row.Name)
  if website_url:
   url,is_valid=validate_website(website_url)  # Removed await as validate_website is not an async function
   if not is_valid:
    logger.warning(f"Skipping company {row.Name} due to invalid website URL after Wikipedia search: {website_url}")
    return None
  else:
   return None
 return {'Name':row.Name,'Website':url}
@log_input
async def main()->None:
 logger.info("Starting main function")
 df=await get_company_data()
 print("Data fetched",df.head())
 if df.empty:
  logger.error("No data retrieved.")
 else:
  logger.info("Data retrieved successfully")
  grouped_data=group_by_sector(df)
  logger.info("Data grouped by sector")
  report_text=""
  report_json={}
  tasks=[asyncio.create_task(process_sector(name,group)) for name,group in grouped_data]
  sector_details_list=[]
  async for sector_details_task in async_tqdm(asyncio.as_completed(tasks),total=len(tasks)):
   details = await sector_details_task  # Await the task to get the actual result
   logger.info(f"Processed sector: {details['Sector']}")
   sector_companies = []
   for company_task in details['Companies']:
    company = await company_task  # Await each company task
    if company is not None:  
     sector_companies.append(company)
   report_json[details['Sector']] = {
     'Sector': details['Sector'],
     'Companies': sector_companies
   }
   sector_info = f"Sector: {details['Sector']}\n"
   for company in sector_companies:
    sector_info += f"Name: {company['Name']}, Website: {company['Website']}\n"
   report_text += sector_info
   logger.debug(f"Current report_text: {report_text}")
   logger.debug(f"Current report_json: {json.dumps(report_json,indent=2)}")
  try:
   with open('sector_report.txt','w') as text_file,open('sector_report.json','w') as json_file:
    text_file.write(report_text)
    json.dump(report_json,json_file,indent=4)
   logger.info("Reports generated in both text and JSON formats.")
  except Exception as e:
   logger.error(f"Error writing reports: {e}")
if __name__=="__main__":
 asyncio.run(main())

