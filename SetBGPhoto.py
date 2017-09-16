#!/usr/bin/python
#encoding:utf-8
import time
import os
import urllib
import re
import os

html = urllib.urlopen("http://cn.bing.com/").read()

imgAddress = re.search(r'g_img={url: "(.*?)"',html).group(1).replace('\\','')
imgAddress = "http://cn.bing.com" + imgAddress


if imgAddress:
	path = os.path.expanduser('~') + "/BingImg/"
	if os.path.exists(path) == False:
		os.makedirs(path)

	fileName = path + time.strftime("%Y-%m-%d") + ".jpg"
	print "今天Bing图片的地址是:" + imgAddress
	print "正在下载……"
	urllib.urlretrieve(imgAddress, fileName)
	print "下载完毕!" + "存储为" + fileName
	orderStr = "gsettings set org.gnome.desktop.background picture-uri \"file:" + fileName + "\""
	os.system(orderStr)
else:
	print "今天貌似出问题了……"
