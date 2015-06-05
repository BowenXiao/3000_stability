#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import random
import util as u

class The3rdTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		u.tearDown()


	def testWeibo(self):
		# launch weibo
		d.start_activity(component='com.sina.weibo/.SplashActivity')
		assert d(packageName = 'com.sina.weibo').wait.exists(timeout = 5000),'Launch Weibo failed in 5s!'
		if d(text = '特别提示').wait.exists(timeout = 5000):
			d(text = '确定').click.wait()
		if d(text = '给我们评分').wait.exists(timeout = 5000):
			d(text = '不了，谢谢').click.wait()

		#Refresh weibo
		d(description = '首页').click.wait()
		d.sleep(3)
		if d(description = '评论').exists:
			d(description = '评论').click.wait()
		if d(text = '赞').exists:
			d(text = '赞').click.wait()
		if d(description = '评论').exists:
			d(description = '评论').click.wait()
		d(resourceId = 'com.sina.weibo:id/et_mblog').set_text('Good!')
		d(text = '发送').click.wait()
		if d(resourceId = 'com.sina.weibo:id/titleBack').exists:
			d(resourceId = 'com.sina.weibo:id/titleBack').click.wait()
		d.sleep(1)
		# check one message of weibo
		d.click(770, 670)
		d.sleep(2)
		d.swipe(540, 1400, 540, 700, 100)
		d.sleep(2)
		d.swipe(540, 1400, 540, 700, 100)
		d.sleep(2)

	def testWeixin(self):
		#Launch weixin
		d.start_activity(component='com.tencent.mm/.ui.LauncherUI')
		assert d(packageName = 'com.tencent.mm').wait.exists(timeout = 5000),'Launch Weixin failed in 5s!'
		if d(textContains = '欢迎使用微信').exists:
			d(text = '确定').click.wait()

		d(text = '微信').click.wait()
		assert d(resourceId = 'android:id/text1',textContains = '微信').wait.exists(timeout = 5000),'Switch to chat view failed in 5s!'
		d(text = 'Autotest').click.wait()
		assert d(textContains = 'Autotest').wait.exists(timeout = 5000),'Switch to dialog view failed in 5s!'
		
		#Edit text content
		d(className = 'android.widget.EditText').set_text('test')
		#add emoji
		d(className = 'android.widget.ImageButton',resourceId = 'com.tencent.mm:id/r3').click.wait()
		d(resourceId = 'com.tencent.mm:id/bie').click()
		d(text = '发送').click.wait()

	def testNavigation(self):
		d.start_activity(component='com.autonavi.minimap/com.autonavi.map.activity.SplashActivity')
		if d(text = '系统提示').wait.exists(timeout = 5000):
			d(text = '不再显示提醒!').click.wait()
			d(text = '同意').click.wait()
		if d(text = '欢迎使用高德地图!').wait.exists(timeout = 5000):
			d(text = '同意').click.wait()
		for i in range(10):
			direction = random.choice(['left','right','up','down'])
			step = random.randint(5,50)
			self._swipeMap(direction,step)
			d.sleep(1)
		d(resourceId = 'com.autonavi.minimap:id/GpsButton',description = '我的位置').click.wait()
		d(textContains = '我的位置 (精度').wait.exists(timeout = 30000)
		assert d(textContains = '我的位置 (精度').exists,'Location failed, My position is not show on the screen!'
		d.press('back')
		d.sleep(1)
		d.press('back')
		d.press('back')
		#d(text = '退出').wait.exists(timeout = 5000),'Confirm exit alarm does not pop-up in 5s!'
		#d(text = '确定').click.wait()

	def testGame(self):
		#Launch DiTiePaoKu
		d.start_activity(component='com.kiloo.subwaysurf/.RRAndroidPluginActivity')
		assert d(packageName = 'com.kiloo.subwaysurf').wait.exists(timeout = 5000),'Launch game failed in 5s!'
		d.sleep(10)
		if d(text = '地铁跑酷正试图发送短信').exists:
			d(text = '允许').click.wait()
		if d(text = '地铁跑酷正试图获取位置信息').exists:
			d(text = '允许').click.wait()
		if d(text = '免费礼包大派送').exists:
			d(text = '7天内不再显示').click.wait()
			d(text = '暂不领取').click.wait()
		if d(text = '提示').exists:
			d(text = '取消').click.wait()
		if d(className = 'android.widget.TextView').exists:
			d(className = 'android.widget.TextView').click.wait()

		#Click screen to start game
		d.click(300,1540)
		d.sleep(4)

		for i in range(900):
			direction = random.choice(['left','right','up','down'])
			step = random.randint(2,20)
			self._swipeGame(direction,step)
			d.sleep(1)

		#Exit game
		d.press('back')
		d.sleep(1)
		d.click(150,1800)
		d.sleep(1)
		d.click(700,1100)
		d.sleep(1)

	def testYouku(self):
		#Launch youku
		d.start_activity(component='com.youku.phone/.ActivityWelcome')
		if d(textContains = '欢迎使用优酷客户端').exists:
			d(text = '不再显示提醒！').click.wait()
			d(text = '确定').click.wait()
		if d(textContains = '优酷Youku软件最终用户').exists:
			d(text = '同意').click.wait()
		assert d(packageName = 'com.youku.phone').wait.exists(timeout = 5000),'Launch Youku failed in 5s!'
		d(text = '首页').wait.exists
		assert d(resourceId = 'com.youku.phone:id/home_gallery_item_title_layout').wait.exists(timeout = 10000),'Youku homepage does not loading finished in 10s!'
		
		#Play video
		#d(resourceId = 'com.youku.phone:id/homepage_gallery_item_play').click.wait()
		d.click(500,650)
		assert d(textContains = '选集').wait.exists(timeout = 5000),'Switch surface view failed in 5s!'
		# play time
		d.sleep(10)
		assert d(resourceId = 'com.youku.phone:id/surface_view').exists,'Playground is not show on the screen!'

	def _swipeGame(self,direction,step=None):
		if direction == 'left':
			d.swipe(800,960,300,960,step)
		elif direction == 'right':
			d.swipe(300,960,800,960,step)
		elif direction == 'up':
			d.swipe(540,1030,540,540,step)
		elif direction == 'down':
			d.swipe(540,540,540,1030,step)
		else:
			raise NameError
			print 'invalid string'

	def _swipeMap(self,direction,step=None):
		if direction == 'left':
			d(resourceId = 'com.autonavi.minimap:id/right_content').swipe.left(steps=step)
		elif direction == 'right':
			d(resourceId = 'com.autonavi.minimap:id/right_content').swipe.right(steps=step)
		elif direction == 'up':
			d(resourceId = 'com.autonavi.minimap:id/right_content').swipe.right(steps=step)
		elif direction == 'down':
			d(resourceId = 'com.autonavi.minimap:id/right_content').swipe.right(steps=step)
		else:
			raise NameError
			print 'invalid string'