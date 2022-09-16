import re

# 定义数据
birthdays = '''
任仁珠 05-21; 孙宏 01-08; 06-17 邵电克;隗辉 01-07; 杭利 07-10; 08-22 许珍;
雷义元 08-08; 03-26 颛孙金叶;常歌固 05-21; 杨上辰 10-12; 宁信文 06-22; 
09-19 包被超;01-31 宰电云;丁纯 11-25; 庞忠姣 10-26; 05-21 程聪;
'''

# 提取日期
date_list = re.findall('[0-1][0-9]-[0-3][0-9]', birthdays)

# 创建计数字典
count_dict = {}
# 遍历日期
for date in date_list:

    # 判断日期是否在字典中，不存在则将日期写入字典，并将值设置为1
    #可以采用 if count_dict.get(date) == None: 语句来判断数据是否在字典中：
   # a. 当不存在时，就需要创建这个键，值为1，即 字典['日期'] = 1；
   # b. 当存在时，直接对这个键的值加1，即 字典['日期'] += 1 。
    if count_dict.get(date) == None:
        count_dict[date] = 1
    # 否则该日期的值加1
    else:
        count_dict[date] += 1

# 打印计数字典
print(count_dict)
