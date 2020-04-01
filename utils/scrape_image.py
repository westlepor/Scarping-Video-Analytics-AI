"""
Scrape Images from cctv url

"""

import requests
import urllib3
import cv2
import re
from bs4 import BeautifulSoup
from utils.scrape_cctv_info import get_cctv_url
import time

def get_image():
    # 5 urls
    url_list = [get_cctv_url()[231], get_cctv_url()[352], get_cctv_url()[233], get_cctv_url()[235], get_cctv_url()[237]]
    resource_url_list = []

    for url in url_list:
        # Get image and video urls
        raw_source = requests.get(url).text
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, 'lxml')

        # For Video
        if raw_source.find("sourceURL") != -1:
            m3u8_url = raw_source[raw_source.find("sourceURL") + len("sourceURL") + 3 : raw_source.find("posterFrameURL") - 3]
            resource_url = re.sub(r'[^a-zA-Z0-9:_/.]', '', m3u8_url)
        # For Image
        else:
            start = [m.start() for m in re.finditer('http://cwwp2', raw_source)][-1]
            end = [m.start() for m in re.finditer('jpg?', raw_source)][-1] + 3
            resource_url = raw_source[start:end]
        
        resource_url_list.append(resource_url)

    while True:
        for index, url in enumerate(resource_url_list):
            video = cv2.VideoCapture(url)
            ret, frame = video.read()
            filename = "imgs/test" + str(index) + ".jpg"
            cv2.imwrite(filename, frame)
        # Every 2 mins
        time.sleep(120)