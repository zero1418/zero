import csv
import requests
from bs4 import BeautifulSoup

# 设置列表，用以存储每部电影的信息
data_list = []
# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

# 使用 for 循环遍历取值范围为 0~3 的数据
for page_number in range(4):
    # 设置要请求的网页链接
    url = 'https://movie.douban.com/top250?start={}&filter='.format(page_number * 25)
    # 请求网页
    movies_list_res = requests.get(url, headers=headers)
    # 解析请求到的网页内容
    bs = BeautifulSoup(movies_list_res.text, 'html.parser')
    # 搜索网页中所有包含单部电影全部信息的 Tag
    movies_list = bs.find_all('div', class_='item')

    # 使用 for 循环遍历搜索结果
    for movie in movies_list:
        # 提取电影的序号
        movie_num = movie.find('em').text
        # 提取电影名
        movie_name = movie.find('span').text
        # 提取电影的评分
        movie_score = movie.find("span", class_='rating_num').text
        # 提取电影的推荐语
        movie_instruction = movie.find("span", class_='inq').text
        # 提取电影的链接
        movie_link = movie.find('a')['href']

        # 将信息添加到字典中
        movie_dict = {
            '序号': movie_num,
            '电影名': movie_name,
            '评分': movie_score,
            '推荐语': movie_instruction,
            '链接': movie_link
        }

        # 打印电影的信息
        print(movie_dict)
        # 存储每部电影的信息
        data_list.append(movie_dict)

# 新建 csv 文件，用以存储电影信息
with open('movies.csv', 'w', encoding='utf-8-sig') as f:
    # 将文件对象转换成 DictWriter 对象
    f_csv = csv.DictWriter(f, fieldnames=['序号', '电影名', '评分', '推荐语', '链接'])
    # 写入表头与数据
    f_csv.writeheader()
    f_csv.writerows(data_list)