import re
import requests
import pytesseract
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 获取手机号码及密码
phone = input('请输入手机号码：')
password = input('请输入密码：')
# 获取歌手名称
singer_name = input('请输入歌手名称：')

# 设置静默模式
opts = Options()
opts.headless = True

# 初始化谷歌浏览器驱动
driver = webdriver.Chrome(options=opts)
# 打开网页
driver.get('https://music.facode.cn/index.php/Home/Index/login.html')

# 定位到手机号码输入框的标签，并输入手机号码
user_tag = driver.find_element_by_name('phone')
user_tag.send_keys(phone)
# 定位到密码输入框的标签，并输入密码
password_tag = driver.find_element_by_name('pass')
password_tag.send_keys(password)

# 定位到图片验证码所在的标签
img_tag = driver.find_element_by_id('graph_img')

# 定义保存的截图名
png_path = '../验证码图片.png'

# 将截图下来的图片保存为 【验证码图片.png】
with open(png_path, 'wb') as f:
    f.write(img_tag.screenshot_as_png)

# 识别图片中的内容
code = pytesseract.image_to_string(png_path)

# 去掉多余的符号
code = code.strip()
# 定位到验证码输入框的标签，并输入验证码
code_tag = driver.find_element_by_name('verify')
code_tag.send_keys(code)

# 定位到【登录】按钮的标签，并点击【登录】按钮
login_tag = driver.find_element_by_class_name('login-btn')
login_tag.click()

# 获取 cookie 列表
cookie_list = driver.get_cookies()

# 创建储存 cookie 的空字符
cookies = ''

# 遍历 cookie 列表，取出目标 cookie 信息
for cookie in cookie_list:
    cookies += '{}={};'.format(cookie['name'], cookie['value'])

# 设置请求头
header = {'Cookie': cookies}

# 关闭浏览器
driver.quit()

# 设置请求链接、请求头、请求数据
search_url = 'https://music.facode.cn//index.php/Home/Index/search_list.html'

data = {
    'value': singer_name,
    'info': '1',
    'page': 1,
}

# 获取响应数据
search_res = requests.post(search_url, data=data, headers=header)
search_json = search_res.json()

# 获取搜索总结果数
result_num = int(search_json['totalnum'])

# 计算总页数
page_num = result_num // 12
if result_num % 12 != 0:
    page_num += 1

# 循环总页数的次数，从第2页开始
for page in range(1, page_num + 1):
    # 修改请求数据字典中的页数
    data['page'] = page
    print('开始爬取第{}页....'.format(page))

    # 获取响应数据
    search_res = requests.post(search_url, data=data, headers=header)
    search_json = search_res.json()

    # 遍历歌曲数据
    for song in search_json['voice']:
        # 拼接文件名
        filename = '{}-{}'.format(song['name'], song['author'].replace('/', ''))

        # 请求歌词数据
        lyrics_res = requests.post('https://music.facode.cn//index.php/Home/Index/lyrics.html', data={'id': song['id']}, headers=header)
        lyrics_json = lyrics_res.json()

        # 如果不存在歌词，则跳过
        if lyrics_json['data'] is None:
            print(filename + ' 没有歌词')
            continue

        match_result = re.sub('\[.*?]', '', lyrics_json['data'])

        # 将歌词写入文本文档中
        with open('../歌词/' + filename + '.txt', 'w') as f:
            f.write(match_result)

        # 打印已写入歌曲信息
        print(filename + ' 歌词的提取写入已完成')