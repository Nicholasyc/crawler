# coding=utf-8
import sys
import requests
import re
import xmltodict

reload(sys)
sys.setdefaultencoding('utf8')

'''
函数说明：获取中国船舶价格交易指数 SSPI chart
参数说明：
shiptype 船舶类型
fromyear 起始年
frommonth 起始月
toyear 截至年
tomonth 截至月
调用样例：getSSPIChartData("Total", 2006, 1, 2016, 12)
'''
def getSSPIChartData(shiptype, fromyear, frommonth, toyear, tomonth):
    url = "http://sspi.csi.com.cn/QXTNew.aspx"
    callData = "{shiptype:"+shiptype+",fromyear:"+str(fromyear)+",frommonth:"+str(frommonth)+",toyear:"+str(toyear)+",tomonth:"+str(tomonth)+"}"
    # print(callData)
    # {shiptype:"Total",fromyear:"2006",frommonth:"1",toyear:"2016",tomonth:"12"}
    payload = {
        'EgAjaxName': 'getdatadiv',
        'EgAjaxCallData': callData,
        'EgUserControl': 'false',
        'timestemp': 1478862456669
    }
    r = requests.post(url, data=payload)
    # print(r.text)
    predata = r.text.split("|")
    prefix = predata[0]
    title = predata[1]
    titleDate = title.split("：")[0]
    spanData = title.split("：")[1]
    m = re.search('>(?P<data>.*?)<', spanData)
    titleValue = m.group("data")
    # 输出文件的第一行
    title = prefix + " " + titleDate + " " + titleValue
    # print(title)

    xmlData = predata[2]
    dictData = xmltodict.parse(xmlData)
    date = dictData['chart']['series']['value']
    # print(date)
    index = dictData['chart']['graphs']['graph']['value']
    # print(index)
    fileName = '../data/sspichart/'+prefix+'.csv'
    print(fileName)
    with open(fileName, 'w+') as f:
        f.write(title)
        f.write('\n')
        size = len(date)
        for i in range(size):
            content = date[i]['#text'] + "," + index[i]['#text']
            f.write(content)
            f.write('\n')

    # print(dictData)
#  shiptype:"Total",fromyear:"2006",frommonth:"1",toyear:"2016",tomonth:"12"
if __name__=='__main__':
    getSSPIChartData("Total", 2006, 1, 2016, 12)
