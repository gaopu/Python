#coding=utf-8
import urllib
import re
import threading

i = 0
def loop():
	global i
	i += 1
	pageUrl = "http://zzk.xywy.com/" + str(i) + "_gaishu.html"
	request = urllib.urlopen(pageUrl)

	# 获得网页源码
	html = request.read()
	# 如果是404就退出
	if html == "404":
		print "404! url:" + pageUrl
		return
	# 获得title
	symptom = re.search(r"<title>(.*?)</title>",html)
	# 如果匹配到了title
	if symptom:
		# 打印症状和链接
		print symptom.group(1).decode("gbk").split(u"怎么办")[0] + " url:" + pageUrl
		# 写入文件
		f.write((symptom.group(1).decode("gbk").split(u"怎么办")[0] + " @f Nesymptom\n").encode("utf-8"))
	# 关闭请求
	request.close()
	
f = open("/home/geekgao/symptom1",'w')

while i < 6911:
	# 存储线程引用
	thirdList = []
	# = 线程计数
	count = 0
	# 每次同时启用200个线程
	while count < 200:
		count += 1
		t = threading.Thread(target = loop, name = str(i))
		t.start()
		thirdList.append(t)
	for t in thirdList:
		t.join()

f.close()
print "完成"