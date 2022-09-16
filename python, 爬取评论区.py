import csv
from email import parser
import requests
from bs4 import BeautifulSoup

# 设置列表，用以存储每条评论的信息
data_list = {}

# 设置登录网站的请求网址
book_url = 'https://wp.forchange.cn/wp-admin/admin-ajax.php'
# 输入用户的账号密码


# 设置登录请求的请求体数据
login_data = {
    'action': 'ajaxlogin',
    'username': '1752043727',
    'password': 'aa158975589',
    'remember': 'true'
}

# 请求登录网站
denglu_res = requests.post(book_url,data=login_data)

# 设置要请求的书籍网页链接
comment_url = 'https://wp.forchange.cn/psychology/11069/comment-page-1/'
# 携带获取到的 Cookies 信息请求书籍网页
comment_res = requests.get(comment_url, cookies=denglu_res.cookies)
# 解析请求到的书籍网页内容
soup = BeautifulSoup(comment_res.text, 'html.parser')
# 搜索网页中所有包含评论的 Tag
comment_list = soup.find('div', class_='comment-txt')

# 使用 for 循环遍历搜索结果
for comment in comment_list:
    # 提取用户名
    comment_yhm = comment.find('cite', class_= 'fn').text[:-2]
    # 提取评论时间
    comment_time = comment.find('p', class_= 'date').text
    # 提取评论内容
    comment_nr = comment.find('div', class_= 'bd').find('p').text

    # 将评论的信息添加到字典中
    comment_dict = {
         '用户名': comment_yhm,
         '评论时间': comment_time,
         '评论内容': comment_nr
     }
    # 打印评论的信息
    print(comment_dict)
    # 存储每条评论的信息
    data_list.append(comment_dict)

# 新建 csv 文件，用以存储评论的信息
with open ('book,csv', 'w', encoding='utf-8-sig') as f:
    # 将文件对象转换成 DictWriter 对象
    f_csv = csv.DictWriter(f,fieldnames=['用户名', '评论时间', '评论内容'])
    # 写入表头与数据
    f_csv.writeheader()
    f_csv.writerows(data_list)