from bs4 import BeautifulSoup
import requests
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

serviceKey = "bEN6V0S1X1t%2F9g6gW6tw9oLyS80Et3DFdyFWk2ReJi5JaaitcpueGhEOficFv36f95iL6AHfL%2BVv7tCGaIhmbQ%3D%3D"
YM = "202206"

URL = ("http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList")
URL += "?serviceKey=" + serviceKey
URL += "&YM=" + YM
print(URL)

response = requests.get(URL)
soup = BeautifulSoup(response.content.decode(encoding='UTF-8', errors='strict'), 'html.parser')

print(soup.prettify())
for item in soup.find_all("item"):
    print("ed:", item.ed.string)
    print("edCd:", item.edcd.string)
    print("natCd:", item.natcd.string)
    print("natKorNm:", item.natkornm.string)
    print("num:", item.num.string)
    print("rnum", item.rnum.string)
    print("ym:", item.ym.string)
    print("---------------------------------------------")