# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands

class UiaTest(unittest.TestCase):
	def setUp(self):
		for i in range(3):
			d.press('back')
		d.press('home')

	def tearDown(self):
		d.press('home')

	def testMOCall(self):
		commands.getoutput('adb shell am start -n com.android.contacts/.activities.DialtactsActivity')
		d(resourceId = 'com.android.contacts:id/one_classic', description = '一').click.wait()
		d(resourceId = 'com.android.contacts:id/zero_classic', description = '零').click.wait()
		d(resourceId = 'com.android.contacts:id/zero_classic', description = '零').click.wait()
		d(resourceId = 'com.android.contacts:id/eight_classic', description = '八').click.wait()
		d(resourceId = 'com.android.contacts:id/six_classic', description = '六').click.wait()
		d(resourceId = 'com.android.contacts:id/call_classic').click.wait()
		assert d(text='结束').wait.exists(timeout=15000),'Calling failed!'
		d(text='结束').click.wait()
		d.sleep(3)
		d.expect('10086.png')