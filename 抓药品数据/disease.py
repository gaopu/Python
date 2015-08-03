#coding=utf-8
import urllib
import re
import threading

i = 0
def loop():
	global i
	i += 1
	pageUrl = "http://jib.xywy.com/il_sii_" + str(i + 1) + ".htm"
	request = urllib.urlopen(pageUrl)

	# 获得网页源码
	html = request.read()
	# 获得title
	disease = re.search(r"<title>(.*?)</title>",html)
	# 如果匹配到了title
	if disease:
		# 打印病名和链接
		print disease.group(1).decode("gbk").split(",")[0] + " url:" + pageUrl
		# 如果是404就退出
		if re.match("^404",disease.group(1).decode("gbk").split(",")[0]):
			return
		# 写入文件
		f.write((disease.group(1).decode("gbk").split(",")[0] + " @f NeDisease\n").encode("utf-8"))
	# 关闭请求
	request.close()
	
f = open("/home/geekgao/disease1",'w')

while i < 10136:
	# 存储线程引用
	thirdList = []
	# = 线程计数
	count = 0
	# 每次同时启用100个线程
	while count < 200:
		count += 1
		t = threading.Thread(target = loop, name = str(i))
		t.start()
		thirdList.append(t)
	for t in thirdList:
		t.join()

f.close()
print "完成"