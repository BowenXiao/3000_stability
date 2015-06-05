#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import string
import util as u

class MultiMediaTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		u.tearDown()
		# clear date
		self._clearDate('/sdcard/DCIM/Camera/*')
		self._clearDate('/sdcard/smartisan/Recorder/*')
		# kill recorder
		recorderPID = u.getPID('com.smartisanos.recorder')
		if recorderPID == '':
			pass
		else:
			commands.getoutput('adb shell kill %s'%recorderPID)

	def testRecordVideo(self):
		#Launch camera
		self._launchCamera()

		#Start record video
		d(resourceId = 'com.android.camera2:id/mode_video_hammer').click()
		assert d(resourceId = 'com.android.camera2:id/recording_time').wait.exists(timeout = 5000),'Start recording failed in 5s!'

		#Keep recording 30s
		d.sleep(30)
		assert d(textStartsWith = '00:3').wait.exists(timeout = 5000),'Camera stop recording before 30s!'

		#Stop record
		d(resourceId = 'com.android.camera2:id/mode_video_hammer').click()
		assert d(resourceId = 'com.android.camera2:id/ctrl_btn').wait.exists(timeout = 5000),'Stop recording failed in 5s!'

		#Play the recorded video
		d.sleep(3)  #wait for thumbnail refresh
		d(resourceId = 'com.android.camera2:id/thumbnail').click.wait()#wait for thumbnail refresh
		assert d(resourceId = 'com.android.gallery3d:id/gallery_root').wait.exists(timeout = 6000),'Switch to gallery view failed in 6s!'
		d.sleep(1)
		d.click('Gallery_Play_Icon.png')
		assert d(className = 'android.widget.VideoView').wait.exists(timeout = 5000),'Play video failed in 5s!'
		#play 10s
		d.sleep(10)
		d.press('back')

		#Delete recorded video
		before = commands.getoutput('adb shell ls /sdcard/DCIM/Camera/* | grep mp4 | wc -l')
		#(975,145) is the position of delete icon
		d.click(975,145)
		assert d(textContains = '确认要删除这段视频').wait.exists(timeout = 5000),"Delete confirmation pop-up failed in 5s!"
		d(text = '确认删除').click.wait()
		d.sleep(2)
		after = commands.getoutput('adb shell ls /sdcard/DCIM/Camera/* | grep mp4 | wc -l')
		result = string.atoi(before) - string.atoi(after)
		assert result == 1,'Delete file failed!'

	def testTakePicture(self):
		#Launch camera
		self._launchCamera()

		#Take pics
		d(resourceId = 'com.android.camera2:id/shutter_button').click.wait()
		d.sleep(2)  #wait for thumbnail refresh
		
		#Check Pics
		d(resourceId = 'com.android.camera2:id/thumbnail').click.wait()
		assert d(resourceId = 'com.android.gallery3d:id/gallery_root').wait.exists(timeout = 6000),'Switch to gallery view failed in 6s!'
		
		# delete pics
		before = commands.getoutput('adb shell ls /sdcard/DCIM/Camera/* | grep jpg | wc -l')
		#(975,145) is the position of delete icon
		d.click(975,145)
		d.sleep(1)
		assert d(textContains = '确认要删除这张图片').wait.exists(timeout = 5000),"Delete confirmation pop-up failed in 5s!"
		d(text = '确认删除').click.wait()
		d.sleep(2)
		after = commands.getoutput('adb shell ls /sdcard/DCIM/Camera/* | grep jpg | wc -l')
		result = string.atoi(before) - string.atoi(after)
		assert result == 1,'Delete file failed!'

	def testRecordAudio(self):
		#Launch sound recorder
		d.start_activity(component='com.smartisanos.recorder/.activity.EmptyActivity')
		d.click(880,1545)
		assert d(text = '录音机').wait.exists(timeout = 5000),'Launch sound recorder failed in 5s!'

		#Start record
		for i in range(3):
			if i ==3:
				# kill recorder
				recorderPID = u.getPID('com.smartisanos.recorder')
				commands.getoutput('adb shell kill %s'%recorderPID)
				assert False,'Can not start recording!'
			d(resourceId = 'com.smartisanos.recorder:id/recorder_main_control_record').click()
			if d(resourceId='com.smartisanos.recorder:id/recorder_main_control_mark').enabled:
				break

		#Record 5s
		d.sleep(5)

		#Stop record and then save audio
		d(resourceId = 'com.smartisanos.recorder:id/recorder_main_control_stop').click.wait()
		if not d(text = '命名并保存').exists:
			recorderPID = u.getPID('com.smartisanos.recorder')
			commands.getoutput('adb shell kill %s'%recorderPID)
		assert d(text = '命名并保存').wait.exists(timeout=5000),'Save window does not pop-up in 5s!'
		d(text = '确定').click.wait()

		#Play the recorded video
		d(resourceId = 'com.smartisanos.recorder:id/recorder_main_title_list').click.wait()
		assert d(text = '录音列表').wait.exists(timeout=5000),'Switch audio list failed in 5s!'
		d(resourceId = 'com.smartisanos.recorder:id/list_item_arrow').click.wait()
		assert d(resourceId = 'com.smartisanos.recorder:id/recorder_edit_control_play').wait.exists(timeout=5000),'Switch to audio play view failed in 5s!'
		d(resourceId = 'com.smartisanos.recorder:id/recorder_edit_control_play').click()
		assert d(resourceId = 'com.smartisanos.recorder:id/recorder_edit_control_pause').wait.exists(timeout=5000),'Play audio failed in 5s!'
		#play audio time
		d.sleep(5)

		#Delete audio
		before = commands.getoutput('adb shell ls /sdcard/smartisan/Recorder/* | grep wav | wc -l')
		d(resourceId = 'com.smartisanos.recorder:id/recorder_edit_title_delete').click.wait()
		assert d(textContains = '确认要删除此音频文件').wait.exists(timeout=5000),'Delete confirmation does not pop-up in 5s!'
		d(text = '确认删除').click.wait()
		after = commands.getoutput('adb shell ls /sdcard/smartisan/Recorder/* | grep wav | wc -l')
		result = string.atoi(before) - string.atoi(after)
		assert result == 1,'Delete file failed!'

	def testPlayMusic(self):
		#Launch music player
		d.start_activity(component='com.smartisanos.music/.activities.MusicMain')
		assert d(resourceId = 'com.smartisanos.music:id/ib_right').wait.exists(timeout=5000),'Launch music player failed in 5s!'

		#Select music to play
		d(text = '渴').click.wait()
		d.expect('Pause_Icon.png')
		d.sleep(5)    # play time
		for i in range (50):
			d.click('Music_Next_Icon.png')
			d.sleep(5)
		# stop play
		d.click('Pause_Icon.png')
		assert d(packageName = 'com.smartisanos.music').exists,'Music player is not show on the screen!'

	def _launchCamera(self):
		d.start_activity(component='com.android.camera2/com.android.camera.CameraLauncher')
		assert d(resourceId = 'com.android.camera2:id/shutter_button').wait.exists(timeout = 5000),'Launch camera failed in 5s!'

	def _clearDate(self,path):
		commands.getoutput('adb shell rm -r %s'%path)