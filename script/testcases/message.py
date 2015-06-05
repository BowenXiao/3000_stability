#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import util as u
# Send Item
SMS_MAX_CONTENT = 'AutoTestContentAutoTestContentAutoTestContentAutoTestContentAutoTestContentAutoTestContentAutoTestContentAutoTestContentAutoTestContentAutoTestContent'
MMS_RECEIVER	= '15650790637'
MMS_VIDEO_CONT	= 'Test MMS With Video'
MMS_PICS_CONT	= 'Test MMS With PICS'

#Read Item
SMS_SENDER_INSERT			= '\"156 1234 9876\"'
SMS_CONT_INSERT				= '\"Test SMS\"'
SMS_SENDER					= '156 1234 9876'
SMS_CONT					= 'Test SMS'
MMS_PICS_SENDER 			= '150 0845 5658'
MMS_VIDEO_SENDER 			= '151 0845 5658'
MMS_PICS_SENDER_INSERT 		= '\"150 0845 5658\"'
MMS_VIDEO_SENDER_INSERT		= '\"151 0845 5658\"'
MMS_VIDEO_CONT_INSERT		= '\"Test MMS With Video\"'
MMS_PICS_CONT_INSERT		= '\"Test MMS With PICS\"'

class MessageTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		u.tearDown()

	def testSendSMSWithMaxChar(self):
		#Launch message app and enter new message screen
		self._launchAndEnterNewMsg()

		#Input receiver and content
		self._editTestContent(u.getNumber(),SMS_MAX_CONTENT)
		
		#Send SMS
		self._sendMessage()

	def testSendMMSWithVideo(self):
		#Launch message app and enter new message screen
		self._launchAndEnterNewMsg()

		#Input receiver and text content
		self._editTestContent(MMS_RECEIVER,MMS_VIDEO_CONT)
		
		#Add video as attachment
		d(resourceId = 'com.android.mms:id/input_extention').click.wait()
		# (120,1830) is the positon of '照片和视频'
		d.click(120,1830)
		assert d(text = '请选择操作').wait.exists(timeout = 5000),"Trigger '照片和视频' failed in 5s!"
		d(text = '选取视频').click.wait()
		assert d(packageName = 'com.android.gallery3d').wait.exists(timeout = 5000),'Switch to gallery view failed in 5s!'
		# (800,1825) is the position of '所有相册'
		d.click(800,1825)
		# select '根目录'
		d.click('MMS_Into_RootDir.png')
		d.sleep(1)
		# (100,350) is the positon of video attachment
		d.click(100,350)

		#Send MMS
		self._sendMessage()

	def testSendMMSWithPics(self):
		#Launch message app and enter new message screen
		self._launchAndEnterNewMsg()

		#Input receiver and text content
		self._editTestContent(MMS_RECEIVER,MMS_PICS_CONT)

		#Add pics as attachment
		d(resourceId = 'com.android.mms:id/input_extention').click.wait()
		# (120,1830) is the positon of '照片和视频'
		d.click(120,1830)
		assert d(text = '请选择操作').wait.exists(timeout = 5000),"Trigger '照片和视频' failed in 5s!"
		d(text = '选取照片').click.wait()
		assert d(packageName = 'com.android.gallery3d').wait.exists(timeout = 5000),'Switch to gallery view failed in 5s!'
		# (800,1825) is the position of '所有相册'
		d.click(800,1825)
		# select '根目录'
		d.click('MMS_Into_RootDir.png')
		d.sleep(1)
		d.click('MMS_Pics.png')

		#Send MMS
		self._sendMessage()

	def testReadSMS(self):
		# insert SMS
		self._insertSMS(SMS_SENDER_INSERT,SMS_CONT_INSERT)
		#Launch message
		d.start_activity(component='com.android.mms/.ui.ConversationList')
		assert d(text = '短信').wait.exists(timeout = 5000),'Launch message failed in 5s!'

		#Read a SMS
		d(text = SMS_CONT).click.wait()
		assert d(resourceId = 'com.android.mms:id/text_view',text = SMS_CONT).wait.exists(timeout = 5000),'There is no text view, read SMS failed is 5s!'

	def testReadMMSPics(self):
		# insert MMS pics
		self._insertMMS('\"Mms_p\"',MMS_PICS_SENDER_INSERT,MMS_PICS_CONT_INSERT)
		#Launch message
		d.start_activity(component='com.android.mms/.ui.ConversationList')
		assert d(text = '短信').wait.exists(timeout = 5000),'Launch message failed in 5s!'

		#Open and read MMS Pics attachment
		d(text = MMS_PICS_SENDER).click.wait()
		d(resourceId = 'com.android.mms:id/mms_image_view').click.wait()
		#assert d(text = '彩信').wait.exists(timeout = 5000),'Switch to MMS view failed in 5s!'
		if d(resourceId = 'com.android.mms:id/mms_image_part').wait.exists(timeout = 5000):
			d(resourceId = 'com.android.mms:id/mms_image_part').click.wait()
		#d(resourceId = 'com.android.mms:id/mms_image_part').click.wait()
		assert d(packageName = 'com.android.gallery3d').wait.exists(timeout = 5000), 'Read MMS in gallery failed in 5s!'

	def testReadMMSVideo(self):
		# insert MMS video
		self._insertMMS('\"Mms_v\"',MMS_VIDEO_SENDER_INSERT,MMS_VIDEO_CONT_INSERT)
		#Launch message
		d.start_activity(component='com.android.mms/.ui.ConversationList')
		assert d(text = '短信').wait.exists(timeout = 5000),'Launch message failed in 5s!'

		#Open and read MMS video attachment
		d(text = MMS_VIDEO_SENDER).click.wait()
		d(resourceId = 'com.android.mms:id/mms_type_icon').click.wait()
		assert d(text = '彩信').wait.exists(timeout = 5000),'Switch to MMS view failed in 5s!'
		d(resourceId = 'com.android.mms:id/mms_video').click.wait()
		assert d(packageName = 'com.android.gallery3d').wait.exists(timeout = 5000), 'Read MMS in gallery failed in 5s!'

	def _launchAndEnterNewMsg(self):
		#Start message
		d.start_activity(component='com.android.mms/.ui.ConversationList')
		if  d(text = '短信',resourceId = 'com.android.mms:id/button_left').exists:
			d(text = '短信',resourceId = 'com.android.mms:id/button_left').click.wait()
		if  d(text = '返回').exists:
			d(text = '返回').click.wait()
		if  d(resourceId = 'com.android.mms:id/creat_new_message').wait.exists(timeout=1000):
			d(resourceId = 'com.android.mms:id/creat_new_message').click.wait()
		assert d(description='发送').wait.exists(timeout=5000), 'Can not switch to new message screen. '



	def _editTestContent(self,receiver,content):
		#Input receiver and text content
		d(resourceId = 'com.android.mms:id/recipients_edittext',text = '接收者').set_text(receiver)
		d(resourceId = 'com.android.mms:id/embedded_text_editor',text = '键入短信').set_text(content)

	def _sendMessage(self):
		#Send Message
		d(description = '发送').click.wait()
		d(text = '准备发送…').wait.exists(timeout = 5000)
		d(text = '准备发送…').wait.gone(timeout = 10000)
		d.sleep(1)
		assert d(text="发送中…").wait.gone(timeout=60000), 'Send SMS failed in 60s'
		if d(textContains = '发送失败').exists:
			assert False,'Send SMS failed, please check single!'

	def _insertSMS(self,name,content):
		'''
		@param method:  add or clear
		@param content: phone number
		@param count:   call number
		'''
		commands.getoutput('adb shell am startservice -a smartisan.datahelper.InitData --es type "Sms" --es name %s --es content %s'%(name,content))

	def _insertMMS(self,atttype,name,content):
		'''
		@param method:  add or clear
		@param content: phone number
		@param count:   call number
		'''
		commands.getoutput('adb shell am startservice -a smartisan.datahelper.InitData --es type %s --es method "add" --es name %s --es content %s'%(atttype,name,content))