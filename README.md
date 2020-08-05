# Scraping Video from this map site and detecting cars on the road
http://cwwp2.dot.ca.gov/vm/iframemap.htm

## Get CCTV camera urls from map site
Used several python libraries for scraping such as beautifulsoup4.
The m3u8 data which extracted by ffmpeg from each live camera is sent for car detection in the road.
<img src="./assets/map.png?raw=true">

## Detect Cars and Send numbers of cars as json into backend in real-time
Detected Cars using DarkNet in low quality images for more accuracy.
Integrated deep learning model into backend
<img src="./assets/1.jpg?raw=true">
