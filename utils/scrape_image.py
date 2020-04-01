"""
Scrape Images from cctv url

"""

import requests
import cv2
import subprocess as sp
import numpy
import re
from scrape_cctv_info import get_cctv_url

FFMPEG_BIN = "ffmpeg.exe"
url = get_cctv_url()[231]
raw_source = requests.get(url).text
m3u8_url = raw_source[raw_source.find("sourceURL") + len("sourceURL") + 3 : raw_source.find("posterFrameURL") - 3]
video_url = re.sub(r'[^a-zA-Z0-9:_/.]', '', m3u8_url)

pipe = sp.Popen([ FFMPEG_BIN, "-i", video_url,
           "-loglevel", "quiet",
           "-an",
           "-f", "image2pipe",
           "-pix_fmt", "bgr24",
           "-vcodec", "rawvideo", "-"],
           stdin = sp.PIPE, stdout = sp.PIPE)

while True:
    raw_image = pipe.stdout.read(640*480*3)
    image =  numpy.fromstring(raw_image, dtype='uint8').reshape((480,640,3))
    cv2.imshow("cctv_road",image)
    if cv2.waitKey(5) == 27:
        break

pipe.stdout.flush()

cv2.destroyAllWindows()