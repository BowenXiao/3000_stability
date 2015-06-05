#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import random
import util as u

THEME = ['经典','蓝色','褐色','青色','木纹','浅灰','橙色','紫色','灰岩']

class SettingTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		u.tearDown()

	def testSetTheme(self):
		#Launch Setting
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		#Set theme
		theme = random.choice(THEME)
		self._selectOption('主题、壁纸、图标')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '主题、壁纸、图标').wait.exists(timeout = 5000),'Switch to theme view failed in 5s!'
		self._selectOption('桌面主题')
		assert d(resourceId = 'com.smartisanos.launcher:id/tv_title',text = '桌面主题').wait.exists(timeout = 5000),'Switch to theme view failed in 5s!'
		self._selectOption(theme)
		assert d(resourceId = 'smartisanos:id/tv_title',text = theme).wait.exists(timeout = 5000),'Switch to theme thumbnail failed in 5s!'
		d(text = '设定').click.wait()
		assert d(packageName = 'com.smartisanos.launcher').exists,'Launcher is not show on the screen!'

		# back from setting to home screen
		d.start_activity(component='com.android.settings/.Settings')

	def testTurnOnOffWiFi(self):
		#Launch Setting
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		self._selectOption('无线网络')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '无线网络').wait.exists(timeout = 5000),'Switch to WIFI failed in 5s!'
		if d(text = '要查看可用网络，请打开无线网络').exists:
			print 'Current wifi status: Off'
			d(resourceId = 'com.android.settings:id/item_switch').swipe.right(steps = 5)
			d(text = '已连接').wait.exists(timeout = 5000)
		else:
			print 'Current wifi status: On'
			d(text = '已连接').wait.exists(timeout = 5000)
		#Turn off wifi
		d(resourceId = 'com.android.settings:id/item_switch').swipe.left(steps = 5)
		assert d(text = '要查看可用网络，请打开无线网络').wait.exists(timeout = 5000),'Turn off wifi failed in 5s!'
		#Turn on wifi
		d(resourceId = 'com.android.settings:id/item_switch').swipe.right(steps = 5)
		assert d(text = '已连接').wait.exists(timeout = 5000),'Turn on wifi failed in 5s!'

	def testTurnOnOffBT(self):
		#Launch Setting
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		self._selectOption('蓝牙')
		assert d(resourceId = 'smartisanos:id/tv_title',text = '蓝牙').wait.exists(timeout = 5000),'Switch to BT failed in 5s!'
		if d(text = '范围内可配对设备').exists:
			print 'Current BT status: On'
			d(resourceId = 'com.android.settings:id/item_switch').swipe.left(steps = 5)
			d(text = '要查看可用蓝牙设备，请打开蓝牙功能').wait.exists(timeout = 5000)
		#Turn off BT
		d(resourceId = 'com.android.settings:id/item_switch').swipe.right(steps = 5)
		assert d(text = '范围内可配对设备').wait.exists(timeout = 5000),'Turn on BT failed in 5s!'
		#Turn on wifi
		d(resourceId = 'com.android.settings:id/item_switch').swipe.left(steps = 5)
		assert d(text = '要查看可用蓝牙设备，请打开蓝牙功能').wait.exists(timeout = 5000),'Turn off BT failed in 5s!'

	def testTurnOnOffNFC(self):
		#Launch Setting
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout = 5000),'Launch settings failed in 5s!'

		self._selectOption('NFC')
		assert d(resourceId = 'smartisanos:id/tv_title',text = 'NFC').wait.exists(timeout = 5000),'Switch to NFC failed in 5s!'
		d(className="android.widget.RelativeLayout", resourceId="com.android.settings:id/item_id_nfc").child(className="smartisanos.widget.SwitchEx").swipe.right(steps = 5)
		d.sleep(3)
		assert d(className="android.widget.RelativeLayout", resourceId="com.android.settings:id/item_id_android_beam").child(className="smartisanos.widget.SwitchEx").info['enabled'],'Turn NFC failed in 3s!'
		#d(text="NFC").right(className="smartisanos.widget.SwitchEx").click()
		d(className="android.widget.RelativeLayout", resourceId="com.android.settings:id/item_id_nfc").child(className="smartisanos.widget.SwitchEx").swipe.left(steps = 5)
		assert not d(className="android.widget.RelativeLayout", resourceId="com.android.settings:id/item_id_android_beam").child(className="smartisanos.widget.SwitchEx").info['enabled'],'Turn NFC failed in 3s!'

	def _selectOption(self,option):
		i = 1
		while i:
			if d(text = option).exists:
				break
			d.swipe(540,1400,540,400,100)
			d.sleep(1)
			i+=1
			if d(text = option).exists or i==10:
				break
		d.sleep(1)
		d(text = option).click.wait()