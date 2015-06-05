#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import util as u

class PIMTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		u.tearDown()

	def testCalendarEvent(self):
		#Launch calander
		d.start_activity(component='com.android.calendar/.AllInOneActivity')
		assert d(text='今天').wait.exists(timeout = 5000),'Launch calendar failed in 5s!'

		#Create event and edit event title and address
		d(text = '新建').click.wait()
		if  d(text = '请选择将任务保存至').exists:
			d(text = '本地账户').click.wait()
		assert d(text = '本地账户').wait.exists(timeout = 5000),'Switch to create event view failed in 5s!'
		d(text = '任务标题').set_text('Test Event')
		if  d(text = '更多选项').exists:
			d(text = '更多选项').click.wait()
		assert d(text = '地点').wait.exists(timeout=5000),'Switch detil edit view failed in 5s!'
		d(text = '地点').set_text('Motolora')
		d(text = '完成').click.wait()
		assert d(resourceId = "com.android.calendar:id/agenda_content").wait.exists(timeout=5000),'Event does not show on the screen in 5s!'
		d.sleep(2)

		#Delete event
		d(resourceId = "com.android.calendar:id/agenda_content").swipe.right(steps=10)
		d(resourceId = 'com.android.calendar:id/delete_icon').click.wait()
		assert d(textContains = '任务列表为空').exists,'Delete event failed'

	def testClock(self):
		#Launch clock
		d.start_activity(component='com.smartisanos.clock/.activity.ClockActivity')
		if d(textContains = '时钟需要获取定位数据').wait.exists(timeout=3000):
			d(text = '同意').click.wait()
		assert d(text = '闹钟').wait.exists(timeout=5000),'Launch clock failed in 5s!'

		d(text = '闹钟').click.wait()
		assert d(resourceId = 'com.smartisanos.clock:id/title',text = '闹钟').wait.exists(timeout=5000),'Switch to clock view failed in 5s!'

		#Create clock
		d(resourceId = 'com.smartisanos.clock:id/add').click.wait()
		assert d(resourceId = 'com.smartisanos.clock:id/hour').wait.exists(timeout=5000),'Switch to edit clock view failed in 5s!'
		d(resourceId = 'com.smartisanos.clock:id/hour').swipe.up(steps=10)
		d(text = '确定').click.wait()

		d(resourceId = 'com.smartisanos.clock:id/set').click.wait()
		assert d(text = '删除闹钟').wait.exists(timeout = 5000),'Switch to set clock view failed in 5s!'
		d(text = '删除闹钟').click.wait()
		assert d(packageName = 'com.smartisanos.clock').exists,'Clock is not show on the screen!'