import csv
import requests
from bs4 import BeautifulSoup

# (headers 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

# 设置列表，用以存储每种食物的信息
data_list = []

# 使用 for 循环遍历取值范围为 1~3 的数据
for type_number in range(1, 4):
    # 使用 for 循环遍历取值范围为 1~3 的数据
    for page_number in range(1, 4):
        # 设置要请求的网页链接
        menu_url = 'http://www.boohee.com/food/group/{}?page={}'.format(type_number, page_number)
        # 请求网页 (设置 headers 部分可先记为固定格式，暂时不用理解)
        food_list_res = requests.get(menu_url, headers = headers)
        # 解析请求到的网页内容
        bs = BeautifulSoup(food_list_res.text, 'html.parser')
        # 提取食物类别
        food_type = bs.find('div', class_='widget-food-list pull-right').find('h3').text.strip()
        # 搜索网页中所有包含食物信息的 Tag
        food_list = bs.find_all('div', class_='text-box pull-left')

        # 使用 for 循环遍历搜索结果
        for food in food_list:
            # 提取食物名
            food_name = food.find('a')['title']
            # 提取食物热量
            food_calorie = food.find('p').text[3:]
            # 提取食物链接
            food_href = 'http://www.boohee.com/{}'.format(food.find('a')['href'])

            # 将信息添加到字典中
            food_dict = {
                '食物类别': food_type,
                '食物名': food_name,
                '食物热量': food_calorie,
                '食物链接': food_href
            }

            # 将每种食物的信息添加至列表中
            data_list.append(food_dict)
            # 打印食物的信息
            print(food_dict)

# 新建 csv 文件，用以存储食物信息
with open('foods.csv', 'w', encoding='utf-8-sig') as f:
    # 将文件对象转换成 DictWriter 对象
    f_csv = csv.DictWriter(f, fieldnames=['食物类别', '食物名', '食物热量', '食物链接'])
    # 写入表头与数据
    f_csv.writeheader()
    f_csv.writerows(data_list)
