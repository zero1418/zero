import csv
import requests
from bs4 import BeautifulSoup

# 设置列表，用以存储每本书籍的信息
data_list = []
# 设置登录网站的请求网址
login_url = 'https://wp.forchange.cn/wp-admin/admin-ajax.php'
# 输入用户的账号密码
username = input('请输入用户名：')
password = input('请输入密码：')

# 设置登录请求的请求体数据
login_data = {
    'action': 'ajaxlogin',
    'username': username,
    'password': password,
    'remember': 'true'
}

# 请求登录网站
login_res = requests.post(login_url, data=login_data)

# 设置要请求的书籍网页链接
book_list_url = 'https://wp.forchange.cn/resources/'
# 请求书籍列表页
book_list_res = requests.get(book_list_url)
# 解析请求到的书籍网页内容
soup = BeautifulSoup(book_list_res.text, 'html.parser')
# 搜索网页中所有包含书籍名和书籍链接的 Tag
book_href_list = soup.find_all('a', class_='post-title')

# 使用 for 循环遍历搜索结果
for href in book_href_list:
    
    # 提取书籍名
    book_name = href.text
    # 提取书籍链接
    book_url = href['href']
    # 携带获取到的 Cookies 信息请求书籍网页
    comment_res = requests.get(book_url, cookies=login_res.cookies)
    # 解析请求到的书籍网页内容
    soup = BeautifulSoup(comment_res.text, 'html.parser')

    # 搜索网页中包含评分信息的 Tag
    score_data = soup.find('div', id='curItemTotalStar')

    # 定位书籍评分所在的 Tag
    score = score_data.find('b')
    # 定位评分人数所在的 Tag
    score_number = score_data.find('p', class_='wk')

    # 若没有书籍评分，则提示 “暂无评分”，否则提取书籍评分
    if score == None:
        score = '暂无评分'
    else:
        score = score.text

    # 若没有评分人数，则提示 “暂无人评”，否则提取评分人数
    if score_number == None:
        score_number = '暂无人评'
    else:
        score_number = score_number.text[7:-5]

    # 将书籍的各项信息存入到字典 book_data
    book_data = {
        '书籍名称': book_name,
        '书籍评分': score,
        '评分人数': score_number
    }

    # 打印书籍的信息
    print(book_data)
    # 存储每本书籍的信息
    data_list.append(book_data)

# 新建 csv 文件存储书籍信息
with open('books.csv', 'w', encoding='utf-8-sig') as f:
    # 将文件对象转换成 DictWriter 对象
    writer = csv.DictWriter(f, fieldnames=['书籍名称', '书籍评分', '评分人数'])
    # 写入表头与数据
    writer.writeheader()
    writer.writerows(data_list)