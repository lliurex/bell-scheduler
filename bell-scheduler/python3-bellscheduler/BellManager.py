#!/usr/bin/env python3

import os
import json
import codecs
from mimetypes import MimeTypes
import tempfile
import shutil
import subprocess
import threading
import glob
import random
import urllib.request
import n4d.client
from datetime import datetime, date,timedelta
import copy
import gettext
gettext.textdomain("bell-scheduler")
_ = gettext.gettext


class BellManager(object):

	
	MISSING_BELL_NAME_ERROR=-1
	INVALID_SOUND_FILE_ERROR=-2
	MISSING_SOUND_FILE_ERROR=-3
	INVALID_IMAGE_FILE_ERROR=-4
	MISSING_IMAGE_FILE_ERROR=-5
	MISSING_SOUND_FOLDER_ERROR=-7
	SOUND_FILE_URL_NOT_VALID_ERROR=-8
	RECOVERY_BELLS_CONFIG=-9
	BELLS_WITH_ERRORS=-31
	FOLDER_WITH_INCORRECT_FILES_ERROR=-38
	TIME_OUT_VALIDATION_ERROR=-41
	DAY_NOT_IN_VALIDITY_ERROR=-56

	ACTION_SUCCESSFUL=0
	BELL_REMOVED_SUCCESSFULLY=14
	BELL_EDITED_SUCCESSFULLY=15
	BELL_ACTIVATED_SUCCESSFULLY=16
	BELL_DEACTIVATED_SUCCESSFULLY=17
	BELL_ADDED_SUCCESSFULLY=18
	BELLS_ALREADY_ACTIVATED=53
	BELLS_ALREADY_DEACTIVATED=54
	BELLS_ALREADY_REMOVED=55

	def __init__(self):

		super(BellManager, self).__init__()

		self.dbg=0
		self.credentials=[]
		self.server='localhost'
		self.holidayToken="/etc/bellScheduler/enabled_holiday_token"
		self.bellsConfigData=[]
		self.imgNoDispPath="/usr/lib/python3/dist-packages/bellscheduler/rsrc/image_nodisp.svg"
		self.bannersPath="/usr/share/bell-scheduler/banners"
		self.imagesPath="/usr/local/share/bellScheduler/images"
		self.soundsPath="/usr/local/share/bellScheduler/sounds"
		self.imagesConfigData=[]
		self._getSystemLocale()
		self._getImagesConfig()
		self.initValues()

	#def __init__	

	def createN4dClient(self,ticket):

		ticket=ticket.replace('##U+0020##',' ')
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)

	#def createN4dClient

	def _debug(self,function,msg):

		if self.dbg==1:
			print("[BELLSCHEDULER]: "+ str(function) + str(msg))

	#def _debug	

	def _getSystemLocale(self):

		language=os.environ["LANGUAGE"]

		if language!="":
			tmpLang=language.split(":")
			self.systemLocale=tmpLang[0]
		else:
			self.systemLocale=os.environ["LANG"]

	#def _getSystemLocale	

	def syncWithCron(self):

		result=self.client.BellSchedulerManager.sync_with_cron()
		self._debug("SyncWithCron: ",result)
		return result

	#def syncWithCron

	def readConf(self):
		
		self.loadError=False
		result=self.client.BellSchedulerManager.read_conf()
		self._debug("Read configuration file: ",result)
		self.bellsConfig=result["data"]
		self.bellsConfigData=[]
		if result["status"]:
			self._getBellsConfig()
	
		return result

	#def readConf	

	def _getBellsConfig(self):

		orderBells=self._getOrderBell()

		for item in orderBells:
			soundError=False
			imgError=False
			tmp={}
			search=""
			tmp["id"]=item
			tmp["cron"]=self.formatTime(item)[2]
			search+=tmp["cron"]
			tmp["mo"]=self.bellsConfig[item]["weekdays"]["0"]
			if tmp["mo"]:
				search+=self._getDayToSearch(0)
			tmp["tu"]=self.bellsConfig[item]["weekdays"]["1"]
			if tmp["tu"]:
				search+=self._getDayToSearch(1)
			tmp["we"]=self.bellsConfig[item]["weekdays"]["2"]
			if tmp["we"]:
				search+=self._getDayToSearch(2)
			tmp["th"]=self.bellsConfig[item]["weekdays"]["3"]
			if tmp["th"]:
				search+=self._getDayToSearch(3)
			tmp["fr"]=self.bellsConfig[item]["weekdays"]["4"]
			if tmp["fr"]:
				search+=self._getDayToSearch(4)
			try:
				tmp["validity"]=self.bellsConfig[item]["validity"]["value"]
				search+=tmp["validity"]
				tmp["validityActivated"]=self.bellsConfig[item]["validity"]["active"]
			except:
				tmp["validity"]=""
				tmp["validityActivated"]=False
			if os.path.exists(self.bellsConfig[item]["image"]["path"]):
				tmp["img"]=self.bellsConfig[item]["image"]["path"]
			else:
				imgError=True
				tmp["img"]=self.imgNoDispPath
				self.loadError=True

			tmp["name"]=self.bellsConfig[item]["name"]
			search+=tmp["name"]
			tmpRet=self._loadSoundPath(item)
			tmp["sound"]=tmpRet[1]
			if not tmpRet[0]:
				tmp["bellActivated"]=self.bellsConfig[item]["active"]
			else:
				soundError=True
				self.loadError=True
				tmp["bellActivated"]=False
				self.bellsConfig[item]["active"]=False
				self._saveConf(self.bellsConfig,item,"active")
 
			tmp["metaInfo"]=search
			tmp["isSoundError"]=soundError
			tmp["isImgError"]=imgError

			self.bellsConfigData.append(tmp)

	#def _getBellsConfig

	def _getImagesConfig(self):

		self.imagesConfigData=[]

		tmpFiles=[]
		if os.path.exists(self.bannersPath):
			for item in os.listdir(self.bannersPath):
				tmpFiles.append(item)
			
			tmpFiles.sort()
			for item in tmpFiles:
				tmp={}
				tmp["imageSource"]="%s/%s"%(self.bannersPath,item)
				self.imagesConfigData.append(tmp)

	#def _getImagesConfig

	def initValues(self):

		self.bellToLoad=""
		self.bellCron=[0,0]
		self.bellDays=[False,False,False,False,False]
		self.bellValidityActive=False
		self.bellValidityValue=""
		self.bellValidityRangeOption=True
		self.bellValidityDaysInRange=[]
		self.enableBellValidity=False
		self.bellName=""
		self.bellImage=["stock",1,"/usr/share/bell-scheduler/banners/bell.png",False]
		self.bellSound=["file","",False,True]
		self.bellStartIn=0
		self.bellDuration=0
		self.bellActive=False
		self.currentBellConfig={}
		self.currentBellConfig["hour"]=self.bellCron[0]
		self.currentBellConfig["minute"]=self.bellCron[1]
		self.currentBellConfig["validity"]={}
		self.currentBellConfig["validity"]["active"]=self.bellValidityActive
		self.currentBellConfig["validity"]["value"]=self.bellValidityValue
		self.currentBellConfig["weekdays"]={}
		self.currentBellConfig["weekdays"]["0"]=self.bellDays[0]
		self.currentBellConfig["weekdays"]["1"]=self.bellDays[1]
		self.currentBellConfig["weekdays"]["2"]=self.bellDays[2]
		self.currentBellConfig["weekdays"]["3"]=self.bellDays[3]
		self.currentBellConfig["weekdays"]["4"]=self.bellDays[4]
		self.currentBellConfig["name"]=self.bellName
		self.currentBellConfig["image"]={}
		self.currentBellConfig["image"]["option"]=self.bellImage[0]
		self.currentBellConfig["image"]["path"]=self.imagesConfigData[self.bellImage[1]]["imageSource"]
		self.currentBellConfig["sound"]={}
		self.currentBellConfig["sound"]["option"]=self.bellSound[0]
		self.currentBellConfig["sound"]["path"]=self.bellSound[1]
		self.currentBellConfig["play"]={}
		self.currentBellConfig["play"]["duration"]=self.bellDuration
		self.currentBellConfig["play"]["start"]=self.bellStartIn
		self.currentBellConfig["active"]=self.bellActive
		self.currentBellConfig["soundDefaultPath"]=self.bellSound[3]
	
	#def initValues

	def _loadSoundPath(self,bell):
		
		path=self.bellsConfig[bell]["sound"]["path"]
		option=self.bellsConfig[bell]["sound"]["option"]
		error=False
		
		if option!="url" and option!="urlslist":
			if os.path.exists(path):
				if option=="file":
					file=os.path.basename(path)
					return [error,file]
				else:
					return [error,path]	
			else:
				self.loadError=True
				error=True
				msg=_("ERROR: File or directory not available")
				return [error,msg]	
		else:
			self.loadError=True
			error=True
			msg=_("ERROR: Current option for sound not supported")
			return [error,msg]

	#def _loadSoundPath

	def _getDayToSearch(self,day):

		tmpDay=""
		if day==0:
			tmpDay+=_("Monday")
			tmpDay+=_("M")
			tmpDay+=("Mon")
		elif day==1:
			tmpDay+=_("Tuesday")
			tmpDay+=_("T")
			tmpDay+=_("Tue")
		elif day==2:
			tmpDay+=_("Wednesday")	
			tmpDay+=_("W")
			tmpDay+=_("Wed")
		elif day==3:
			tmpDay+=_("Thursday")
			tmpDay+=_("R")
			tmpDay+=_("Thu")
		elif day==4:
			tmpDay+=_("Friday")
			tmpDay+=_("F")	
			tmpDay+=_("Fri")

		return tmpDay

	#def _getDayToSearch

	def loadBellConfig(self,bellToLoad):

		self.bellToLoad=bellToLoad[0]
		self.currentBellConfig=self.bellsConfig[bellToLoad[0]]
		self.bellCron=[self.currentBellConfig["hour"],self.currentBellConfig["minute"]]
		self.bellDays=[self.currentBellConfig["weekdays"]["0"],self.currentBellConfig["weekdays"]["1"],self.currentBellConfig["weekdays"]["2"],self.currentBellConfig["weekdays"]["3"],self.currentBellConfig["weekdays"]["4"]]
		try:
			self.bellValidityActive=self.currentBellConfig["validity"]["active"]
			self.bellValidityValue=self.currentBellConfig["validity"]["value"]
		except:
			self.currentBellConfig["validity"]={}
			self.currentBellConfig["validity"]["active"]=False
			self.currentBellConfig["validity"]["value"]=""
			self.bellValidityActive=False
			self.bellValidityValue=""
		self.bellValidityDaysInRange=[]
		self._getValidityConfig(self.bellValidityValue)
		self.enableBellValidity=self.areDaysChecked(self.currentBellConfig["weekdays"])
		self.bellName=self.currentBellConfig["name"]
		if self.currentBellConfig["image"]["option"]=="stock":
			imgIndex=self._getImageIndexFromPath(self.currentBellConfig["image"]["path"])
		else:
			imgIndex=1
		self.bellImage=[self.currentBellConfig["image"]["option"],imgIndex,self.currentBellConfig["image"]["path"],bellToLoad[1]]

		tmpSoundPath=self.currentBellConfig["sound"]["path"]
		soundDefaultPath=True
		if self.currentBellConfig["sound"]["option"]=="file":
			if self.soundsPath not in tmpSoundPath:
				soundDefaultPath=False
		self.bellSound=[self.currentBellConfig["sound"]["option"],tmpSoundPath,bellToLoad[2],soundDefaultPath]
		self.bellStartIn=self.currentBellConfig["play"]["start"]
		self.bellDuration=self.currentBellConfig["play"]["duration"]
		self.bellActive=self.currentBellConfig["active"]
		self.currentBellConfig["soundDefaultPath"]=soundDefaultPath

	#def loadBellConfig

	def _getImageIndexFromPath(self,imagePath):

		for i in range(len(self.imagesConfigData)):
			if self.imagesConfigData[i]["imageSource"]==imagePath:
				return i

	#def _getImageIndexFromPath

	def _getValidityConfig(self,validityInfo):

		tmpValue=validityInfo

		if tmpValue!="":
			if "-" in tmpValue:
				self.bellValidityRangeOption=True
				self.bellValidityDaysInRange=self.getDaysInRange(tmpValue)
			else:
				self.bellValidityRangeOption=False
				self.bellValidityDaysInRange.append(tmpValue)

	#def _getValidityConfig

	def areDaysChecked(self,daysSelected):

		for item in range(len(daysSelected)):
			if daysSelected[str(item)]:
				return True
		
		return False

	#def areDaysChecked
	
	def _saveConf(self,info,last_change,action):

		self.bellsConfig=info
		change=str(last_change)
				
		result=self.client.BellSchedulerManager.save_changes(info,change,action)
		self._debug("Save configuration file: ",result)
		return result

	#def _saveConf		

	def checkData(self,data):
		
		checkValidity=None
		checkImage={"result":True,"code":"","data":""}
		checkSound={"result":True,"code":"","data":""}

		if data["name"]=="":
			return {"result":False,"code":BellManager.MISSING_BELL_NAME_ERROR,"data":""}

		if data["validity"]["active"]:
			checkValidity=self.checkValidity(data["weekdays"],data["validity"]["value"])
		
		if checkValidity==None:
			if data["image"]["option"]=="custom":
				if data["image"]["path"]!="":
					checkImage=self.checkMimetypes(data["image"]["path"],"image")
				else:
					return {"result":False,"code":BellManager.MISSING_IMAGE_FILE_ERROR,"data":""}
			
			if checkImage["result"]:
				if data["sound"]["option"]=="file":
					if data["sound"]["path"]!="":
						checkSound=self.checkMimetypes(data["sound"]["path"],"audio")
						
						if checkSound["result"]:
							return self.checkAudiofile(data["sound"]["path"],"file")
						else:
							return checkSound
					else:
						return {"result":False,"code":BellManager.MISSING_SOUND_FILE_ERROR,"data":""}

				elif data["sound"]["option"]=="directory":
					if data["sound"]["path"]=="":
						return {"result":False,"code":BellManager.MISSING_SOUND_FOLDER_ERROR,"data":""}
					else:
						self.correctFiles=0
						return self.checkDirectory(data["sound"]["path"])	
					
			else:
				return checkImage
		else:
			return checkValidity			
	
	#def checkData

	def checkMimetypes(self,file,check):

		mime = MimeTypes()
		fileMimeType= mime.guess_type(file)
		error=False
		
		if check=="audio":
			if fileMimeType[0]!=None:
				if not 'audio' in fileMimeType[0] and not 'video' in fileMimeType[0]:
					error=True
			else:
				error=True
		else:
			if fileMimeType[0]!=None:
				if not 'image' in fileMimeType[0]: 
					error=True
			else:
				error=True

		if error:
			if check=="audio":
				return {"result":False,"code":BellManager.INVALID_SOUND_FILE_ERROR,"data":""}
			else:
				return {"result":False,"code":BellManager.INVALID_IMAGE_FILE_ERROR,"data":""}
		else:
			return {"result":True,"code":"","data":""}

	#def checkMimetypes			
				
	def checkAudiofile(self,file,type):
		
		params=' -show_entries stream=codec_type,duration -of compact=p=0:nk=1'
		
		if type=="file":
			cmd='ffprobe -i "'+file +'"'+ params
		else:
			cmd='ffprobe -i $(youtube-dl -g "'+file+'" |sed -n 2p) '+params

			
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()[0]
		
		if len(poutput)==0:
			return {"result":False,"code":BellManager.SOUND_FILE_URL_NOT_VALID_ERROR,"data":""}	
		else:
			return {"result":True,"code":BellManager.ACTION_SUCCESSFUL,"data":""}
	
	#def checkAudiofile	

	def checkDirectory(self,directory):

		path=directory+"/*"
		contentDirectory=glob.glob(path)
		for item in contentDirectory:
			if os.path.isfile(item):
				checkFile=self.checkMimetypes(item,"audio")
				if checkFile["result"]:
					checkRun=self.checkAudiofile(item,'file')
					if checkRun["result"]:
						self.correctFiles+=1
			else:
				if os.path.isdir(item):
					self.checkDirectory(item)			
		
		if self.correctFiles>0:
			return {"result":True,"code":BellManager.ACTION_SUCCESSFUL,"data":""}
		else:
			return {"result":False,"code":BellManager.FOLDER_WITH_INCORRECT_FILES_ERROR,"data":""}

	#def checkDirectory		

	def saveData(self,data):

		ret=[False,""]
		origImgPath=""
		origSoundPath=""
		activeBell=False
		bellsConfig=copy.deepcopy(self.bellsConfig)
		orderKeys=[]

		if self.bellToLoad!="":
			order=self.bellToLoad
			action="edit"
		else:
			if len(bellsConfig)>0:
				keys=bellsConfig.keys()
				for item in keys:
					orderKeys.append(int(item))

				order=str(int(max(orderKeys))+1)
			else:
				order="1"

			action="add"

		bellsConfig[order]={}
		bellsConfig[order]["hour"]=data["hour"]
		bellsConfig[order]["minute"]=data["minute"]
		bellsConfig[order]["weekdays"]=data["weekdays"]
		
		if data["validity"]["value"]=="":
			data["validity"]["active"]=False

		bellsConfig[order]["validity"]=data["validity"]
		bellsConfig[order]["name"]=data["name"]

		if data["image"]["option"]=="custom":
			origImgPath=data["image"]["path"]
			destImgPath=os.path.join(self.imagesPath,os.path.basename(origImgPath))
			data["image"]["path"]=destImgPath

		bellsConfig[order]["image"]=data["image"]

		if data["sound"]["option"]=="file":
			if data["soundDefaultPath"]:
				origSoundPath=data["sound"]["path"]
				destSoundPath=os.path.join(self.soundsPath,os.path.basename(origSoundPath))
				data["sound"]["path"]=destSoundPath

		bellsConfig[order]["sound"]=data["sound"]

		bellsConfig[order]["play"]=data["play"]

		if self.areDaysChecked(data["weekdays"]):
			if action=="edit":
				activeBell=data["active"]
			else:
				activeBell=True
		else:
			activeBell=False

		bellsConfig[order]["active"]=activeBell
		retCopy=self._copyMediaFiles(origImgPath,origSoundPath)

		if retCopy["status"]:
			retSave=self._saveConf(bellsConfig,order,action)
			if retSave["status"]:
				retReadConfig=self.readConf()
				if retReadConfig["status"]:
					if action=="edit":
						ret=[True,BellManager.BELL_EDITED_SUCCESSFULLY]
					else:
						ret=[True,BellManager.BELL_ADDED_SUCCESSFULLY]
				else:
					ret=[False,retReadConfig["code"]]
			else:
				ret=[False,retSave["code"]]
		else:
			ret=[False,retCopy["code"]]	

		return ret	

	#def saveData

	def changeBellStatus(self,allBells,active,bellToEdit=None):

		if allBells:
			if self._checkBellStatus(active):
				retChangeStatus=self.changeActivationStatus(active)
				if retChangeStatus['status']:
					retReadConfig=self.readConf()
					if retReadConfig["status"]:
						return [True,retChangeStatus["code"]]
					else:
						return [False,retReadConfig["code"]]
				else:
					return [False,retChangeStatus["code"]]
			else:
				if active:
					return [True,BellManager.BELLS_ALREADY_ACTIVATED]
				else:
					return [True,BellManager.BELLS_ALREADY_DEACTIVATED]
		else:
			self.bellsConfig[bellToEdit]["active"]=active
			ret=self._saveConf(self.bellsConfig,bellToEdit,"active")

			if ret["status"]:
				self._updateBellsConfigData("bellActivated",active,bellToEdit)
				if active:
					return [True,BellManager.BELL_ACTIVATED_SUCCESSFULLY]
				else:
					return [True,BellManager.BELL_DEACTIVATED_SUCCESSFULLY]
			else:
				return [False,ret["code"]]

	#def changeBellStatus

	def _checkBellStatus(self,active):

		if len(self.bellsConfig)>0:
			for item in self.bellsConfig:
				if self.bellsConfig[item]["active"]!=active:
					return True
		return False			

	#def _checkBellStatus

	def _updateBellsConfigData(self,param,value,bellId):

		for item in self.bellsConfigData:
			if item["id"]==bellId:
				if item[param]!=value:
					item[param]=value
				break

	#def _updateBellsConfigData

	def removeBell(self,allBells,bellToRemove=None):

		if allBells:
			if len(self.bellsConfig)>0:
				retRemove=self._removeAllBells()
				if retRemove['status']:
					retReadConfig=self.readConf()
					if retReadConfig["status"]:
						return [True,retRemove["code"]]
					else:
						return [False,retReadConfig["code"]]
				else:
					return [False, retRemove["code"]]
			else:
				return [True,BellManager.BELLS_ALREADY_REMOVED]
		else:
			bellsConfig=copy.deepcopy(self.bellsConfig)
			bellsConfig.pop(bellToRemove)
			ret=self._saveConf(bellsConfig,bellToRemove,"remove")

			if ret["status"]:
				self.bellsConfig=bellsConfig
				for i in range(len(self.bellsConfigData)-1,-1,-1):
					if self.bellsConfigData[i]["id"]==bellToRemove:
						self.bellsConfigData.pop(i)
						break
				return [True,BellManager.BELL_REMOVED_SUCCESSFULLY]
			else:
				return [False,ret["code"]]

	#def removeBell

	def _getOrderBell(self,info=None):
	
		tmp=[]
		orderBells=[]
		currentDay=date.today().strftime('%d/%m/%Y')
		if info==None:
			if len(self.bellsConfig)>0:
				for item in self.bellsConfig:
					time=str(self.bellsConfig[item]["hour"])+":"+str(self.bellsConfig[item]["minute"])
					time_f=datetime.strptime(time,"%H:%M")
					try:
						if (self.bellsConfig[item]["validity"]["value"]!=""):
							if "-" in self.bellsConfig[item]["validity"]["value"]:
								dateToFormat=self.bellsConfig[item]["validity"]["value"].split("-")[0]
								datef=datetime.strptime(dateToFormat,"%d/%m/%Y")
							else:
								dateToFormat=self.bellsConfig[item]["validity"]["value"]
								datef=datetime.strptime(dateToFormat,"%d/%m/%Y")
						else:
							datef=datetime.strptime(currentDay,"%d/%m/%Y")
					except:
						datef=datetime.strptime(currentDay,"%d/%m/%Y")

					x=()
					x=item,time_f,datef
					tmp.append(x)
		else:
			
			for item in info:
				time=str(info[item]["hour"])+":"+str(info[item]["minute"])
				time_f=datetime.strptime(time,"%H:%M")
				try:
					if (info[item]["validity"]["value"]!=""):
						if "-" in info[item]["validity"]["value"]:
							dateToFormat=info[item]["validity"]["value"].split("-")[0]
							datef=datetime.strptime(dateToFormat,"%d/%m/%Y")
						else:
							dateToFormat=info[item]["validity"]["value"]
							datef=datetime.strptime(dateToFormat,"%d/%m/%Y")
					else:
						datef=datetime.strptime(currentDay,"%d/%m/%Y")
				except:
					datef=datetime.strptime(currentDay,"%d/%m/%Y")
				x=()
				x=item,time_f,datef
				tmp.append(x)		

		tmp.sort(key=lambda bell:(bell[1],bell[2]))
		for item in tmp:
			orderBells.append(item[0])

		return orderBells	

	#def _getOrderBells
	
	def formatTime(self,item):
	
		time=[]
		hour=self.bellsConfig[item]["hour"]
		minute=self.bellsConfig[item]["minute"]

		if hour<10:
			hour='0'+str(hour)

		if minute<10:
			minute='0'+str(minute)

		cron=str(hour)+":"+str(minute)
		time=[hour,minute,cron]
		return time		

	#def formatTime	

	def _copyMediaFiles(self,image,sound):

		result=self.client.BellSchedulerManager.copy_media_files(image,sound)
		self._debug("Copy Media files: ",result)
		return result

	#def _copyMediaFiles	

	def exportBellsConfig(self,destFile):

		user=os.environ["USER"]
		result=self.client.BellSchedulerManager.export_bells_conf(destFile,user)
		self._debug("Export bells conf : ",result)
		
		return result

	#def exportBellsConf

	def importBellBackup(self,origFile):

		backup=True
		resultImport=self._importBellsConfifg(origFile,backup)

		if resultImport['status']:
			retReadConfig=self.readConf()
			if retReadConfig["status"]:
				return [True,resultImport["code"]]
			else:
				return [False,retReadConfig["code"]]
		else:
			return [False,resultImport["data"]]

	#def importBellBackup

	def _importBellsConfifg(self,origFile,backup):
		
		user=os.environ["USER"]
		result=self.client.BellSchedulerManager.import_bells_conf(origFile,user,backup)
		self._debug("Import bells config: ",result)	
		
		return result

	#def importBellsConfig

	def recoveryBellBackup(self,origFile):

		backup=False
		resultRecovery=self._recoveryBellsConfig(origFile,backup)
		retReadConfig=self.readConf()
		if resultRecovery["status"]:
			if retReadConfig["status"]:
				return [False,BellManager,RECOVERY_BELLS_CONFIG]
			else:
				return [False,retReadConfig["code"]]
		else:
			return [False,resultRecovery["code"]]

	#def recoveryBellBackup

	def _recoveryBellsConfig(self,origFile,backup):
		
		user=os.environ["USER"]
		result=self.client.BellSchedulerManager.import_bells_conf(origFile,user,backup)
		self._debug("Recovery bells config: ",result)	
		
		return result

	#def recoveryBellsConfig	

	def changeActivationStatus(self,active):

		if active:
			action="activate"
		else:
			action="deactivate"

		result=self.client.BellSchedulerManager.change_activation_status(action)
		self._debug("Activation/Deactivation process: ",result)	
		
		return result

	#def changeActivationStatus	

	def _removeAllBells(self):

		result=self.client.BellSchedulerManager.remove_all_bells()
		self._debug("Remove all bells process: ",result)	
		
		return result

	#def removeAllBells

	def checkValidity(self,weekdays,validity):

		daysInValidity=[]
		weekdaysSelected=[]
		weekdaysValidity=[]
		noMatchDay=0
		
		if validity!="":
			daysInValidity=self.getDaysInRange(validity)
	
			for item in daysInValidity:
				tmpDay=datetime.strptime(item,"%d/%m/%Y")
				tmpWeekday=tmpDay.weekday()
				if tmpWeekday not in weekdaysValidity:
					weekdaysValidity.append(tmpWeekday)

			for i in range(len(weekdays)):
				if weekdays[str(i)]:
					weekdaysSelected.append(i)

			for item in weekdaysSelected:
				if item not in weekdaysValidity:
					noMatchDay+=1

			if noMatchDay>0:
				return {"result":False,"code":BellManager.DAY_NOT_IN_VALIDITY_ERROR,"data":""}

	#def checkValidity

	def getDaysInRange(self,day):	

		listDays=[]
		if day!="":
			if "-" in day:
				tmp=day.split("-")
				date1=datetime.strptime(tmp[0],'%d/%m/%Y')
				date2=datetime.strptime(tmp[1],'%d/%m/%Y')
			else:
				date1=datetime.strptime(day,'%d/%m/%Y')
				date2=date1
			delta=date2-date1
			for i in range(delta.days + 1):
				tmpDay=(date1 + timedelta(days=i)).strftime('%d/%m/%Y')
				listDays.append(tmpDay)

		return listDays	

	#def getDaysInRange

	def checkGlobalOptionStatus(self):

		if len(self.bellsConfig)>0:
			return True
		else:
			return False
			
	#def checkGlobalOptionStatus

	def checkIfAreBellsWithDirectory(self):

		for item in self.bellsConfig:
			if self.bellsConfig[item]["sound"]["option"]=="directory":
				return True

		return False

	#def checkIfAreBellsWithRandom

	def checkHolidayManagerStatus(self):

		if os.path.exists(self.holidayToken):
			return True
		else:
			return False

	#def checkHolidayManagerStatus

	def enableHolidayControl(self,action):

		result=self.client.BellSchedulerManager.enable_holiday_control(action)
		self._debug("Enable holiday control: ",result)	
		
		return result

	#def enableHolidayControl

	def checkChangeStatusBellsOption(self):

		allActivated=False
		allDeactivated=False
		enableStatusFilter=True
		countActivated=0
		countDeactivated=0
		result=[]
		
		if len(self.bellsConfig)>0:
			for item in self.bellsConfig:
				if self.bellsConfig[item]['active']:
					countActivated+=1
				else:
					countDeactivated+=1

			if countActivated==0:
				allDeactivated=True
				enableStatusFilter=False

			if countDeactivated==0:
				allActivated=True
				enableStatusFilter=False
		else:
			enableStatusFilter=False

		result=[allActivated,allDeactivated,enableStatusFilter]

		return result

	#def checkChangeStatusBellsOption	

#class BellManager 		
