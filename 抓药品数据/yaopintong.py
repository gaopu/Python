# coding=utf-8
# 抓取药品通的网站需要的数据，这个代码是检查哪些网页不是404.存储起来，在yaopintong2.py中进行抓取
import urllib
import re
import threading
import time
import socket

# 设置这么长时间超时
socket.setdefaulttimeout(8)

# 抓网页的地址起始数字
i = 800000
# 存储线程的个数
thirdCount = 0

# 处理抓取任务
def loop():
	global i,thirdCount,titleRegex,NLRegex
	i += 1
	# 当前网页的编号
	pageNum = i
	# 表示新线程启动了
	thirdCount += 1
	
	pageUrl = "http://wapypk.39.net/manual/" + str(pageNum)
	try:
		request = urllib.urlopen(pageUrl)
	except Exception, e:
		# 减少一个线程
		thirdCount -= 1
		return
	
	# 不正常就退出
	if request.getcode() != 200:
		print "不正常的页面:" + str(pageNum) + " 返回值:" + str(request.getcode())
		# 关闭请求
		request.close()
		# 减少一个线程
		thirdCount -= 1
		return
	print "正常的页面:" + str(pageNum)
	
	f.write(pageUrl + '\n')
	# 关闭请求
	request.close()
	# 减少一个线程
	thirdCount -= 1
	
startTime = time.time()
f = open('/home/geekgao/1','a+')
while i < 830000:
	num = i + 1
	# 线程要始终保持在50个
	if thirdCount < 50:
		print '【新进程】:' + str(num) + "loopThird" + "进程总数:" + str(thirdCount)
		t = threading.Thread(target = loop, name = str(num) + "loopThird")
		t.start()
	time.sleep(0.001)

thisStartTime = time.time()
while thirdCount != 0:
	# 等待超时就退出（没有这个有时候线程并不能全部退出，看资源管理器，说“等候频道 poll_scheme_time”）
	if time.time() - thisStartTime > 10:
		print "等待时间到,强行退出."
		break
	print "等待线程全部结束！还有" + str(thirdCount) + "个线程在工作"
	time.sleep(0.010)
endTime = time.time()

allTime = endTime - startTime
f.close()
print "完成!花费时间:" + str(allTime) + "s"