#!/usr/bin/python
#coding:utf-8
import urllib
import sys
import re

if len(sys.argv) == 1:	#没有单词就提示用法
	print "用法:./Dict.py 要查找的单词"
	sys.exit()

word = ""
for x in range(len(sys.argv) - 1): #查找的可能是短语，中间有空格，如"join in",这里拼接单词
	word += " " + sys.argv[x + 1]
print "单词：" + word

searchUrl = "http://dict.youdao.com/search?q=" + word + "&keyfrom=dict.index"	#查找的地址
response = urllib.urlopen(searchUrl).read() #获得查找到的网页源码

#从网页源码提取出单词释义那一部分
searchSuccess = re.search(r"(?s)<div class=\"trans-container\">\s*<ul>.*?</div>",response)

if searchSuccess:
	means = re.findall(r"(?m)<li>(.*?)</li>",searchSuccess.group()) #获取我们想提取的核心单词释义
	print "释义："
	for mean in means:
		print "\t" + mean	#输出释义
else:
	print "未查找到释义."