import requests
from bs4 import BeautifulSoup

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
comment_url = 'https://wp.forchange.cn/psychology/8384/'
# 携带获取到的 Cookies 信息请求书籍网页
comment_res = requests.get(comment_url, cookies=login_res.cookies)
# 解析请求到的书籍网页内容
soup = BeautifulSoup(comment_res.text, 'html.parser')

# 提取书籍名称
book_name = soup.find('h1', class_='title-detail').text

# 搜索网页中包含评分信息的 Tag
score_data = soup.find('div', id='curItemTotalStar')

# 提取书籍评分
score = score_data.find('b').text
# 提取评分人数
score_number = score_data.find('p', class_='wk').text[7:-5]

# 将书籍的各项信息存入到字典 book_data
book_data = {
    '书籍名称': book_name,
    '书籍评分': score,
    '评分人数': score_number
}
# 打印书籍的信息
print(book_data)