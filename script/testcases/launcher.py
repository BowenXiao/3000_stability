#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import random
import util as u

# screen display resolution
RESOLUTION_X = d.info['displayWidth']
RESOLUTION_Y = d.info['displayHeight']

VIEW_MODE = {'36':'三十六宫格',
			'81':'八十一宫格',
			'16':'十六宫格',
			'default':'安卓原生'}

THEME_LIST = ['经典','蓝色','褐色','青色','木纹','浅灰','橙色','紫色','灰岩']

class LauncherTest(unittest.TestCase):
	def setUp(self):
		d.watcher("IGNORE_ANR").when(textContains='停止运行').click(text='确定')
		u.setUp()

	def tearDown(self):
		d.watchers.remove("IGNORE_ANR")
		u.tearDown()

#	def testLauncherMultiViewRename(self):
#		# press menu to enter multi view
#		d.press('menu')
#		d.sleep(1)
#		# click 'rename' icon
#		d.click(470,150)
#		d.sleep(1)
#		assert d(text = '命名板块标题').exists,'Rename is not show on the screen!'
#		if d(text = '命名板块标题').exists:
#			d(className = 'android.widget.EditText').set_text('test')
#			d(text = '取消').click.wait()#

#	def testLauncherMultiViewHide(self):
#		# press menu to enter multi view
#		d.press('menu')
#		d.sleep(1)
#		# click 'setting' icon
#		d.click(130,1800)
#		d.sleep(1)
#		# click 'Hide' icon
#		d.click(70,150)
#		d.sleep(1)
#		assert d(packageName = 'com.smartisanos.launcher').exists,'Launcher is not show on the screen!'
#		# click 'Hide' icon again to show the hided view
#		d.click(70,150)
#		d.sleep(1)#

#	def testLauncherMultiViewLock(self):
#		# press menu to enter multi view
#		d.press('menu')
#		d.sleep(1)
#		# click 'setting' icon
#		d.click(130,1800)
#		d.sleep(1)
#		# click 'lock' icon
#		d.click(470,145)
#		d.sleep(1)
#		assert d(text = '板块密码').exists,'Create password view is not show on the screen!'
#		if d(text = '板块密码').exists:
#			d(text = '取消').click.wait()#

#	def testLauncherSwipeScreen(self):
#		# swipe to left
#		for i in range(3):
#			d.swipe(1040,960,40,960,10)
#			d.sleep(1)
#		# swipe to right
#		for i in range(3):
#			d.swipe(40,960,1040,960,10)
#			d.sleep(1)
#		assert d(packageName = 'com.smartisanos.launcher').exists,'Launcher is not show on the screen!'

	def testScreenLockUnlock(self):
		for i in range(100):
			# screen off
			d.screen.off()
			u.unlock()


	def testMultiViewDrag(self):
		# press menu to enter multi view
		d.press('menu')
		d.sleep(1)
		for i in range(100):
			# random select drag range
			range_X = range(30,1060)
			range_Y = range(210,1630)
			sx = random.choice(range_X)
			sy = random.choice(range_Y)
			ex = random.choice(range_X)
			ey = random.choice(range_Y)
			step = random.randint(10,50)
			d.drag(sx, sy, ex, ey,step)
			d.sleep(1)

	def testSwipeScreen(self):
		# swipe home screen 1000 times totally
		for i in range(100):
			direction = random.choice(['left','right'])
			step = random.randint(5,50)
			self._swipeScreen(direction,step)
			d.sleep(1)

	def _switchLauncherSettings(self,viewmode):
		# launch setting
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		# get into launcher settings
		if d(text = '单板块视图').wait.exists(timeout = 5000):
			pass
		else:
			u.selectOption('桌面设置项')
			assert d(text = '单板块视图').wait.exists(timeout = 5000),'Switch to Desktop Settings failed in 5s!'
		if viewmode == '36' or viewmode == '81':
			if d(text = '多板块视图').exists:
				d(text = VIEW_MODE[viewmode]).click.wait()
				if d(text = '设置桌面').wait.exists(timeout = 5000):
					d(text = '确定').click.wait()
			else:
				d(text = '九宫格').click.wait()
				d.sleep(3)
				if d(text = '设置桌面').wait.exists(timeout = 5000):
					d(text = '确定').click.wait()
					d.sleep(3)
				d.start_activity(component='com.android.settings/.Settings')
				assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'
				d(text = VIEW_MODE[viewmode]).click.wait()
				if d(text = '设置桌面').wait.exists(timeout = 5000):
					d(text = '确定').click.wait()
		else:
			d(text = VIEW_MODE[viewmode]).click.wait()
			if d(text = '设置桌面').wait.exists(timeout = 5000):
				d(text = '确定').click.wait()

	def _swipeScreen(self,direction,step=None):
		if direction == 'left':
			d(resourceId = 'com.smartisanos.launcher:id/glview').swipe.left(steps=step)
		elif direction == 'right':
			d(resourceId = 'com.smartisanos.launcher:id/glview').swipe.right(steps=step)
		else:
			raise NameError
			print 'invalid string'