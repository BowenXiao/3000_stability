#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import string

def getNumber():
	#For UC
	#return '10010'

	#For CMCC
	return '10086'

def unlock():
	'''
	unlock() 解锁屏幕，黑屏或其他状态解锁屏幕。
	return boolean
	'''
	d.wakeup()
	lockscreen = d(className = 'android.widget.ImageView',resourceId = 'com.smartisanos.keyguard:id/desk_kg')
	if lockscreen.exists:
		x = d.info['displayWidth']
		y = d.info['displayHeight']
		d.swipe(x/2,int(y/1.5),x/2,0,20)
		if not lockscreen.exists:
			return True
		else:
			return False
def setUp():
	# unlock screen
	unlock()
	for i in xrange(2):
		d.press('back')
	d.press('home')
	d.sleep(1)
	# clear logcat
	commands.getoutput('adb shell logcat -c')
	d.sleep(1)
	registerSysWatchers()

def tearDown():
	for i in xrange(2):
		d.press('back')
	if d(textContains = '退出').exists:
		d(text = '确定').click()
	d.press('home')
	checkSystemWatchers()
	#d.press('recent')
	#d.sleep(1)
	#if  d(resourceId = 'com.smartisanos.systemui:id/clear_all_task').exists:
	#	d(resourceId = 'com.smartisanos.systemui:id/clear_all_task').click.wait()
	#else:
	#	d.press('home')

def registerSysWatchers():
	d.watchers.reset()
	d.watchers.remove()
	d.watcher("IGNORE_ANR").when(textContains='无响应').click(text='确定')
	d.watcher("IGNORE_CRASH").when(textContains='停止运行').click(text='确定')

def checkSystemWatchers():
	if d.watcher("IGNORE_ANR").triggered:
		raise Exception('AUTO_FC_WHEN_ANR')
	if d.watcher("IGNORE_CRASH").triggered:
		raise Exception('IGNORE_CRASH')
	d.watchers.reset()
	d.watchers.remove()

def getFileCount(folder, ext):
	cmd = 'adb shell ls %s | grep .%s'%(folder, ext)
	r = commands.getoutput(cmd)
	rl = r.split('\n')
	if rl[0] == '':
		return 0
	else:
		return len(rl)

def getPID(name):
	pid = commands.getoutput("adb shell ps | grep %s | awk '{print $2}'"%name)
	return pid
