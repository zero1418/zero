# 导入相关库
import re
import requests

# 获取歌手名称
singer = input('请输入歌手名称：')

# 设置请求链接、请求头、请求数据
search_url = 'https://music.facode.cn//index.php/Home/Index/search_list.html'
header = {'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22180974f244f270-00b8980866d922-49647e56-1327104-180974f24507ed%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.pypypy.cn%2F%22%7D%2C%22%24device_id%22%3A%22180974f244f270-00b8980866d922-49647e56-1327104-180974f24507ed%22%7D; PHPSESSID=60j1acsmvl7tmelgfit95t80op; SERVERID=ea05d8f0df0b500b16ea77d14ece1d58|1659588540|1659588528'}
data = {
    'value': singer,
    'info': 1,
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

    # 提取并写入歌词
    for song in search_json['voice']:
        # 拼接文件名
        filename = '{}-{}'.format(song['name'], song['author'].replace('/', ''))

        # 请求歌词数据
        lyrics_res = requests.post('https://music.facode.cn/index.php/Home/Index/lyrics.html', data={'id': song['id']},headers=header)
        lyrics_json = lyrics_res.json()

        # 如果不存在歌词，则跳过
        if lyrics_json['data'] == '暂无歌词':
            print(filename + ' 没有歌词')
            continue

        # 用 re.sub() 函数处理歌词信息
        match_result = re.sub('\[.*?]', '', lyrics_json['data'])

        # 将歌词写入文本文档中
        with open(filename + '.txt', 'w') as f:
            f.write(match_result)

        # 打印已写入歌曲信息
        print(filename + ' 歌词的提取写入已完成')