# !/usr/bin/python
# coding:utf-8

import urllib, os, urllib2, cookielib, re

# 下载极客学院的视频
# 需要一个vip账号(验证邮箱和手机会有体验vip)
class DownCourse(object):
	# 给urllib2添加cookie支持
	# path: 下载的视频要保存的文件夹
	def __init__(self,path):
		# 初始化一个CookieJar来处理Cookie
		cookieJar = cookielib.CookieJar()
		# 实例化一个全局opener
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		# 把这个cookie处理机制装上去,大概是这个意思-.-
		urllib2.install_opener(opener)

		self.folderPath = path
		# 判断文件夹是否存在
		folderExists = os.path.exists(self.folderPath)
		if not folderExists:
			os.mkdir(self.folderPath)

	# 登陆函数
	def login(self):
		# 从登录页面获取登陆参数
		login_url = 'http://passport.jikexueyuan.com/sso/login'
		# 登陆信息发送到这个地址
		passport_url = 'http://passport.jikexueyuan.com/submit/login?is_ajax=1'
		verifyCode_url = 'http://passport.jikexueyuan.com/sso/verify'

		# 获取登陆页面源码
		request = urllib2.urlopen(login_url)
		html = request.read()
		request.close()

		# 获取登陆要post的数据
		expire = re.search(r"(?s)value='(.*?)' name='expire",html)
		# 验证码
		verifyCodeGifPath = '/tmp/jikexueyuan.gif'
		request = urllib2.urlopen(verifyCode_url)
		gif = request.read()
		request.close()
		fGif = open(verifyCodeGifPath,'w')
		fGif.write(gif)
		fGif.close()
		# 读取保存到本地的验证码图片
		os.system('eog ' + verifyCodeGifPath)
		verify = raw_input("请输入图中的验证码:")

		data = {
			'expire': expire.group(1),
			'referer': 'http%3A%2F%2Fwww.jikexueyuan.com%2F',
			'uname': 用户名,
			'password': 密码,
			'verify': verify,
		}
		post_data = urllib.urlencode(data)

		request = urllib2.Request(passport_url,post_data)
		# 给一个useragent,防止被认为是爬虫程序
		request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36')
		# 发送登录请求
		request = urllib2.urlopen(request)
		request.close()
		print '登陆完成'

	# courseUrl: 课程地址首页,例如:http://www.jikexueyuan.com/course/989.html
	def download(self, courseUrl):
		# 获取课程名称
		request = urllib2.urlopen(courseUrl)
		coursePageHtml = request.read()
		request.close()
		courseName = re.search(r'(?s)<title>(.*?)-',coursePageHtml).group(1)
		# 课程数量
		courseCount = int(re.search(r'(?s)class="timebox"><span>(.*?)课时',coursePageHtml).group(1))
		# 存储视频的文件夹路径
		folderPath = self.folderPath + courseName + '/'
		# 判断文件夹是否存在
		folderExists = os.path.exists(folderPath)
		if not folderExists:
			os.mkdir(folderPath)

		print '课程名:' + courseName + ' 课程数量:' + str(courseCount)
		# 课程的编号,构建课程的页面地址
		i = 0
		while i < courseCount:
			i += 1
			pageUrl = courseUrl.split('.html')[0] + '_' + str(i) + '.html?ss=1'
			# 本节课程的html代码
			request = urllib2.urlopen(pageUrl)
			pageHtml = request.read()
			request.close()
			# 本节课程的名称
			name = re.search(r'(?s)<title>(.*?)-',pageHtml).group(1)
			# 本节课程的视频地址
			videoUrl = re.search(r'<source src="(.*?)"',pageHtml)
			# 有的页面写的课时比实际课时多,会匹配不到视频地址
			if videoUrl == None:
				continue
			else:
				videoUrl = videoUrl.group(1)
			print '正在下载' + name + '...'
			# 存储视频的Path: 总路径/课程名/每一节的名称
			urllib.urlretrieve(videoUrl,folderPath + str(i) + name + '.mp4',self.cbk)
		print '下载完成'

	# 从网上下载的可以显示下载进度的函数
	# \b是我加的,产生了很奇特的显示效果,还行
	def cbk(self,a, b, c):
	    '''回调函数
	    @a: 已经下载的数据块
	    @b: 数据块的大小
	    @c: 远程文件的大小
	    '''
	    per = 100.0 * a * b / c
	    if per > 100:
	        per = 100
	    print '%.2f%%\b\b\b\b\b\b' % per,

# 建立下载对象,参数是即将下载的这些视频放的目录,程序会根据课程名在这个文件夹里面再建文件夹
down = DownCourse('/home/geekgao/视频/SpringMVC/')
down.login()

# 下载一个页面中的所有课程
request = urllib2.urlopen('http://www.jikexueyuan.com/course/springmvc/')
html = request.read()
request.close()
courseUrls = re.findall(r'class="lesson-info-h2"><a href="(.*?)"',html)

for courseUrl in courseUrls:
	down.download(courseUrl)
