# coding:utf-8
import requests
from urllib import urlencode
import re
import xmltodict
import json
import datetime
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

'''
由于使用了第三方模块
请先执行 pip install xmltodict
'''

'''
函数说明：同品种一个或多个城市走势图
参数说明：
startTime 起始日
endTime 截止日
catalog 品种
spec 规格/材质
citys 城市（名字用英文逗号隔开）
调用样例：getChartMultiCity("2016-02-04", "2016-04-04", "螺纹钢_:_螺纹钢", "HRB400 20MM_:_HRB400_20MM", "上海,杭州")
'''


def getChartMultiCity(startTime, endTime, catalog, spec, citys):
    startTime = unicode(startTime, 'utf-8').encode('gb2312')
    endTime = unicode(endTime, 'utf-8').encode('gb2312')
    ucatalog = unicode(catalog, 'utf-8').encode('gb2312')
    uspec = unicode(spec, 'utf-8').encode('gb2312')
    cityArray = citys.split(',')
    suffix = ''
    if len(cityArray) > 1:
        # print(len(cityArray))
        for index in range(1, len(cityArray)):
            city = cityArray[index]
            city = unicode(city, 'utf-8').encode('gb2312')
            arg = {'citys': city}
            q = urlencode(arg)
            suffix = suffix + '&' + q

    city = unicode(cityArray[0], 'utf-8').encode('gb2312')
    submit1 = unicode(" 搜　索 ", 'utf-8').encode('gb2312')
    args = {'startTime': startTime,
            'endTime': endTime,
            'catalog': ucatalog,
            'spec': uspec,
            'citys': city,
            'submit1': submit1}
    q = urlencode(args)
    url = "http://index.glinfo.com/price/getChartMultiCity.ms" + '?' + q + suffix
    # print(url)
    r = requests.get(url)
    m = re.search('so.addVariable\("chart_data", "(?P<data>.*?)"\);', r.text)
    data = m.group("data")
    dictData = xmltodict.parse(data)
    # print(dictData['chart']['series']['value'])  # 日期
    # print(dictData['chart']['graphs']['graph'][0]['@title'])  # 上海
    # print(len(dictData['chart']['graphs']['graph'][0]['value']))  # 上海数据

    citys = dictData['chart']['graphs']['graph']
    date = dictData['chart']['series']['value']

    fileName = str(int(time.time())) + '.csv'
    fileName = '../data/steel/' + fileName
    print(fileName)
    with open(fileName, 'a+') as f:
        title = catalog + ',' + spec + ',' + startTime + ',' + endTime
        f.write(title)
        f.write('\n')
        for city in citys:
            for index in range(len(date)):
                s = date[index]['#text'] + ',' + city['value'][index]['#text'] + ',' + city['@title']
                # print(s)
                f.write(str(s))
                f.write('\n')
                # f.write(json.dumps(xmltodict.parse(data)))
                # f.write('\n')

                # print(m.group("data"))  # catalog spec 可有多个


'''
函数说明：同城市一个或多个品种走势图
参数说明：
startTime 起始日
endTime 截止日
city 城市
catalogs 品种（多个品种中间用英文逗号隔开）
specs 规格/材质（多个规格/材质中间用英文逗号隔开）
调用样例：getChartMultiCatalog("2016-02-04", "2016-04-04", "上海", "螺纹钢_:_螺纹钢,线材_:_线材", "螺纹钢_:_螺纹钢:__:HRB400 20MM_:_HRB400_20MM,螺纹钢_:_螺纹钢:__:HRB335 20MM_:_HRB335_20MM,线材_:_线材:__:6.5高线HPB300_:_HPB300_6.5高线,线材_:_线材:__:8.0高线HPB300_:_HPB300_8.0高线")
'''


def getChartMultiCatalog(startTime, endTime, city, catalogs, specs):
    sChannel = '01'
    startTime = unicode(startTime, 'utf-8').encode('gb2312')
    endTime = unicode(endTime, 'utf-8').encode('gb2312')
    ucity = unicode(city, 'utf-8').encode('gb2312')
    catalogArray = catalogs.split(',')
    suffix = ''
    if len(catalogArray) > 1:
        # print(len(catalogArray))
        for index in range(1, len(catalogArray)):
            catalog = catalogArray[index]
            catalog = unicode(catalog, 'utf-8').encode('gb2312')
            arg = {'catalogs': catalog}
            q = urlencode(arg)
            suffix = suffix + '&' + q
    specArray = specs.split(',')
    if len(specArray) > 1:
        # print(len(specArray))
        for index in range(1, len(specArray)):
            spec = specArray[index]
            spec = unicode(spec, 'utf-8').encode('gb2312')
            arg = {'specs': spec}
            q = urlencode(arg)
            suffix = suffix + '&' + q

    catalogs = unicode(catalogArray[0], 'utf-8').encode('gb2312')
    specs = unicode(specArray[0], 'utf-8').encode('gb2312')
    submit1 = unicode(" 搜　索 ", 'utf-8').encode('gb2312')
    args = {
        'sChannel': sChannel,
        'startTime': startTime,
        'endTime': endTime,
        'city': ucity,
        'catalogs': catalogs,
        'specs': specs,
        'submit1': submit1
    }
    q = urlencode(args)
    url = "http://index.glinfo.com/price/getChartMultiCatalog.ms" + '?' + q + suffix
    r = requests.get(url)
    # print(r.url)
    # print(r.text)
    m = re.search('so.addVariable\("chart_data", "(?P<data>.*?)"\);', r.text)
    data = m.group("data")
    # print(data)
    # print(data)
    dictData = xmltodict.parse(data)
    date = dictData['chart']['series']['value']  # 日期
    specs = dictData['chart']['graphs']['graph']

    # print(len(date))
    # print(dictData)
    # jsonData = json.dumps(dictData)

    fileName = '../data/steel/'+str(int(time.time())) + '.csv'
    with open(fileName, 'a+') as f:
        title = city + ',' + startTime + ',' + endTime
        f.write(title)
        f.write('\n')
        for spec in specs:
            for index in range(len(date)):
                s = date[index]['#text'] + ',' + spec['value'][index]['#text'] + ',' + spec['@title']
                # print(s)
                f.write(str(s))
                f.write('\n')
                # f.write(jsonData)
                # f.write('\n')


# 螺纹钢_:_螺纹钢, HRB400 20MM_:_HRB400_20MM, 上海  搜　索
# 螺纹钢_:_螺纹钢:__:HRB335 20MM_:_HRB335_20MM
# 线材_:_线材
# 线材_:_线材:__:6.5高线HPB300_:_HPB300_6.5高线
# 线材_:_线材:__:8.0高线HPB300_:_HPB300_8.0高线

if __name__ == '__main__':
    getChartMultiCity("2016-02-04", "2016-04-04", "螺纹钢_:_螺纹钢", "HRB400 20MM_:_HRB400_20MM", "上海,杭州")

    # getChartMultiCatalog("2016-02-04", "2016-04-04", "上海", "螺纹钢_:_螺纹钢,线材_:_线材","螺纹钢_:_螺纹钢:__:HRB400 20MM_:_HRB400_20MM,螺纹钢_:_螺纹钢:__:HRB335 20MM_:_HRB335_20MM,线材_:_线材:__:6.5高线HPB300_:_HPB300_6.5高线,线材_:_线材:__:8.0高线HPB300_:_HPB300_8.0高线")
