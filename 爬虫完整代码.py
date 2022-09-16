import requests
import csv
from bs4 import BeautifulSoup

# 设置列表，用以存储每本书籍的信息
data_list = []
# 设置页码 page_number
page_number = 1

# while 循环的条件设置为 page_number 的值是否小于 4
while page_number < 4:
    # 设置要请求的网页链接
    url = 'https://wp.forchange.cn/resources/page/' + str(page_number)

    # 请求网页
    books_list_res = requests.get(url)

    # 解析请求到的网页内容
    bs = BeautifulSoup(books_list_res.text, 'html.parser')
    # 搜索网页中所有包含书籍名和书籍链接的 Tag
    href_list = bs.find_all('a', class_='post-title')

    # 使用 for 循环遍历搜索结果
    for href in href_list:
        # 创建字典，用以存储书籍信息
        info_dict = {}
        # 提取书籍名
        info_dict['书名'] = href.text
        # 提取书籍链接
        book_url = href['href']
        # 通过书籍链接请求书籍详情页
        book_list_res = requests.get(book_url)

        # 解析书籍详情页的内容
        new_bs = BeautifulSoup(book_list_res.text, 'html.parser')
        # 搜索网页中所有包含书籍各项信息的 Tag
        info_list = new_bs.find('div', class_='res-attrs').find_all('dl')

        # 遍历搜索结果，提取书籍各项信息，存储到字典中
        for info in info_list:
            # 提取信息的提示项
            key = info.find('dt').text[:-2]
            # 提取信息的内容
            value = info.find('dd').text
            # 将信息添加到字典中
            info_dict[key] = value

        # 打印书籍的信息
        print(info_dict)
        # 存储每本书籍的信息
        data_list.append(info_dict)

    # 页码 page_number 自增
    page_number += 1

# 新建 csv 文件存储书籍信息
with open('books.csv', 'w') as f:
    # 将文件对象转换成 DictWriter 对象
    writer = csv.DictWriter(f, fieldnames=['书名', '作者', '出版社', 'ISBN', '页数', '出版年', '定价'])
    # 写入表头与数据
    writer.writeheader()
    writer.writerows(data_list)
