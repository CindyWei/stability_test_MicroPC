#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import os

img_url = None

try:
	r=requests.get('http://vbuild.alibaba-inc.com:8080/job/rk-rk3188-micropc_askey-rk3188-eng/lastBuild/console')
	soup=bs(r.text)
	console=soup.find("pre", {"class", "console-output"})
	logs=console.text.split("\n")
	for l in logs:
		if l.find("img_oss url")>=0:
			img_url = l.split(" ")[2]
			break

	#http://osimage.oss-cn-hangzhou-zmf.aliyuncs.com/YUNPC_MICROPC_ASK/0.8.6-D-20150227.0441/0.8.6-D-20150227.0441_img.zip
	if img_url:
		img_name = img_url.split("/")[-1]

		#检查当前最新的测试包是否已经测试过，查询数据库的下载测试记录。
		

		#数据库记录新下载的镜像包、下载时间、下载状态(成功/失败)
		os.system("curl " + img_url + " -o " + img_name)

		#解压zip包
		os.system("unzip " + img_name)

		#刷机
		os.system("adb reboot bootloader")
		sleep(5)
		os.system("./upgrade_tool di -b")
		os.system("./upgrade_tool di -m")
		os.system("./upgrade_tool di -r")
		os.system("./upgrade_tool di -s")
		os.system("./upgrade_tool di rd")

except:
	print "error happend"
