#coding=utf-8
# 最大453482
import urllib
import re
import threading

# 抓网页的地址数字
i = 0
def loop():
	global i
	i += 1
	pageUrl = "http://yao.xywy.com/goods/" + str(i + 1) + ".htm"
	request = urllib.urlopen(pageUrl)

	# 获得网页源码
	html = request.read()
	# 获得title
	medicament = re.search(r"<title>(.*)?</title>",html)
	org = re.search(r'生产企业.*?">(.*?)</a>',html)
	# 如果匹配到了title
	if medicament:
		# 如果是404就退出
		if medicament.group(1) == "":
			print "404! url:" + pageUrl
			return
		# 打印药名和链接
		print medicament.group(1).decode("utf-8").split("(")[0] + " url:" + pageUrl
		# 写入文件
		medicamentF.write((medicament.group(1).decode("utf-8").split("(")[0] + " @f NeMedicament\n").encode("utf-8"))
		orgF.write((org.group(1).decode("utf-8") + " @f NeOrg\n").encode("utf-8"))
	# 关闭请求
	request.close()
	
medicamentF = open("/home/geekgao/medicament",'w')
orgF = open("/home/geekgao/org",'w')

while i < 453482:
	# 存储线程引用
	thirdList = []
	# = 线程计数
	count = 0
	# 每次同时启用10个线程
	while count < 10:
		count += 1
		t = threading.Thread(target = loop, name = str(i))
		t.start()
		thirdList.append(t)
	for t in thirdList:
		t.join()

medicamentF.close()
orgF.close()
print "完成"