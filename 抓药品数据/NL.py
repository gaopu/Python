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
# 获取title的正则表达式
titleRegex = re.compile(r"(?s)<title>(.*?)_")
# 获取自然语言的正则表达式（中间会有<br>，在最后写入文件之前去掉）
NLRegex = re.compile(r'(?s)<div class="pt15 f14 graydeep\s*pl20 pr20">(.*?)</div>')
# 获取大概的问题，里面会有html标签
generalQuestionRegex = re.compile(r'(?s)<div class="graydeep User_quecol pt10 mt10" id="qdetailc"(.*?)/div>')
# 获取大概的问题中的文字，去除html标签
accurateQuestionRegex = re.compile(r'(?s)>(.*?)<')
# 删除字符串中的空白字符
deleteSpaceRegex = re.compile(r'\s')
# 删除<br>
deleteBrRegex = re.compile(r'<br>')

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
	# 获取大概的问题，里面会有html标签
	generalQuestion = generalQuestionRegex.search(html)
	
	# 没有找到title就退出
	if title == None:
		# 关闭请求
		request.close()
		# 减少一个线程
		thirdCount -= 1
		return
	# 如果是404页面就退出
	if title.group(1).decode("gbk") == u"404页面":
		# 关闭请求
		request.close()
		# 减少一个线程
		thirdCount -= 1
		return
	print "url: " + pageUrl + " title:" + title.group(1).decode("gbk")
	
	# 获取大概的问题中的文字，去除html标签
	accurateQuestion = accurateQuestionRegex.findall(generalQuestion.group(1))

	# 如果有人说的话
	if NL:
		# 打开文件
		NLFile = open('/home/geekgao/data/' + repr(time.time()),'w')
		# 写入文件的结果字符串（问题和回答）
		result = ''
		for x in accurateQuestion:
			result += x
		for x in NL:
			result += x
		# 删除空白字符
		result = deleteSpaceRegex.sub('',result)
		# 删除<br>
		result = deleteBrRegex.sub('',result)
		
		NLFile.write(result.decode("gbk").encode("utf-8"))
		# 关闭文件
		NLFile.close()
	# 关闭请求
	request.close()
	# 减少一个线程
	thirdCount -= 1
	


startTime = time.time()
while i < 100000:
	num = i
	# 线程要始终保持在50个
	if thirdCount < 50:
		print '【新进程】:' + str(num) + "loopThird" + "进程总数:" + str(thirdCount)
		t = threading.Thread(target = loop, name = str(num) + "loopThird")
		t.start()
	time.sleep(0.001)

thisStartTime = time.time()
while thirdCount != 0:
	# 等待超时就退出（有时候线程并不能全部退出，看资源管理器，说“等候频道 poll_scheme_time”）
	if time.time() - thisStartTime > 10:
		print "等待时间到,强行退出."
		break
	print "等待线程全部结束！还有" + str(thirdCount) + "个线程在工作"
	time.sleep(0.010)
endTime = time.time()

allTime = endTime - startTime
print "完成!花费时间:" + str(allTime) + "s"