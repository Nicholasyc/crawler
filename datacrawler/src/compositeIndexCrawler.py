# coding=utf-8
import sys
import requests
import re
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

'''
由于引用了第三方模块，请先 pip install beautifulsoup4
'''
'''
函数说明：月度综合指数表
参数说明：page 总共爬取页数 默认为10页
数据较多，需要运行一小段时间，请耐心等候
'''

def getCompositeIndexData(page=10):
    fileName = '../data/compositeindex/compositedata.csv'
    with open(fileName, 'w+') as f:
        for i in range(1, int(page)+1):
            url = "http://sspi.csi.com.cn/ydzhzsb_" + str(i) + ".html"
            r = requests.get(url)
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.table
            if i == 1:
                thead = table.thead
                trArray = thead.find_all('tr')
                td1Array = trArray[0].find_all('td')
                headtime = td1Array[0].text.strip()
                # headqishu = td1Array[1].text.strip()
                headzonghe = td1Array[2].text.strip()
                # headgansa = td1Array[3].text.strip()
                # headyouchuan = td1Array[4].text.strip()
                # headhuochuan = td1Array[5].text.strip()
                # 文件第一行
                title = headtime + "," + headzonghe
                # print(title)
                f.write(title)
                f.write('\n')

            tbody = table.tbody
            for tr in tbody.find_all('tr'):
                tdarr = tr.find_all('td')
                # print(len(tdarr))
                # print(tdarr)
                time = ""
                zhonghe = ""
                for i in range(len(tdarr) - 1):
                    if i == 0:
                        time = tdarr[i].text
                    elif i==2:
                        zhonghe = tdarr[i].text
                        break
                    # content = content + tdarr[i].text + ","
                # content = content[:-1]
                content = time + "," + zhonghe
                if len(content) != 1:
                    f.write(content)
                    f.write('\n')

if __name__ == '__main__':
    getCompositeIndexData(8)
