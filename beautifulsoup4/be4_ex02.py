from bs4 import BeautifulSoup

html = html = '''
<h1 id="title">한빛출판네트워크</h1>
<div class="top">
    <ul class="menu">
        <li>
            <a href=http://www.hanbit.co.kr/member/login.html class="login">로그인</a>
        </li>
    </ul>
    <ul class="brand">
        <li>
            <a href="http://www.hanbit.co.kr/media/">한빛미디어</a>
        <li>
            <a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a>
        </li>
    </ul>
</div>
'''


soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())
# print(soup.h1)
# tag_div = soup.div
# print(tag_div)
# tag_ul = soup.ul
# print(tag_ul)
# tag_li = soup.li
# print(tag_li)
# tag_a = soup.a
# print(tag_a)
# tag_ul_all = soup.find_all('ul')
# # print(tag_ul_all)
# for tag in tag_ul_all:
#     print(tag.li.a.get_text())
# tag_a_all = soup.find_all('a')
# print(tag_a_all)
# tag_a = soup.a
# print(tag_a.attrs)
# print(tag_a['href'])
# print(tag_a['class'])
# tag_ul_2 = soup.find('ul',attrs={'class':'brand'})
# print(tag_ul_2.prettify())
# title = soup.find(id='title')
# print(title)
# title.string
# print(title.string)
li_list = soup.select('div > ul.brand > li')
print(li_list)
for li in li_list:
    print(li.string)