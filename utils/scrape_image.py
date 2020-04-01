"""
Scrape Images from cctv url

"""

import requests
import urllib3
import cv2
import re
from bs4 import BeautifulSoup
from utils.scrape_cctv_info import get_cctv_url

def get_image():
    # url = get_cctv_url()[231]
    url = "http://cwwp2.dot.ca.gov/vm/loc/d4/tvd13i80tollplaza.htm"
    raw_source = requests.get(url).text

    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, 'lxml')

    if raw_source.find("sourceURL") != -1:
        m3u8_url = raw_source[raw_source.find("sourceURL") + len("sourceURL") + 3 : raw_source.find("posterFrameURL") - 3]
        video_url = re.sub(r'[^a-zA-Z0-9:_/.]', '', m3u8_url)
    else:
        start = [m.start() for m in re.finditer('http://cwwp2', raw_source)][-1]
        end = [m.start() for m in re.finditer('jpg?', raw_source)][-1] + 3
        video_url = raw_source[start:end]

    while True:
        video = cv2.VideoCapture(video_url)
        ret, frame = video.read()
        cv2.imwrite("test.jpg", frame)
        if cv2.waitKey() == 27:
            break

    cv2.destroyAllWindows()