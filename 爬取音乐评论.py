import csv
import requests
from bs4 import BeautifulSoup

# 设置歌曲详情页请求链接
page_url = 'https://music.facode.cn/index.php/Home/Index/voice_details/id/403778'
# 设置评论区请求链接
comment_url = 'https://music.facode.cn/index.php/Home/Index/pl_list.html'

# 发起请求，获取网页内容
show_res = requests.get(page_url)
# 解析数据
soup = BeautifulSoup(show_res.text, 'html.parser')
# 提取评论总数所在的标签
comment_tag = soup.find('span', class_='c_tx_thin part__tit_desc')
# 提取评论总数
comment_num = int(comment_tag.text[1:-3])

# 评论总数除以 10，取商并赋值给页数
page_num = comment_num // 10

# 如果评论总数除以 10，余数不为零，则页数 +1
if comment_num % 10 != 0:
    page_num += 1    

# 设置列表，用以存储每条评论的信息
data_list = []

# 循环评论总页数的次数，从第 1 页开始
for page in range(1, page_num + 1):

    # 设置表单提交数据
    data = {
    'voice_id': '403778',
        'info': 2,
        'page': page

    }
    
    # 发起请求，获取网页内容
    comment_res = requests.post(comment_url, data=data)

    # 将 JSON 格式的文本转换为字典
    json_data = comment_res.json()

    # 循环获取每一条评论信息
    for comment in json_data['data']:
        # 将评论的信息添加到字典中
        comment_dict = {
            '用户名':comment['user_name'],
            '评论时间':comment['time'],
            '评论内容':comment['content']
        }
        print(comment_dict)

        # 存储每条评论的信息
        data_list.append(comment_dict)

# 新建 csv 文件，用以存储评论的信息
with open('所有评论.csv', 'w', encoding='utf-8-sig') as f:
    # 将文件对象转换成 DictWriter 对象
    f_csv = csv.DictWriter(f,fieldnames=['用户名', '评论时间', '评论内容'])
    # 写入表头与数据
    f_csv.writeheader()
    f_csv.writerows(data_list)