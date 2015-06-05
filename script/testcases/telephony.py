#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import random
import util as u

class TelephonyTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		u.tearDown()
		# kill phone
		#phonePID = u.getPID('com.android.contacts')
		#if phonePID == '':
		#	pass
		#else:
		#	commands.getoutput('adb shell kill %s'%phonePID)


	def testCallViaDialer3G(self):
		self._callDialer()

	def testCallViaCallLog3G(self):
		self._callCallLog()

	def testCallViaPhoneBook3G(self):
		self._callPhoneBook()

	def testCallViaDialer2G(self):
		self._callDialer()

	def testCallViaCallLog2G(self):
		self._callCallLog()

	def testCallViaPhoneBook2G(self):
		self._callPhoneBook()

	def testAddDelContact(self):
		#Launch phone app
		self._launchPhone()

		#Select Contacts
		d(text = '联系人').click.wait()
		assert d(text = '群组').wait.exists(timeout=5000),'Switch to phone book failed in 5s!'

		#Add new contact
		d(text = '添加').click.wait()
		assert d(text = '本地保存').wait.exists(timeout = 5000),'Pop-up reserve method failed in 5s!'
		d(text = '本地保存').click.wait()
		assert d(text = '新建 本地 联系人').wait.exists(timeout = 5000),'Switch to create contacts failed in 5s!'
		d(text="姓名").set_text("adele")
		# click the top of screen, prevent the duplication
		d.sleep(1)
		d.click(580,170)
		d(className = 'android.widget.EditText', text="电话").set_text('15050505050')
		d(text = '完成').click.wait()
		assert d(text = '联系人详情').wait.exists(timeout = 5000),'Switch to contacts detail failed in 5s!'
		assert d(text = 'adele').wait.exists(timeout = 5000), 'adele is not show on screen!'

		#Delete contact
		d(text = '删除此联系人').click.wait()
		assert d(textContains = '要删除联系人吗').wait.exists(timeout = 5000),'Delete confirm info does not pop-up in 5s!'
		d(text = '确认删除').click.wait()
		assert d(text = 'adele').wait.gone(timeout = 5000),'Delete contact failed in 5s!'

	def testSwitchMobileNetWorkTo3G(self):
		self._setMobileNetWork('3G')

	def testSwitchMobileNetWorkTo2G(self):
		self._setMobileNetWork('2G')

	def _callDialer(self):
		#Launch call app
		self._launchPhone()

		#Select dialer
		d(text = '拨号').click.wait()
		assert d(resourceId = 'com.android.contacts:id/call_classic').wait.exists(timeout=5000),'Switch to dialer UI failed!'

		#Dial u.getNumber()
		if u.getNumber() == '10010':
			d(description = '一').click.wait()
			d(description = '零').click.wait()
			d(description = '零').click.wait()
			d(description = '一').click.wait()
			d(description = '零').click.wait()
		else:
			d(description = '一').click.wait()
			d(description = '零').click.wait()
			d(description = '零').click.wait()
			d(description = '八').click.wait()
			d(description = '六').click.wait()

		d(resourceId = 'com.android.contacts:id/call_classic').click.wait()

		self._operateDuringCalling()

	def _callCallLog(self):
		# create call log
		self._operateCallLog('add',u.getNumber(),3)
		#Launch call app
		d.start_activity(component='com.android.contacts/.activities.DialtactsActivity')
		assert d(text = '拨号').wait.exists(timeout=5000), 'Launch call app failed in 5s!'

		# select call log
		d(text = '通话记录').click.wait()
		assert d(resourceId = 'com.android.contacts:id/tab_call_log_missed').wait.exists(timeout=5000),'Switch to calllog failed in 5s!'
		d(text = '全部').click.wait()

		#Select call log
		d(textStartsWith = 'Test').click.wait()

		self._operateDuringCalling()

	def _callPhoneBook(self):
		# Before running this test, pls make sure there is 50 contacts in phone book
		# launch call app
		d.start_activity(component='com.android.contacts/.activities.DialtactsActivity')
		assert d(text = '拨号').wait.exists(timeout=5000),'Launch phone failed in 5s!'

		# select phone book
		d(text = '联系人').click.wait()
		assert d(text = '群组').wait.exists(timeout=5000),'Switch to phone book failed in 5s!'
		d(text = '全部').click.wait()

		#Make a MO call to 'Test'
		d(textStartsWith = 'Test')[random.randint(0,4)].click.wait()
		assert d(text = '联系人详情').wait.exists(timeout=5000),'Switch to contacts detail failed in 5s!'
		d(resourceId = 'com.android.contacts:id/fourthly_action_button').click.wait()

		self._operateDuringCalling()


	#Switch between 2G and 3G
	def _setMobileNetWork(self,net):
		d.start_activity(component='com.android.settings/.Settings')
		assert d(text = '设置').wait.exists(timeout=5000), 'Settings application can not be launched'
		
		#Switch to network, and find the network switcher
		d(text = '蜂窝移动数据').click.wait()
		assert d(textContains = '网络').wait.exists(timeout=5000), 'Can not switch the screen to network'

		netSwitcher = d(className = 'android.widget.LinearLayout', resourceId = 'com.android.phone:id/network_mode_switch').child(className = 'smartisanos.widget.SwitchEx')
		#netSwitcher = d(textContains = '使用 3G 网络').sibling(className='android.widget.CheckBox')

		if net == '3G':
			netSwitcher.swipe.right()
		else:
			netSwitcher.swipe.left()

	def _launchPhone(self):
		#Launch phone
		d.start_activity(component='com.android.contacts/.activities.DialtactsActivity')
		assert d(text = '拨号').wait.exists(timeout=5000),'Launch phone failed in 5s!'

	def _makeNumber(self):
		#Random click a number
		dialer_num = ['一', '二','三','四','五','六','七','八','九']
		d(text = '拨号键盘').click.wait()
		d(description = dialer_num[random.randint(0, 8)]).click.wait()

	def _operateDuringCalling(self):
		assert d(text = '结束').wait.exists(timeout=5000),'Switch to dialing failed in 5s!'
		if not d(resourceId = 'com.android.incallui:id/elapsedTime').wait.exists(timeout = 15000):
			d(text = '结束').click.wait()
		assert d(resourceId = 'com.android.incallui:id/elapsedTime').wait.exists(timeout = 15000), 'Calling failed to connect in 15s'
		#Random click a number
		self._makeNumber()

		#Keep calling over 10s
		assert d(textStartsWith = '00:1').wait.exists(timeout=15000), 'Calling finished in 10s.'
		
		#Hangup call
		d(text = '结束').click.wait()

	def _operateCallLog(self,method,content,count):
		'''
		@param method:  add or clear
		@param content: phone number
		@param count:   call number
		'''
		commands.getoutput('adb shell am startservice -a smartisan.datahelper.InitData --es type "CallLog" --es method %s --es content %s --ei count %d'%(method,content,count))

	def _operateContact(self,method,content,count):
		'''
		@param method:  add or clear
		@param content: phone number
		@param count:   call number
		'''
		commands.getoutput('adb shell am startservice -a smartisan.datahelper.InitData --es type "Contact" --es method %s --es content %s --ei count %d'%(method,content,count))