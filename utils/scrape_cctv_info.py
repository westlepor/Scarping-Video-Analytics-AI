"""
Retrieve CCTV Informations(URL, Location, etc) from JS file

"""

import urllib3
import json
import re
from bs4 import BeautifulSoup
import requests
import csv

def get_cctv_url():
    """ Scrape cctv live url from js variable
    """
    # Retrieve external js file
    http = urllib3.PoolManager()
    base_url = 'http://cwwp2.dot.ca.gov/vm/iframemap.htm'
    response = http.request('GET', base_url)
    soup = BeautifulSoup(response.data, 'lxml')
    data  = soup.find_all("script")

    # Get js file location which contain cctv information
    cctv_info_url = 'http://cwwp2.dot.ca.gov/vm/' + data[2]['src']

    # Parse js variable to get urls array
    cctv_info_content = requests.get(cctv_info_url).text
    cctv_urls = []
    for line in cctv_info_content.splitlines():
        url = line[line.find('http') : line.find('htm') + 3]
        if url:
            cctv_urls.append(url)

    with open('cctv_info.csv', 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(cctv_urls)

    return cctv_urls