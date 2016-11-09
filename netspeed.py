#! /usr/bin/python
#coding:utf-8

import urllib2,re,sys

if len(sys.argv) < 3:
    print "用法:./netspeed 主机号 下载速度(kB/S)"
    sys.exit()

ip = "192.168.1." + sys.argv[1]
downSpeed = int(sys.argv[2]) * 8

request = urllib2.Request('http://192.168.1.1/userRpm/QoSCfgRpm.htm?enable=true&start_ip_addr=' + ip + '&end_ip_addr=' + ip + '&min_up_band_width=0&max_up_band_width=0&min_down_band_width=0&max_down_band_width=' + str(downSpeed) + '&Save=%B1%A3+%B4%E6&curEditId=0&Page=1')
request.add_header('Cookie','Authorization=Basic%20YWRtaW46aHVxaWFuZ3hp; ChgPwdSubTag=')
request.add_header('Referer','http://192.168.1.1/userRpm/SystemStatisticRpm.htm?contType=1&sortType=4&Num_per_page=100&Goto_page=1')
request.add_header('Upgrade-Insecure-Requests','1')
request.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36')

urllib2.urlopen(request)
