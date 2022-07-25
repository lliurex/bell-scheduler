#!/bin/python3

import os
import subprocess
import dbus
import sys
import json

class BellSchedulerPlayer:

	def __init__(self,bellId):

		self.bellId=bellId
		self.configDir=os.path.expanduser("/etc/bellScheduler/")
		self.configFile=os.path.join(self.configDir,"bell_list")

		self.playBell()

	#def__init__

	def playBell(self):

		user=self._getActiveUser()
		playCommand=self._getPlayCommand()

		if user!="":
			cmd="su -l %s -c '%s'"%(user,playCommand)
		else:
			cmd=playCommand

		subprocess.run(cmd,shell=True,check=True)
		sys.exit(0)

	#def playBell

	def _getActiveUser(self):

		user=""
		try:
			bellBus=dbus.SystemBus()
			bellProxy=bellBus.get_object('org.freedesktop.login1','/org/freedesktop/login1')
			dbusBell=dbus.Interface(bellProxy,dbus_interface='org.freedesktop.login1.Manager')
			currentSessions=dbusBell.ListSessions()
			if len(currentSessions)>0:
				for item in currentSessions:
					uid=int(item[0])
					user=str(item[2])
					cmd='loginctl session-status %s | grep "active" | grep -v "grep"'%uid
					p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
					pout=p.communicate()[0].decode()
					if len(pout)>0:
						break
		except Exception as e:
			pass

		if user=="sddm":
			user=""
		return user

	#def _getActiveUser

	def _getPlayCommand(self):

		playCommand=""
		if os.path.exists(self.configFile):
			try:
				f=open(self.configFile)
				bellsConfig=json.load(f)
				for item in bellsConfig:
					if item==str(self.bellId):
						playCommand=bellsConfig[item]["scriptCommand"]
						break
			except Exception as e:
				pass

		return playCommand

	#def _getPlayCommand

#class BellSchedulerPlayer

if __name__=="__main__":

	bellId=sys.argv[1]
	bp=BellSchedulerPlayer(bellId)

