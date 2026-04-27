import pandas as pd
from bs4 import BeautifulSoup
import urllib.request


def Music_rank(result,search_day):
    music_url = 'https://music.bugs.co.kr/chart/track/day/total?chartdate=%d'% int(search_day)
    html = urllib.request.urlopen(music_url)
    soup = BeautifulSoup(html, 'html.parser')
    tag_tbody = soup.find('tbody')
    for tr in tag_tbody.find_all('tr'):
        rank_tag = tr.find('div',class_='ranking')
        rank = rank_tag.find('strong').string

        artist_tag = tr.find('p', class_='artist')
        singer = artist_tag.find('a').string

        title_tag = tr.find('p', class_='title')
        title = title_tag.find('a').string
        result.append([search_day] + [rank] + [singer] + [title])
        print([search_day] + [rank] + [singer] + [title])


def main():
    result = []
    print('Bugs music crawling >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    while True:
        search_day = input('검색할 날짜를 입력하세요(입력 가능한 날짜는 2006년9월22일부터 하루전까지): ')
        if len(search_day) != 8:
            print('검색 형식을 맞춰주세요.')
            continue
        try:
            Music_rank(result,search_day)
        except:
            print('해당 날짜는 데이터가 없습니다.')
            continue
        music_tbl = pd.DataFrame(result, columns=['search_day','rank','singer','title'])
        music_tbl.to_csv(f'bugschart_{search_day}.csv', encoding='utf-8', mode='w', index=False)
        del result[:]
        break

if __name__ == '__main__':
    main()
