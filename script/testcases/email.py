#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import util as u

ACCOUNT = 'stabilitymailpost@smartisan.com'
PASSWORD = 'Smartisantest011'
SEND_TO = 'stabilitymailget@smartisan.com'
#SEND_TO = 'smartisanauto@hotmail.com'
SUBJECT = 'Test Send Email'
ATT_SUBJECT = 'Send With Attachment'
NOATT_SUBJECT = 'Send Without Attachment'
BODY = 'This mail is send by autotest'

#commands.getoutput('adb shell am startservice -a smartisan.datahelper.InitData --es type "Email" --es method "add" ')

class EmailTest(unittest.TestCase):
	def setUp(self):
		d.watcher("IGNORE_DRAFT").when(textContains='是否保存草稿').click(text='不保存草稿')
		u.setUp()

	def tearDown(self):
		d.watchers.remove("IGNORE_DRAFT")
		u.tearDown()

	def testClearAccount(self):
		commands.getoutput('adb shell am startservice -a smartisan.datahelper.InitData --es type "Email" --es method "clear" ')

	def testLogInAccount(self):
		self._launchEmail()

	def testInsertAccount(self):
		# Insert Email account
		commands.getoutput('adb shell am startservice -a smartisan.datahelper.InitData --es type "Email" --es method "add" ')

	def testSendEmailNoAtt(self):
		#Launch Email
		self._launchEmail()

		#Edit mail content and then send out
		d(resourceId = 'com.android.email:id/compsoe_view').click.wait()
		assert d(text = '写邮件').wait.exists(timeout = 5000),'Switch to compose view failed in 5s!'
		d(resourceId = 'com.android.email:id/to_recipient_view').set_text(SEND_TO)
		d.press('enter')
		d(resourceId = 'com.android.email:id/subject').set_text(SUBJECT)
		d(resourceId = 'com.android.email:id/body').set_text(BODY)
		d(text = '发送').click.wait()
		assert d(text = '设置').wait.exists(timeout = 5000),'Switch to mail list (after click send icon) failed in 5s!'

		#Delete mail from sendbox
		d(resourceId = 'com.android.email:id/options_view').click.wait()
		assert d(resourceId = 'com.android.email:id/bottom_dialog_title_text',text = 'Exchange').wait.exists(timeout = 5000),'Trigger menu list failed in 5s!'
		d(text = '已发送邮件').click.wait()
		assert d(resourceId = 'com.android.email:id/title',text = '已发送邮件').wait.exists(timeout = 5000),'Switch to sended box failed in 5s!'
		# looping 60s to check if mail sending finished
		for i in range(12):
			d(resourceId = 'com.android.email:id/refresh_view').click.wait()
			if d(descriptionContains = SUBJECT).wait.exists(timeout=5000):
				break
			if i == 11:
				assert False, 'Can not send out email in 60s. '
		d(descriptionContains = SUBJECT).click.wait()
		assert d(resourceId = 'com.android.email:id/send_calendar_btn').wait.exists(timeout = 5000),'Open mail failed in 5s!'
		d(resourceId = 'com.android.email:id/detail_delete_view').click.wait()
		d(text = '确认删除').click.wait()
		assert d(text = '已发送邮件').wait.exists(timeout = 5000),'Switch to sending box failed (after delete send mail) in 5s!'

	def testReadEmailNoAtt(self):
		#Launch Email
		self._launchEmail()

		#Get into star box
		d(resourceId = 'com.android.email:id/options_view').click.wait()
		assert d(resourceId = 'com.android.email:id/bottom_dialog_title_text').wait.exists(timeout = 5000),'Pop-up menu list failed in 5s!'
		d(text = '已加旗标').click.wait()
		assert d(resourceId = 'com.android.email:id/title',text = '已加旗标').wait.exists(timeout = 5000),'Switch Star box failed in 5s!'

		#Open and read mail
		for i in range(60):
			d.sleep(1)
			if d(descriptionContains = NOATT_SUBJECT).exists:
				break
			d(resourceId = 'com.android.email:id/refresh_view').click.wait()
		assert d(descriptionContains = NOATT_SUBJECT).exists,'Do not received mail!'
		# check received mail
		d(descriptionContains = NOATT_SUBJECT).click()
		assert d(resourceId = 'com.android.email:id/send_calendar_btn').wait.exists(timeout = 5000),'Switch to mail detail failed in 5s!'

	def testSendEmailWithAtt(self):
		#Launch Email
		self._launchEmail()

		#Edit mail content
		d(resourceId = 'com.android.email:id/compsoe_view').click.wait()
		assert d(text = '写邮件').wait.exists(timeout = 5000),'Switch to compose view failed in 5s!'
		d(resourceId = 'com.android.email:id/to_recipient_view').set_text(SEND_TO)
		d.press('enter')
		d(resourceId = 'com.android.email:id/subject').set_text(SUBJECT)
		d(resourceId = 'com.android.email:id/body').set_text(BODY)

		#Add attachment and then send out
		d(resourceId = 'com.android.email:id/compose_attach').click.wait()
		assert d(text = '选择应用添加附件').wait.exists(timeout = 5000),"'选择应用添加附件' does not pop-up in 5s!"
		d(text = '相册').click.wait()
		assert d(packageName = 'com.android.gallery3d').wait.exists(timeout = 5000),'Switch to gallery view failed in 5s!'
		d.sleep(3)
		# select pics as attachment
		d.click('Attachment_Into_RootDir.png')
		#d.sleep(1)
		d.click('Attachment_Pics.png')
		#d.sleep(1)
		d(text = '发送').click.wait()
		#d.sleep(1)
		assert d(text = '设置').wait.exists(timeout = 5000),'Switch to mail list (after click send icon) failed in 5s!'

		#Delete mail from sendbox
		d(resourceId = 'com.android.email:id/options_view').click.wait()
		assert d(resourceId = 'com.android.email:id/bottom_dialog_title_text',text = 'Exchange').wait.exists(timeout = 5000),'Trigger menu list failed in 5s!'
		d(text = '已发送邮件').click.wait()
		assert d(resourceId = 'com.android.email:id/title',text = '已发送邮件').wait.exists(timeout = 5000),'Switch to sended box failed in 5s!'
		# looping 60s to check if mail sending finished
		for i in range(12):
			d.sleep(5)
			if d(descriptionContains = 'Auto Send.').exists:
				break
			d(resourceId = 'com.android.email:id/refresh_view').click.wait()
		assert d(descriptionContains = BODY).wait.exists(timeout = 1000),'Send mail does not show in send box in 5s!'
		d(descriptionContains = BODY).click.wait()
		assert d(resourceId = 'com.android.email:id/send_calendar_btn').wait.exists(timeout = 5000),'Open mail failed in 5s!'
		d(resourceId = 'com.android.email:id/detail_delete_view').click.wait()
		d(text = '确认删除').click.wait()
		assert d(text = '已发送邮件').wait.exists(timeout = 5000),'Switch to sending box failed (after delete send mail) in 5s!'

	def testReadEmailWithAtt(self):
		#Launch Email
		self._launchEmail()

		#Get into star box
		d(resourceId = 'com.android.email:id/options_view').click.wait()
		#assert d(resourceId = 'com.android.email:id/bottom_dialog_title_text').wait.exists(timeout = 5000),'Pop-up menu list failed in 5s!'
		d(text = '已加旗标').click.wait()
		assert d(resourceId = 'com.android.email:id/title',text = '已加旗标').wait.exists(timeout = 5000),'Switch Star box failed in 5s!'

		# check inbox
		for i in range(30):
			d.sleep(1)
			if d(descriptionContains = ATT_SUBJECT).exists:
				break
			d(resourceId = 'com.android.email:id/refresh_view').click.wait()
		# check received mail
		assert d(descriptionContains = ATT_SUBJECT).exists,'Do not received mail!'
		d(descriptionContains = ATT_SUBJECT).click()
		assert d(resourceId = 'com.android.email:id/send_calendar_btn').wait.exists(timeout = 5000),'Switch to mail detail failed in 5s!'
		# check attachment
		if  d(text = '下载').exists:
			d(text = '下载').click.wait()
		assert d(text = '打开').wait.exists(timeout = 15000),'Download attachment failed in 15s!'
		d(text = '打开').click.wait()
		assert d(text = '选择要使用的应用').wait.exists(timeout = 5000),"'选择要使用的应用' does not pop up in 5s!"
		d(text = '相册').click.wait()
		assert d(packageName = 'com.android.gallery3d').wait.exists(timeout = 5000),'Switch to gallery view failed in 5s!'

	def testLogOutAccount(self):
		self._clearAccount()

	def _launchEmail(self):
		#Launch Email
		d.start_activity(component='com.android.email/.activity.Welcome')
		d.sleep(1)
		#Check if login account is needed.
		if d(text = '添加账户').exists:
			self._loginAccount()
		else:
			pass
		assert d(resourceId = 'com.android.email:id/subtitle',text = 'Exchange').wait.exists(timeout = 10000),'Launch email failed in 10s!'

	def _loginAccount(self):
		# select exchage
		d(resourceId = 'com.android.email:id/perset_exchange').click.wait()
		d(resourceId = 'com.android.email:id/account_email').set_text(ACCOUNT)
		d(resourceId = 'com.android.email:id/account_password').set_text(PASSWORD)
		d(text = '下一步').click.wait()
		if d(text = '远程安全管理').wait.exists(timeout = 10000):
			d(text = '确定').click.wait()
			if d(text = '要激活设备管理器吗？').wait.exists(timeout = 5000):
				d(text = '激活').click.wait()
		d(resourceId = 'com.android.email:id/subtitle',text = 'Exchange').wait.exists(timeout = 120000)

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

	def _clearAccount(self):
		commands.getoutput('adb shell am start -n com.android.settings/.Settings')
		self._selectOption('高级设置')
		self._selectOption('账户和同步')
		if d(text = 'Exchange').exists:
			d(text = 'Exchange').click.wait()
			d(text = '账户设置').click.wait()
			d(text = 'Exchange').click.wait()
			d(text = '删除此账户').click.wait()
			d(text = '确认删除').click.wait()
		else:
			pass
