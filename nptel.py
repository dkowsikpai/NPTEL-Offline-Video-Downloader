"""
 NPTEL Video Offline Downloader
 Author: Kowsik Nandagopan D
 Git: https://github.com/dkowsikpai

Initially install all the requirements using:
    pip install -r req.txt

Tested on Linux
"""

# Import Libraries
from bs4 import BeautifulSoup # pip install beautifulsoup4
from bs4.dammit import EncodingDetector
from requests import get
from tqdm import tqdm
import os

# Create directory
dirName = 'NPTEL'
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
resp = get(input("Enter course link: ")) # https://nptel.ac.in/courses/106/106/106106145/

# Encoding
http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
encoding = html_encoding or http_encoding
soup = BeautifulSoup(resp.content, parser, from_encoding=encoding)

# Scrapping
# https://nptel.ac.in/content/storage/106/106/106106145/MP4/mod01lec01.mp4
l = []
x = soup.find('table', {'id': "request"})
for i in x.find_all("tr"):
    tds = i.find_all("td")
    if len(tds) == 3:
        a = tds[2].find("a")
        href = a["href"]
        if href[-3:] == "mp4":
            l.append({
                "name": tds[1].text + ".mp4",
                "link": "https://nptel.ac.in" + href
            })

# Download
def download(url, name):
    response = get(url, stream=True) # create HTTP response object 
    # send a HTTP request to the server and save 
    # the HTTP response in a response object called r 
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open("./" + dirName + '/' + name, 'wb') as file: 
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

# Looping Each URL
start = int(input("Enter Start Lecture Number: "))
end = int(input("Enter End Lecture Number: "))

for i in range(start, end+1):
    print("Downloading", l[i-1]["name"])
    download(l[i-1]["link"], l[i-1]["name"])
    print("Downloaded")





