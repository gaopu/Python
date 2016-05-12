#! /usr/bin/python
#coding:utf-8

import urllib2,re

request = urllib2.Request('http://192.168.1.1/userRpm/SystemStatisticRpm.htm?contType=1&sortType=4&autoRefresh=2&Num_per_page=100&Goto_page=1')
request.add_header('Cookie','Authorization=Basic%20YWRtaW46aHVxaWFuZ3hp; ChgPwdSubTag=')
request.add_header('Referer','http://192.168.1.1/userRpm/SystemStatisticRpm.htm?contType=1&sortType=4&Num_per_page=100&Goto_page=1')
request.add_header('Upgrade-Insecure-Requests','1')
request.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36')

htmlCode = urllib2.urlopen(request).read()
resultStr = re.search(r'(?s)new Array\(\n(.*?)\n0,0 \);',htmlCode).group(1)

# 字符串数组，每一项是一项主机记录
computers = re.findall(r'(?m)^(.*?)$',resultStr)
# 分别输出没一行记录
i = 0
for c in computers:
	# 计数
	i += 1
	print ('%3d:'%i),
	
	# ip
	ip = c.split('"')[1].split('"')[0]
	print ip + '  ',
	# front代表紧接着的下次分割时的字符串
	front = ip + '","'
	
	# mac
	mac = c.split(front)[1].split('"')[0]
	print mac + '  ',
	front = front + mac + '",'
	
	# 上传量(B)
	upSize = c.split(front)[1].split(',')[0]
	print ("[↓%8.2fMB "%(float(upSize) / 1024 / 1024)),
	front = front + upSize + ','
	
	# 下载量(B)
	downSize = c.split(front)[1].split(',')[0]
	print ("↑%8.2fMB]\t"%(float(downSize) / 1024 / 1024)),
	front = front + downSize + ','
	
	# 上传速度(B/s)
	up = c.split(front)[1].split(',')[0]
	print ("[↓%8.2fKB/s "%(float(up) / 1024)),
	front = front + up + ','
	
	# 上传速度(B/s)
	down = c.split(front)[1].split(',')[0]
	print ("↑%8.2fKB/s]\t"%(float(down) / 1024))