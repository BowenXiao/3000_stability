#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import util as u

TOP5 = ['www.baidu.com','www.taobao.com','www.163.com','www.qq.com','www.youku.com']
CHECK_POINT = ['Baidu.png','Taobao.png','163.png','QQ.png','Youku.png']

class BrowserTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		self._clearCache()
		u.tearDown()
		self._clearData('/sdcard/Download/*')
		
	def _clearData(self):
		#Clear cache

		#Delete files
		commands.getoutput("adb shell rm -rf /sdcard/Download/*")
		#update media mounted
		commands.getoutput("adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard")

	def _closeWindows(self):
		# close all webpage
		d(resourceId = 'com.android.browser:id/switch_btn').click.wait()
		d(resourceId = 'com.android.browser:id/clearall').click.wait()
		d(text = '关闭').click.wait()

	#Open webpage and do some swiping
	def testVisitWebPage(self):
		#Launch Browser
		self._launchBrowser()

		# visite webpage
		d(resourceId = 'com.android.browser:id/url', text = '输入网址').set_text(TOP5[3])
		d.press('enter')
		d.expect(CHECK_POINT[3], timeout=15)
		# browse webpage
		d.swipe(1000,1300,1000,600,10)
		d.sleep(1)
		d.swipe(1000,1300,1000,600,10)
		d.sleep(1)
		d.swipe(1000,600,1000,1300,10)
		d.sleep(1)
		d.swipe(1000,600,1000,1300,10)
		d.sleep(1)

		#Close all webpage windows
		#self._closeWindows()

	#Open webpage and do some navigation
	def testWebNavigation(self):
		#Launch Browser
		self._launchBrowser()

		#Visite webpage
		d(resourceId = 'com.android.browser:id/url', text = '输入网址').set_text('wap.sohu.com')
		d.press('enter')
		d.expect('Web_Navigation_News.png',timeout=10, msg = 'Loading webpage failed in 10s!')

		#Click Navigation '新闻'
		d.click('Web_Navigation_News.png')
		#d.expect('Web_Title_News.png',timeout=10, msg = 'Loading to News failed in 10s!')

		#Close all webpage windows
		#self._closeWindows()

	#Visit top5 web pages
	def testVisitTop5(self):
		#Launch Browser
		self._launchBrowser()

		#Visite TOP5 webpage
		for i in range(5):
			d(resourceId = 'com.android.browser:id/url', text = '输入网址').set_text(TOP5[i])
			d.sleep(2)
			d.press('enter')
			if d(textContains = '需要了解您的位置信息').wait.exists():
				d(text = '拒绝').click.wait()
			d.expect(CHECK_POINT[i],timeout=10, msg = 'Loading webpage %s failed in 10s!'%TOP5[i])
			d(resourceId = 'com.android.browser:id/newtab_btn').click.wait()

		#Close all webpage windows
		#self._closeWindows()

	def testDownloadPics(self):
		#Launch Browser
		self._launchBrowser()

		#Input download pics url
		d(resourceId = 'com.android.browser:id/url', text = '输入网址').set_text('auto.smartisan.com/media/Auto_Test_Image.jpg')
		d.sleep(1)
		d.press('enter')
		d.sleep(5)
		# swipe up to show '普通下载'
		d.long_click(500, 670)
		d.sleep(1)
		assert d(text = '保存图片').wait.exists(timeout = 5000),'Save download window does not pop-up in 5s!'
		d(text = '保存图片').click()
		if  d(textContains = '您正在通过移动数据下载').wait.exists(timeout=1000):
			d(text = '继续').click.wait()
		
		#Looping 60s to check if download is ok
		for i in range(60):
			if u.getFileCount('/sdcard/Download', 'jpg') > 0:
				return
			d.sleep(1)
		assert False, 'Can not download pics in 60s. '

		#Close all webpage windows and clear downloaded resource
		#self._closeWindows()
		self._clearData()

