from selenium import webdriver

# 初始化谷歌浏览器驱动
driver = webdriver.Chrome()
# 打开网页
driver.get('http://music.facode.cn/index.php/Home/Index/login.html')

# 打印网页的源代码
print(driver.page_source)

# 关闭浏览器
driver.quit()
