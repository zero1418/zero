import requests

# 设置登录网站的请求网址
url_login =  'https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-login.php'

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

# 输入用户的账号密码
username = input('请输入用户名：')
password = input('请输入密码：')

# 设置登录请求的请求体数据
data = {
    'log': username,
    'pwd': password,
    'wp-submit': '登录',
    'redirect_to': 'https://wordpress-edu-3autumn.localprod.oc.forchange.cn',
    'testcookie': '1'
}

# 请求登录网站
login = requests.post(url_login, headers=headers, data=data)

# 打印 Cookies 值
print(login.cookies)

# 步骤三：发送评论
#对cookies进行赋值
cookies = login.cookies
#设置博客内容请求连接
url_comment = 'https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-comments-post.php'
# 设置博客评论页链接中，请求体的表单数据
data_comment = {
    'comment': input('请输入你想要发表的评论：'),
    'submit': '发表评论',
    'comment_post_ID': '13',
    'comment_parent': '0'
}
#提交评论
comment = requests.post(url_comment, headers=headers, data=data_comment, cookies=cookies)
if comment.status_code == 200:
    print('评论发送成功！')
else:
    print('评论发送失败！请求状态码为{}'.format(comment.status_code))