#!/usr/bin/python
#encoding:utf-8
import time
import os
import urllib
import re

html = urllib.urlopen("http://cn.bing.com/").read()

imgAddress = re.search(r"http://.*?\.jpg",html)

if imgAddress:
	fileName = "/home/geekgao/图片/BingImg/" + time.strftime("%Y-%m-%d") + ".jpg"
	print "今天Bing图片的地址是:" + imgAddress.group()
	print "正在下载……"
	urllib.urlretrieve(imgAddress.group(), fileName)
	print "下载完毕!" + "存储为" + fileName
	orderStr = "gsettings set org.gnome.desktop.background picture-uri \"file:" + fileName + "\""
	os.system(orderStr)
else:
	print "今天貌似出问题了……"