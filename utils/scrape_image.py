"""
Scrape Images from cctv url

"""

import requests
import cv2
import subprocess as sp
import numpy
import re
from utils.scrape_cctv_info import get_cctv_url

def get_image():
    FFMPEG_BIN = "ffmpeg.exe"
    url = get_cctv_url()[231]
    raw_source = requests.get(url).text
    m3u8_url = raw_source[raw_source.find("sourceURL") + len("sourceURL") + 3 : raw_source.find("posterFrameURL") - 3]
    video_url = re.sub(r'[^a-zA-Z0-9:_/.]', '', m3u8_url)

    while True:
        video = cv2.VideoCapture(video_url)
        ret, frame = video.read()
        cv2.imwrite("test.jpg", frame)
        if cv2.waitKey() == 27:
            break

    cv2.destroyAllWindows()