#		# set pics as wallpapper
#		commands.getoutput('adb shell am start -n com.android.settings/.Settings')
#		d(text = '主题、壁纸、图标').click.wait()
#		d(text = '锁屏壁纸').click.wait()
#		d(text = '从相册选取').click.wait()
#		for i in range(2):
#			d.click(100,330)
#			d.sleep(1)
#		d.sleep(3)
#		d(resourceId = 'com.android.gallery3d:id/confirm_btn_in_crop',text = '确定').click.wait()


	def testDownloadAudio(self):
		#Launch Browser
		self._launchBrowser()

		# input download audio url
		d(resourceId = 'com.android.browser:id/url', text = '输入网址').set_text('auto.smartisan.com/media/Auto_Test_Music.mp3')
		d.sleep(1)
		d.press('enter')
		assert d(text = '是否下载该文件?').wait.exists(timeout = 10000), 'Not trigger download. '
		d(text = '下载').click.wait()
		if  d(textContains = '您正在通过移动数据下载').exists:
			d(text = '继续').click.wait()
		#Looping 60s to check if download is ok
		for i in range(60):
			if u.getFileCount('/sdcard/Download', 'mp3') > 0:
				return
			d.sleep(1)
		assert False, 'Can not download audio in 60s. '

		#Close all webpage windows and clear downloaded resource
		#self._closeWindows()
		self._clearData()

		# set pics as wallpapper
		#commands.getoutput('adb shell am start -n com.android.settings/.Settings')
		#d.sleep(1)
		#i = 1
		#while i:
		#	d.swipe(840,1400,840,400,100)
		#	d.sleep(1)
		#	i+=1
		#	if d(text = '声音和振动').exists or i==10:
		#		break
		#d(text = '声音和振动').click.wait()
		#d(text = '电话铃声').click.wait()
		#d(text = '选择歌曲作为铃声').click.wait()
		#d(text = '序幕:天地孤影任我行').click.wait()

	def testDownloadVideo(self):
		#Launch Browser
		self._launchBrowser()

		# input download audio url
		d(resourceId = 'com.android.browser:id/url', text = '输入网址').set_text('http://pan.baidu.com/s/1eQcRK3o')
		d.press('enter')
		d.sleep(5)
		d.swipe(540,1400,540,400,100)
		# click download
		d.click(800,1550)
		assert d(text = '是否下载该文件?').wait.exists(timeout = 10000), 'Not trigger download. '
		d(text = '下载').click.wait()
		if  d(textContains = '您正在通过移动数据下载').exists:
			d(text = '继续').click.wait()
		#Looping 60s to check if download is ok
		for i in range(60):
			if u.getFileCount('/sdcard/Download', 'mp4') > 0:
				return
			d.sleep(1)
		assert False, 'Can not download video in 60s. '

		#Close all webpage windows and clear downloaded resource
		#self._closeWindows()
		self._clearData()

		# check video
		#d.swipe(540,1,540,500,10)
		#d.sleep(1)
		#d(text = 'Auto_Test_Download_resource.mp4').click.wait()
		#d(text = '视频播放器').click.wait()
		#assert d(packageName = 'com.android.gallery3d').exists,'Play view is not show on the screen'

	def testPlayStreamingVideo(self):
		#Launch Browser
		self._launchBrowser()

		# input download audio url
		d(resourceId = 'com.android.browser:id/url', text = '输入网址').set_text('auto.smartisan.com/media/Auto_Test_Video.mp4')
		d.press('enter')
		d.sleep(5)
		d.expect('Streaming_Play.png',timeout = 15000)
		d.click('Streaming_Play.png')
		assert d(className = 'android.view.View').wait.exists(timeout = 15000),'Loading streaming video failed in 15s!'
		# play time
		d.sleep(10)
		d.press('back')
		assert d(description = '媒体控件').wait.exists(timeout = 5000),'Switch to webview failed in 5s!'
		if d.orientation != 'natural':
			d.orientation = 'n'

	def _launchBrowser(self):
		#Start Browser
		d.start_activity(component='com.android.browser/.BrowserActivity')
		assert d(resourceId = 'com.android.browser:id/switch_btn').wait.exists(timeout = 5000),'Launch browser failed in 5s!'
		d(resourceId = 'com.android.browser:id/newtab_btn').click.wait()


	def _clearCache(self):
		# close all webpage
		d(resourceId = 'com.android.browser:id/switch_btn').click.wait()
		d(resourceId = 'com.android.browser:id/clearall').click.wait()
		d(text = '关闭').click.wait()
		# clear cache
		d(resourceId = 'com.android.browser:id/menu_btn').click.wait()
		d.sleep(1)
		#select setting in option list
		d.click(590,1700)
		#d(resourceId = 'com.android.browser:id/option_list_item_text',text = '设置').click.wait()
		assert d(text = '设置').wait.exists(timeout = 3000),'Switch to setting view failed in 3s!'
		d(text = '隐私和安全').click.wait()
		assert d(resourceId = 'com.android.browser:id/action_new_event_text',text = '隐私和安全').wait.exists(timeout = 3000),'Switch to event view failed in 3s!'
		d(text = '清除缓存').click.wait()
		if  d(resourceId = 'android:id/alertTitle',text = '清除缓存').exists:
			d(text = '确定').click.wait()
		d(text = '清除历史记录').click.wait()
		if  d(resourceId = 'android:id/alertTitle',text = '清除历史记录').exists:
			d(text = '确定').click.wait()
		d(text = '清除所有 Cookie 数据').click.wait()
		if  d(resourceId = 'android:id/alertTitle',text = '清除所有 Cookie 数据').exists:
			d(text = '确定').click.wait()
		d(text = '返回').click.wait()
		d(text = '完成').click.wait()
		# clear download resource

	def _clearData(self,path):
		commands.getoutput('adb shell rm -r %s'%path)
