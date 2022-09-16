from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 初始化谷歌浏览器驱动
driver = webdriver.Chrome()
# 打开网页
driver.get('https://music.facode.cn/index.php/Home/Index/login.html')

# 定位到登录的标签，并点击【登录】按钮
login_tag = driver.find_element_by_class_name('login-btn')
login_tag.click()

# 使程序暂停 1 秒
time.sleep(1)

# 关闭浏览器
driver.quit()