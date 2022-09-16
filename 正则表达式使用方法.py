import pdfplumber
import re
import os
import csv

# 创建数据列表
data_list = []

# 遍历指定文件夹中的文件名
dir_path = '../简历/'
for file_name in os.listdir(dir_path):
    # 获取名字
    name = file_name.split('_')[1][:-4]

    # 打开pdf文档
    with pdfplumber.open(dir_path + file_name) as pdf:
        # 提取文档中第一页信息
        text = pdf.pages[0].extract_text()

        # 用 re.search() 提取手机号码
        phone_match = re.search('1[3-9]\d{9}|1[3-9]\d-\d{4}-\d{4}', text)
        # 用 match.group() 返回匹配结果
        phone_num = phone_match.group()

        # 用 re.search() 提取邮箱
        email_match = re.search('\w+@\w+\.\w+', text)
        # 用 match.group() 返回匹配结果
        email = email_match.group()

        # 用 re.search() 提取期望薪资数值
        income_match = re.search('(\d+)元/月', text)
        # 用 match.group() 返回匹配结果
        income = income_match.group(1)

    # 将数据保存到列表中
    data_list.append({
        '姓名': name,
        '手机号码': phone_num,
        '邮箱': email,
        '期望薪资（元/月）': income
    })

# 步骤二 存储数据到 csv 文件中
# 创建并打开csv文件
with open('个人信息.csv', 'w', newline='') as f:
    # 将数据写入csv文件中
    writer = csv.DictWriter(f, fieldnames=['姓名', '手机号码', '邮箱', '期望薪资（元/月）'])
    writer.writeheader()
    writer.writerows(data_list)
