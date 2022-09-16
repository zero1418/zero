import os
import requests

# 设置文件夹路径
path = '../图片'

# 判断【图片】文件夹是否存在
if not os.path.exists(path):
    # 不存在则创建文件夹
    os.mkdir(path)

# 设置搜索关键词
keyword = input('请输入搜索关键词：')

# 设定图片序号初始值
num = 1

# 设置爬取页数，并执行循环
for page_num in range(1, 4):
    # 打印开始爬取的页数
    print('开始爬取第 {} 页...'.format(page_num))
    
    # 设置批量爬取的请求链接
    url = 'https://unsplash.com/napi/search/photos?query={}&per_page=20&page={}&xp='.format(
        keyword, page_num)
    # 发起请求，获取网页内容
    res = requests.get(url)
    # 将 JSON 格式的文本转换为字典
    json_data = res.json()

    # 遍历图片数据
    for pic_info in json_data['results']:
        # 设置图片名称
        image_name = '{}_{}'.format(keyword, num)
        # 获取图片链接
        pic_url_small = pic_info['urls']['small']
        # 获取图片响应内容
        pic_res = requests.get(pic_url_small)

        # 将图片保存到【图片】文件夹
        with open('{}/{}.jpg'.format(path, image_name), 'wb') as f:
            f.write(pic_res.content)

        # 打印图片爬取信息
        print('{}.jpg 已完成爬取'.format(image_name))
        # 每爬取一张图片，序号加 1
        num += 1

    # 打印已爬取的页面数
    print('第 {} 页图片信息已爬取完成'.format(page_num))