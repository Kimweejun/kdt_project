# pip install beautifulsoup4
# 참고사이트 https://beautiful-soup-4.readthedocs.io/en/latest/

# 웹크롤링
# 정적 : Beautiful Soup
# 동적 : Selenium

from bs4 import BeautifulSoup
import urllib.request as MYURL

# fp = open("song.xml","r")
# soup = BeautifulSoup(fp, "html.parser")
#
# for song in soup.find_all('song'):
#     print(song['album'])
#     print(song.title.string)
#     print(song.length.string)
#     print()

# fp = open("song.xml","r", encoding="utf-8")
# openFile = fp.read()
# soup = BeautifulSoup(openFile, "html.parser")
#
# for song in soup.find_all('song'):
#     print(song['album'])
#     print(song.title.string)
#     print(song.length.string)
#     print()

from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

fp = open("joins.xml","r", encoding="utf-8")
openFile = fp.read()
soup = BeautifulSoup(openFile, "html.parser")

for data in soup.find_all('item'):
    print("title",data.title.string)
    print("description",data.description.string)
