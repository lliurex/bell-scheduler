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
	ERROR_TIMEOUT_EXPIRED=-57
	ERROR_FFPROBE_MISSING=-58

	ACTION_SUCCESSFUL=0
	BELL_REMOVED_SUCCESSFULLY=14
	BELL_EDITED_SUCCESSFULLY=15
	BELL_ACTIVATED_SUCCESSFULLY=16
	BELL_DEACTIVATED_SUCCESSFULLY=17
	BELL_ADDED_SUCCESSFULLY=18
	BELLS_ALREADY_ACTIVATED=53
	BELLS_ALREADY_DEACTIVATED=54
	BELLS_ALREADY_REMOVED=55
	BELL_DUPLICATE=56
	AUDIO_DEVICE_ALREADY_CONFIGURATED=57

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
		self.audioDevicesData=[]
		self.currentAudioDevice=0
		self.enableAudioDeviceConfiguration=False
		self.isAudioDeviceConfigurated=False
		self._getSystemLocale()
		self._getImagesConfig()
		self._getAudioDevices()
		self.initValues()

	#def __init__	

	def createN4dClient(self,ticket):

		ticket=ticket.replace('##U+0020##',' ')
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk,timeout=120)

	#def createN4dClient

	def _debug(self,function,msg):

		if self.dbg==1:
			print(f"[BELLSCHEDULER]: {function} {msg}")

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

		self.bellsConfig=result.get("data",{})

		self.bellsConfigData=[]
		
		if result.get("status"):
			self._getBellsConfig()

		self._getAudioDeviceConfig()
		
		return result

	#def readConf	

	def _getBellsConfig(self):

		daysMapping={0:"mo", 1:"tu", 2:"we", 3:"th", 4:"fr"}
		orderBells=self._getOrderBell()

		for item in orderBells:
			bell=self.bellsConfig.get(item)
			soundError=False
			imgError=False
			tmp={"id":item}
			tmp["id"]=item
			
			tmp["cron"]=self.formatTime(item)[2]
			search=[tmp["cron"]]

			weekdays=bell.get("weekdays",{})
			for dayIdx,dayKey in daysMapping.items():
				isActive=weekdays.get(str(dayIdx),False)
				tmp[dayKey]=isActive

				if isActive:
					search.append(self._getDayToSearch(dayIdx))

			validityInfo=bell.get("validity",{})
			tmp["validity"]=validityInfo.get("value","")
			tmp["validityActivated"]=validityInfo.get("active",False)
			if tmp["validity"]:
					search.append(tmp["validity"])

			
			imgPath=bell.get("image",{}).get("path","")
			if os.path.exists(imgPath):
				tmp["img"]=imgPath
			else:
				imgError=True
				tmp["img"]=self.imgNoDispPath
				self.loadError=True

			tmp["name"]=bell.get("name")
			search.append(tmp["name"])

			tmpRet=self._loadSoundPath(item)
			tmp["sound"]=tmpRet[1]
			if not tmpRet[0]:
				tmp["bellActivated"]=bell.get("active",False)
			else:
				soundError=True
				self.loadError=True
				tmp["bellActivated"]=False
				bell["active"]=False
				self._saveConf(self.bellsConfig,item,"active")
 
			tmp["metaInfo"]="".join(search)
			tmp["isSoundError"]=soundError
			tmp["isImgError"]=imgError

			self.bellsConfigData.append(tmp)

		self.bellsMap = {item["id"]: item for item in self.bellsConfigData if "id" in item}

	#def _getBellsConfig

	def _getImagesConfig(self):

		self.imagesConfigData=[]

		if os.path.exists(self.bannersPath):
			sortedFiles=sorted(os.listdir(self.bannersPath))

			self.imagesConfigData=[{"imageSource":os.path.join(self.bannersPath,item)} for item in sortedFiles]
		
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

		imgId=self.bellImage[1]
		defaultImgPath=(
			self.imagesConfigData[imgId]["imageSource"]
			if len(self.imagesConfigData) >imgId else self.bellImage[2]
		)

		self.currentBellConfig={
			"hour":self.bellCron[0],
			"minute":self.bellCron[1],
			"validity":{
				"active":self.bellValidityActive,
				"value":self.bellValidityValue
			},
			"weekdays":{str(i):status for i,status in enumerate(self.bellDays)},
			"name":self.bellName,
			"image":{
				"option":self.bellImage[0],
				"path":defaultImgPath
			},
			"sound":{
				"option":self.bellSound[0],
				"path":self.bellSound[1]
			},
			"play":{
				"duration":self.bellDuration,
				"start":self.bellStartIn
			},
			"active":self.bellActive,
			"soundDefaultPath":self.bellSound[3]
		}
	
	#def initValues

	def _loadSoundPath(self,bell):
		
		soundConfig=self.bellsConfig[bell]["sound"]

		path=soundConfig["path"]
		option=soundConfig["option"]
		error=False
		
		if option in ["url","url_list"]:
			self.loadError=True
			return [True,_("ERROR: Current option for sound not supported")]
			
		if not os.path.exists(path):
			self.loadError=True
			return [True,_("ERROR: File or directory not available")]

		if option=="file":
			return [False,os.path.basename(path)]

		return [False,path]

	#def _loadSoundPath

	def _getDayToSearch(self,day):

		daysMap={
			0:_("Monday")+_("M")+_("Mon"),
			1:_("Tuesday")+_("T")+_("Tue"),
			2:_("Wednesday")+_("W")+_("Wed"),
			3:_("Thursday")+_("R")+_("Thu"),
			4:_("Friday")+_("F")+_("Fri")
		}

		return daysMap.get(day,"")

	#def _getDayToSearch

	def loadBellConfig(self,bellToLoad,duplicateBell):

		bellId=bellToLoad[0]

		if not duplicateBell:
			self.bellToLoad=bellId

		tmpConfig=self.bellsConfig[bellId]	
		self.currentBellConfig=tmpConfig

		self.bellCron=[tmpConfig["hour"],tmpConfig["minute"]]
		
		weekdays=tmpConfig.get("weekdays",{})
		self.bellDays=[weekdays.get(str(i),False) for i in range(5)]
		
		
		validity=tmpConfig.get("validity",{})
		self.bellValidityActive=validity.get("active",False)
		self.bellValidityValue=validity.get("value","")
		tmpConfig["validity"]={"active":self.bellValidityActive,"value":self.bellValidityValue}

		self.bellValidityDaysInRange=[]
		self._getValidityConfig(self.bellValidityValue)
		self.enableBellValidity=self.areDaysChecked(weekdays)
		self.bellName=tmpConfig["name"]

		imgConfig=tmpConfig["image"]
		imgIndex=(
			self._getImageIndexFromPath(imgConfig["path"])
			if imgConfig["option"]=="stock"
			else 1
		)

		self.bellImage=[imgConfig["option"],imgIndex,imgConfig["path"],bellToLoad[1]]

		soundConfig=tmpConfig["sound"]
		tmpSoundPath=soundConfig["path"]
		soundDefaultPath=True

		if soundConfig["option"]=="file" and self.soundsPath not in tmpSoundPath:
			soundDefaultPath=False
		
		self.bellSound=[soundConfig["option"],tmpSoundPath,bellToLoad[2],soundDefaultPath]
		
		playConfig=tmpConfig.get("play",{})
		self.bellStartIn=playConfig.get("start",0)
		self.bellDuration=playConfig.get("duration",0)

		self.bellActive=tmpConfig["active"]
		tmpConfig["soundDefaultPath"]=soundDefaultPath

	#def loadBellConfig

	def _getImageIndexFromPath(self,imagePath):

		for i, item in enumerate(self.imagesConfigData):
			if item.get("imageSource")==imagePath:
				return i
		
		return 0

	#def _getImageIndexFromPath

	def _getValidityConfig(self,validityInfo):

		if not validityInfo:
			return

		if "-" in validityInfo:
			self.bellValidityRangeOption=True
			self.bellValidityDaysInRange=self.getDaysInRange(validityInfo)
		else:
			self.bellValidityRangeOption=False
			self.bellValidityDaysInRange=[validityInfo]

	#def _getValidityConfig

	def areDaysChecked(self,daysSelected):

		return any(daysSelected.values())

	#def areDaysChecked
	
	def _saveConf(self,info,last_change,action):

		change=str(last_change)
				
		result=self.client.BellSchedulerManager.save_changes(info,change,action)
		self._debug("Save configuration file: ",result)
		
		return result

	#def _saveConf		

	def checkData(self,data):
		
		checkValidity=None
		checkImage={"result":True,"code":"","data":""}
		checkSound={"result":True,"code":"","data":""}

		if not data.get("name"):
			return {"result":False,"code":BellManager.MISSING_BELL_NAME_ERROR,"data":""}

		validity=data.get("validity",{})

		if validity.get("active"):
			checkValidity=self.checkValidity(data.get("weekdays",{}),validity.get("value",""))
			
			if checkValidity is not None:
				return checkValidity

		imgConfig=data.get("image",{})

		if imgConfig.get("option")=="custom":
			imgPath=imgConfig.get("path")
			if not imgPath:
				return {"result":False,"code":BellManager.MISSING_IMAGE_FILE_ERROR,"data":""}

			checkImage=self.checkMimetypes(imgPath,"image")
			
			if not checkImage.get("result"):
				return checkImage

		soundConfig=data.get("sound",{})
		soundOption=soundConfig.get("option")
		soundPath=soundConfig.get("path")

		if soundOption=="file":
			if not soundPath:
				return {"result":False,"code":BellManager.MISSING_SOUND_FILE_ERROR,"data":""}
	
			checkSound=self.checkMimetypes(soundPath,"audio")
			
			if not checkSound.get("result"):
				return checkSound

			return self.checkAudiofile(soundPath,"file")
		
		if soundOption=="directory":
			if not soundPath:
				return {"result":False,"code":BellManager.MISSING_SOUND_FOLDER_ERROR,"data":""}

			self.correctFiles=0
			
			return self.checkDirectory(soundPath)

		return {"result":True,"code":"","data":""}	
					
	#def checkData

	def checkMimetypes(self,file,check):

		mime = MimeTypes()
		fileMimeType,_= mime.guess_type(file)
		
		if check=="audio":
			if not fileMimeType or (not fileMimeType.startswith("audio") and not fileMimeType.startswith("video")):
				return {"result":False,"code":BellManager.INVALID_SOUND_FILE_ERROR,"data":""}
		else:
			if not fileMimeType or not fileMimeType.startswith("image"):
				return {"result":False,"code":BellManager.INVALID_IMAGE_FILE_ERROR,"data":""}

		return {"result":True,"code":"","data":""}

	#def checkMimetypes			
				
	def checkAudiofile(self,file,type):
		
		ffprobeArgs=[
			"ffprobe",
			"-show_entries stream codec_type duration",
			"-of",
			"compact=p=0:nk=1"
		]
		
		if type!="file":
			downloader="yt-dlp" if shutil.wicth("yt-dlp") else "youtube-dl"

			try:
				urlCmd=[downloader,"-g",file]
				urlOutput=subprocess.run(urlCmd,capture_output=True,text=True,check=True)
				urls=[line.strip() for line in urlOutput.stdout.splitlines() if line.strip()]

				if not urls:
					return {"result":False,"code":BellManager.SOUND_FILE_URL_NOT_VALID_ERROR,"data":""}	

				targetUrl=urls[1] if len(urls)>1 else urls[0]
				ffprobeArgs.extend(["-i",targetUrl])

			except (subprocess.CalledProcessError,FileNotFoundError):
				return {"result":False,"code":BellManager.SOUND_FILE_URL_NOT_VALID_ERROR,"data":""}	

		else:
			print("1")
			ffprobeArgs.extend(["-i",file.strip('\'"')])
		try:
			result=subprocess.run(ffprobeArgs,capture_output=True,text=True,timeout=10)
			print(result)
			if not result.stdout.strip():
				return {"result":False,"code":BellManager.SOUND_FILE_URL_NOT_VALID_ERROR,"data":""}	

			return {"result":True,"code":BellManager.ACTION_SUCCESSFUL,"data":""}

		except subprocess.TimeOutExpired:
			return {"result":False,"code":BellManager.ERROR_TIMEOUT_EXPIRED,"data":""}

		except FileNotFoundError:
			print("Error")
			return {"result":False,"code":BellManager.ERROR_FFPROBE_MISSING_,"data":""}	


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

	def checkIfAreHolidaysConfigured(self,):

		result=self.client.HolidayListManager.are_days_configured()
	
		return result["status"]

	#def checkIfAreHolidaysConfigured

	def changeHolidayControl(self,action):

		result=self.client.BellSchedulerManager.enable_holiday_control(action)
		self._debug("Change holiday control: ",result)	
		
		return result

	#def changeHolidayControl

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

	def checkDuplicateBellCron(self,data):

		duplicateWeekDays=False
		duplicateValidity=False
		today=datetime.today()

		currentTimer=[data["hour"],data["minute"]]
		currentWeekDays=[data["weekdays"]["0"],data["weekdays"]["1"],data["weekdays"]["2"],data["weekdays"]["3"],data["weekdays"]["4"]]
		currentValidity=[data["validity"]["active"],data["validity"]["value"]]
		currentDays=self.getDaysInRange(currentValidity[1])

		for item in self.bellsConfig:
			if item!=self.bellToLoad:
				tmpTimer=[self.bellsConfig[item]["hour"],self.bellsConfig[item]["minute"]]
				if tmpTimer==currentTimer:
					duplicateWeekDays=False
					tmpWeekDays=[self.bellsConfig[item]["weekdays"]["0"],self.bellsConfig[item]["weekdays"]["1"],self.bellsConfig[item]["weekdays"]["2"],self.bellsConfig[item]["weekdays"]["3"],self.bellsConfig[item]["weekdays"]["4"]]
					for i in range(len(currentWeekDays)):
						if currentWeekDays[i]:
							if tmpWeekDays[i]:
								duplicateWeekDays=True
								break
					if duplicateWeekDays:
						tmpValidity=[self.bellsConfig[item]["validity"]["active"],self.bellsConfig[item]["validity"]["value"]]
						tmpDays=self.getDaysInRange(tmpValidity[1])
						if currentValidity==tmpValidity:
							duplicateValidity=True
						else:
							if not currentValidity[0] and not tmpValidity[0]:
								duplicateValidity=True
							else:
								if len(currentDays)>0:
									if len(tmpDays)>0:
										for day in currentDays:
											if day in tmpDays:
												duplicateValidity=True
												break
									else:
										for day in currentDays:
											if today < datetime.strptime(day,'%d/%m/%Y'):
												duplicateValidity=True
												break
								else:
									if len(tmpDays)>0:
										for day in tmpDays:
											if today < datetime.strptime(day,'%d/%m/%Y'):
												duplicateValidity=True
												break
									else:
										duplicateValidity=True

						if duplicateValidity:
							return {"result":False,"code":BellManager.BELL_DUPLICATE,"data":""}
		
		return {"result":True,"code":"","data":""}

	#def checkDuplicateBellCron	

	def _getAudioDeviceConfig(self):

		result=self.client.BellSchedulerManager.read_audio_device_config()
		self._debug("Read audio device config: ",result)
		if result["data"]!="":
			self.isAudioDeviceConfigurated=True
			for i in range(len(self.audioDevicesData)):
				if self.audioDevicesData[i]["value"]==result["data"]:
					self.currentAudioDevice=i
					break
		else:
			self.isAudioDeviceConfigurated=False
			self.currentAudioDevice=0

	#def _getAudioDeviceConfig

	def changeAudioDeviceControl(self,status,audioDevice):

		newAudioConfigurationStatus=status
		newAudioDeviceValue=audioDevice
		if newAudioConfigurationStatus!=self.isAudioDeviceConfigurated or newAudioDeviceValue!=self.currentAudioDevice:
			if not newAudioConfigurationStatus:
				newValue=""
			else:
				newValue=self.audioDevicesData[newAudioDeviceValue]["value"]

			result=self.client.BellSchedulerManager.write_audio_device_config(newValue)
			self._debug("Write audio device config:",result)
		else:
			result={"status":True,"code":BellManager.AUDIO_DEVICE_ALREADY_CONFIGURATED,"data":""}

		self._getAudioDeviceConfig()
		
		return result

	#def writeAudioDeviceConfig
	
	def _getAudioDevices(self):

		self.audioDevicesData=[]

		cmd="aplay -l"
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()[0].decode().split("\n")

		for item in poutput:
			if ":" in item and "," in item:
				tmpItem=item.split(", ")
				if len(tmpItem)==2:
					tmpDevice={}
					tmpCard=tmpItem[0].split(":")
					tmpCardCode=tmpCard[0].split(" ")[1]
					tmpCardName=tmpCard[1]
					tmpDisp=tmpItem[1].split(":")
					tmpDispCode=tmpDisp[0].split(" ")[1]
					tmpDispName=tmpDisp[1]
					tmpDevice["name"]="%s-%s"%(tmpCardName,tmpDispName)
					tmpDevice["value"]="hw:%s,%s"%(tmpCardCode,tmpDispCode)
					self.audioDevicesData.append(tmpDevice)

		if len(self.audioDevicesData)>1:
			tmpDevice={}
			tmpDevice["name"]=_("Default audio output")
			tmpDevice["value"]="default"
			self.audioDevicesData.insert(0,tmpDevice)
			self.enableAudioDeviceConfiguration=True

	#def _getAudioDevices()
	
#class BellManager 		
