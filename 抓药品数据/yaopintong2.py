# coding=utf-8
# 抓取药品通网站的数据,这里的链接是经yaopintong.py过滤后确实可用的链接
import urllib
import re
import threading
import time
import socket

# 设置这么长时间超时
socket.setdefaulttimeout(8)

# 进程计数，存储文件计数
i = 0
# 存储线程的个数
thirdCount = 0
# 匹配药品名称
medicamentNameRegex = re.compile(u'(?s)通用名称：(.*?)<')
# 匹配适应症状
symptomRegex = re.compile(u'(?s)适应症：.*?<p>(.*?)<')
# 匹配公司名称
companyNameRegex = re.compile(u'(?s)企业名称：.*?<p>(.*?)<')
# 匹配公司地址
companyAddressRegex = re .compile(u'(?s)生产地址：.*?<p>(.*?)<')
# 电话
phoneNumRegex = re.compile(u'(?s)联系电话：.*?<p>(.*?)<')

# 处理抓取任务
def loop(pageUrl):
	global i,thirdCount,medicamentNameRegex,symptomRegex,companyAddressRegex,companyNameRegex
	i += 1
	# 文件名用数字
	fNum = i;
	# 表示新线程启动了
	thirdCount += 1
	
	try:
		request = urllib.urlopen(pageUrl)
	except Exception, e:
		# 减少一个线程
		thirdCount -= 1
		return
	
	try:
		# 获得网页源码
		html = request.read().decode('gbk')
	except Exception, e:
		# 关闭请求
		request.close()
		# 减少一个线程
		thirdCount -= 1
		return

	# 正则匹配需要的数据
	medicamentName = medicamentNameRegex.search(html)
	symptom = symptomRegex.search(html)
	companyName = companyNameRegex.search(html)
	companyAddress = companyAddressRegex.search(html)
	phoneNum = phoneNumRegex.search(html)
	
	if medicamentName or symptom or companyName or companyAddress or phoneNum:
		f = open('/home/geekgao/data/' + str(fNum),'w')
		if medicamentName:
			f.write(medicamentName.group(1).encode('utf-8') + '\n')
		if symptom:
			f.write(symptom.group(1).encode('utf-8') + '\n')
		if companyName:
			f.write(companyName.group(1).encode('utf-8') + '\n')
		if companyAddress:
			f.write(companyAddress.group(1).encode('utf-8') + '\n')
		if phoneNum:
			f.write(phoneNum.group(1).encode('utf-8') + '\n')
		f.close()
		print pageUrl + '抓取成功!'
	else:
		print pageUrl + '抓取失败!'
	
	# 关闭请求
	request.close()
	# 减少一个线程
	thirdCount -= 1
	
startTime = time.time()
# 打开存储有需要抓取的网页链接的文件
f = open('/home/geekgao/1','r')
while True:
	num = i + 1
	# 线程要始终保持在50个
	if thirdCount <= 50:
		pageUrl = f.readline()
		# 读完了就退出循环
		if pageUrl == '':
			break
		print '【新进程】:' + str(num) + "loopThird" + "进程总数:" + str(thirdCount)
		t = threading.Thread(target = loop, name = str(num) + " loopThird",args=(pageUrl,))
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
f.close()
print "完成!花费时间:" + str(allTime) + "s"