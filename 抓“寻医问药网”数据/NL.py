#coding=utf-8
import urllib
import re
import threading
import time
import socket

# 设置这么长时间超时
socket.setdefaulttimeout(10)

# 抓网页的地址数字
i = 0
# 存储线程的个数
thirdCount = 0
# 获取title的正则表达式，编译一下，提高性能
titleRegex = re.compile(r"<title>(.*?)</title>")
# 获取自然语言的正则表达式，编译一下，提高性能
NLRegex = re.compile(r'<div class="pt15 f14 graydeep  pl20 pr20">(.*?)<')

# 处理抓取任务
def loop():
	global i,thirdCount,titleRegex,NLRegex
	i += 1
	# 表示新线程启动了
	thirdCount += 1
	
	pageUrl = "http://club.xywy.com/static/1/" + str(i) + ".htm"
	try:
		request = urllib.urlopen(pageUrl)
	except Exception, e:
		# 减少一个线程
		thirdCount -= 1
		return
	
	try:
		# 获得网页源码
		html = request.read()
	except Exception, e:
		# 关闭请求
		request.close()
		# 减少一个线程
		thirdCount -= 1
		return
		
	# 获取title
	title = titleRegex.search(html)
	# 获取自然语言
	NL = NLRegex.findall(html)
	
	# 没有找到title就退出
	if title == None:
		# 关闭请求
		request.close()
		# 减少一个线程
		thirdCount -= 1
		return
	# 如果是404页面就退出
	if title.group(1).decode("gbk") == u"404页面_":
		# 关闭请求
		request.close()
		# 减少一个线程
		thirdCount -= 1
		return
	print "url: " + pageUrl + " title:" + title.group(1).decode("gbk")
	# 如果有人说的话
	if NL:
		for l in NL:
			NLFile.write(l.decode("gbk").encode("utf-8"))
	# 关闭请求
	request.close()
	# 减少一个线程
	thirdCount -= 1
	
NLFile = open('/home/geekgao/NL1','w')

startTime = time.time()
while i < 500:
	num = i
	# 线程要始终保持在50个
	if thirdCount < 50:
		print '【新进程】:' + str(num) + "loopThird" + "进程总数:" + str(thirdCount)
		t = threading.Thread(target = loop, name = str(num) + "loopThird")
		t.start()
	time.sleep(0.001)

while thirdCount != 0:
	time.sleep(0.001)
endTime = time.time()

allTime = endTime - startTime

NLFile.close()
print "完成!花费时间:" + str(allTime) + "s"