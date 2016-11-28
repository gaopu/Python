#!/usr/bin/python3
# 百度贴吧签到，需要填充cookie才能使用
from urllib.request import *
import urllib.parse
from time import *
import re

url = "http://tieba.baidu.com/f/like/mylike?v=" + str(int(time() * 1000))
request = Request(url)
# cookie
request.add_header("cookie","")

response = urlopen(request)
html = str(response.read(),'gbk')

# 关注的贴吧html的table部分
tableStr = re.search('<table>.*?</table>',html).group(0)
# 贴吧的所有url
urls = re.findall('href="(/f\?kw.*?)"',tableStr)

# # 遍历百度贴吧，发送签到请求
for url in urls:
	tiebaName = urllib.parse.unquote(re.search('kw=(.*)',url).group(1),encoding = 'gbk')
	print(tiebaName)
	url = 'http://tieba.baidu.com' + url
	print(url)
	
	# 获取post需要的tbs参数
	thisHtml = str(urlopen(Request(url)).read(),'utf-8')
	tbs = re.search("tbs': \"(.*?)\"",thisHtml).group(1)
	print('tbs:' +tbs)

	data = {
		'ie':'utf-8',
		'kw':tiebaName,
		'tbs':tbs
	}
	request = Request('http://tieba.baidu.com/sign/add',data = urllib.parse.urlencode(data).encode(),method = 'POST')
	print('POST的数据:' + urllib.parse.urlencode(data))
	# cookie
	request.add_header("cookie","")
	response = urlopen(request)
	print('statusCode:' + str(response.status))
	print()
