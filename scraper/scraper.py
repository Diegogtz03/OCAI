import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
# PRICES - https://www.oracle.com/cloud/price-list/

def parse_sub_link(new_link):
    req = requests.get('https://www.oracle.com/cloud/price-list/')
    # print(req.content)

    soup = BeautifulSoup(req.content)
    print(soup.get_text(separator='\n', strip=True))

req = requests.get('https://www.oracle.com/cloud/price-list/')
# print(req.content)

soup = BeautifulSoup(req.content)
print(re.sub(r"\n{3,}|\s{2,}", "\n", soup.get_text(separator='\n', strip=True)))

for link in BeautifulSoup(req.content, 'html.parser', parse_only=SoupStrainer('a')):
    if link.has_attr('href'):
        if '#' in link['href'] and 'pricing' in link['href']:
            print(link['href'])
            
            if 'http' in link['href']:
                parse_sub_link(link['href'])
            else:
                parse_sub_link('https://www.oracle.com/cloud/price-list' + link['href'])
            
    
    # input('GO')

