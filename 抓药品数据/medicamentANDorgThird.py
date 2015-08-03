#coding=utf-8
# 最大453482
import urllib
import re
import threading
import time
import socket

# 设置这么长时间超时
socket.setdefaulttimeout(10)

# 抓网页的地址数字
i = 30000
# 存储线程的dict[序号:线程引用]
thirdDict = {}

# 处理抓取任务
def loop():
	global i,thirdDict
	i += 1
	key = i
	# 放入当前进程的引用
	thirdDict[key] = threading.current_thread()
	
	pageUrl = "http://yao.xywy.com/goods/" + str(i + 1) + ".htm"
	try:
		request = urllib.urlopen(pageUrl)
	except Exception, e:
		# 删除key-value
		thirdDict.pop(key)
		return
	
	try:
		# 获得网页源码
		html = request.read()
	except Exception, e:
		# 关闭请求
		request.close()
		# 删除key-value
		thirdDict.pop(key)
		return
		
	# 获得title
	medicament = re.search(r"<title>(.*)?</title>",html)
	org = re.search(r'生产企业.*?">(.*?)</a>',html)
	# 如果匹配到了title和企业信息
	if medicament and org:
		# 如果是404就退出
		if medicament.group(1) == "":
			print "404! url:" + pageUrl
			# 关闭请求
			request.close()
			# 删除key-value
			thirdDict.pop(key)
			return
		# 打印药名和链接
		print medicament.group(1).decode("utf-8").split("(")[0] + " url:" + pageUrl
		# 写入文件
		medicamentF.write((medicament.group(1).decode("utf-8").split("(")[0] + " @f NeMedicament\n").encode("utf-8"))
		orgF.write((org.group(1).decode("utf-8") + " @f NeOrg\n").encode("utf-8"))
	# 关闭请求
	request.close()
	# 删除key-value
	thirdDict.pop(key)
	
medicamentF = open("/home/geekgao/medicament",'w')
orgF = open("/home/geekgao/org",'w')

thisStartTime = time.time()
while i < 453482:
	num = i
	# 线程要始终保持在50个
	if len(thirdDict) < 50:
		# 等待超时就退出（没有这个有时候线程并不能全部退出，看资源管理器，说“等候频道 poll_scheme_time”）
		if time.time() - thisStartTime > 10:
			print "等待时间到,强行退出."
			break
		print '新进程:' + str(num) + "loopThird" + "进程总数:" + str(len(thirdDict))
		t = threading.Thread(target = loop, name = str(num) + "loopThird")
		# t = threading.Thread(target = thirdMonitor, name = str(num) + "thirdMonitor",args=(num,))
		t.start()
	time.sleep(0.001)

while len(thirdDict) != 0:
	time.sleep(0.001)
medicamentF.close()
orgF.close()
print "完成"