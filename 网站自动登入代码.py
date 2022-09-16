import pytesseract
from selenium import webdriver
import time

# 获取手机号码及密码
phone = input('请输入手机号码：')
password = input('请输入密码：')

# 初始化谷歌浏览器驱动
driver = webdriver.Chrome()
# 打开网页
driver.get('https://music.facode.cn/index.php/Home/Index/login.html')

# 定位到手机号码输入框的标签，并输入手机号码
user_tag = driver.find_element_by_name('phone')
user_tag.send_keys(phone)
# 使程序暂停 1 秒
time.sleep(1)

# 定位到密码输入框的标签，并输入密码
password_tag = driver.find_element_by_name('pass')
password_tag.send_keys(password)
# 使程序暂停 1 秒
time.sleep(1)

# 定位到图片验证码所在的标签
img_tag = driver.find_element_by_id('graph_img')

# 定义保存的截图名
png_path = '../验证码图片.png'

# 将截图下来的图片保存为 “验证码图片.png”
with open(png_path, 'wb') as f:
    f.write(img_tag.screenshot_as_png)

# 识别图片中的内容
code = pytesseract.image_to_string(png_path)

# 去掉多余的符号
code = code.strip()
# 定位到验证码输入框的标签，并输入验证码
code_tag = driver.find_element_by_name('verify')
code_tag.send_keys(code)
# 使程序暂停 1 秒
time.sleep(1)

# 定位到【登录】按钮的标签，并点击【登录】按钮
login_tag = driver.find_element_by_class_name('login-btn')
login_tag.click()
# 使程序暂停 2 秒
time.sleep(5)

# 关闭浏览器
driver.quit()