import requests
from bs4 import BeautifulSoup
from collections import Counter
import openpyxl
import matplotlib.pyplot as plt


def get_html_text(url):
    try:
        h = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/68.0.3440.106 Safari/537.36'
             }
        r = requests.get(url, headers=h, timeout=3000)
        r.raise_for_status()   # 如果不是200，则引发HTTPError异常
        r.encoding = r.apparent_encoding  # 根据内容去确定编码格式
        return r.text
    except BaseException as e:
        print("出现异常：", e)
        return str(e)


def writefile(file_name, content_str):  # 将数据写入文件
    with open(file_name, "w", encoding='utf-8', ) as f:
        f.write(content_str)
        f.close


def write_excel(file_name, list_content):
    wb = openpyxl.Workbook()  # 新建Excel工作簿
    st = wb.active
    st['A1'] = "西游记第一章每个字统计" # 修改为自己的标题
    second_row = ["字符", "出现次数"] # 根据实际情况写属性
    st.append(second_row)
    st.merge_cells("A1:B1")  # 根据实际情况合并标题单元格
    for key, value in list_content:
        new = [key,value]
        st.append(new)
    wb.save(file_name)  # 新工作簿的名称


def show_pie(content):
    x = []
    y = []
    for i in content:
        x.append(i[0])
        y.append(int(i[1]))
    plt.rcParams['font.sans-serif'] = ['KaiTi']
    fig1, ax1 = plt.subplots()
    ax1.pie(y, labels=x, autopct='%.1f%%')
    # autopct 数据格式  %%打印%
    ax1.axis('equal')
    plt.savefig('count.png')
    plt.show()


url = 'http://www.qushuba.com/shu17601/9771853.html'  # 需要爬虫的网址
html_text = get_html_text(url)   # 获得网页响应
writefile("data_html.txt", html_text)  # 源码写入文件
soup = BeautifulSoup(html_text, 'html.parser')  # 解析源码
contents = soup.find(id='content').text  # 获得小说文本
counter = Counter(contents).most_common(10)  # 技术
all_str = ''
for k in counter:
    all_str += k[0]+','+str(k[1])+'\n'
write_excel('count.xlsx', counter)  # 数据写入excel
writefile('count.csv', all_str)
show_pie(counter)
print(counter)

