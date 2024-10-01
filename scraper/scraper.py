import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import os
from dotenv import load_dotenv
# PRICES - https://www.oracle.com/cloud/price-list/

def parse_sub_link(new_link):
    req = requests.get('https://www.oracle.com/cloud/price-list/')
    # print(req.content)

    soup = BeautifulSoup(req.content)
    print(soup.get_text(separator='\n', strip=True))

req = requests.get('https://www.oracle.com/cloud/price-list/')
# print(req.content)

soup = BeautifulSoup(req.content, features='html.parser')

# text = re.sub(r"\n{3,}|\s{2,}", "\n", soup.get_text(separator='\n', strip=True))
text = soup.get_text(separator='\n', strip=True)

# promt = "Interpret the following information from tables into price tables for these cloud services, return it in a clean an readable JSON format: " + text
# load_dotenv()
# req = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=' + os.getenv('GEMINI_API_KEY'), headers={'Content-Type': 'application/json'}, data='{"contents":[{"parts":[{"text":"' + promt + '"}]}]}')

# print(req.json())

# for link in BeautifulSoup(req.content, 'html.parser', parse_only=SoupStrainer('a')):
#     if link.has_attr('href'):
#         if '#' in link['href'] and 'pricing' in link['href']:
#             print(link['href'])
            
#             if 'http' in link['href']:
#                 parse_sub_link(link['href'])
#             else:
#                 parse_sub_link('https://www.oracle.com/cloud/price-list' + link['href'])
            
    
#             input('GO')

