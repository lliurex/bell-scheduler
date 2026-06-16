#!/usr/bin/env python3

import os
import shutil
import subprocess
from mimetypes import MimeTypes
from datetime import datetime, date,timedelta
import copy
import re

import n4d.client
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
	BELL_NOT_FOUND_ERROR=-59
	BELL_ACTIVATION_ERROR=-60

	ACTION_SUCCESSFUL=0
	BELL_REMOVED_SUCCESSFULLY=14
	BELL_EDITED_SUCCESSFULLY=15
	BELL_ACTIVATED_SUCCESSFULLY=16
	BELL_DEACTIVATED_SUCCESSFULLY=17
	BELL_ADDED_SUCCESSFULLY=18
	BELLS_ALREADY_ACTIVATED=53
	BELLS_ALREADY_DEACTIVATED=54
	BELLS_ALREADY_REMOVED=55
	AUDIO_DEVICE_ALREADY_CONFIGURATED=57

	KIRIGAMI_MSG_OK=0
	KIRIGAMI_MSG_ERROR=1
	KIRIGAMI_MSG_WARNING=2
	KIRIGAMI_MSG_INFO=3


	def __init__(self):

		super(BellManager, self).__init__()

		self.dbg=0
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
			bellDays=[]
			for day in weekdays:
				isActive=weekdays.get(day,False)
				bellDays.append(isActive) 
				if isActive:
					search.append(self._getDayToSearch(int(day)))

			tmp["weekDays"]=bellDays
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
			tmp["sound"]=tmpRet.get("path")
			if not tmpRet.get("status"):
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
		self.bellCron={"hour":0,"minute":0}
		self.bellDays={
			"0":False,
			"1":False,
			"2":False,
			"3":False,
			"4":False
		}
		self.bellValidityActive=False
		self.bellValidity={
			"value":"",
			"rangeOption":True,
			"daysInRange":[]
		}
		self.enableBellValidity=False
		self.bellName=""
		self.bellImage={"option":"stock","index":1,"path":"/usr/share/bell-scheduler/banners/bell.png","error":False}
		self.bellSound={"option":"file","path":"","error":False,"defaultPath":True}
		self.bellStartIn=0
		self.bellDuration=0
		self.bellActive=False

		imgId=self.bellImage.get("index")
		defaultImgPath=(
			self.imagesConfigData[imgId]["imageSource"]
			if len(self.imagesConfigData) >imgId else self.bellImage.get("path")
		)
		self.currentBellConfig={
			"hour":self.bellCron.get("hour"),
			"minute":self.bellCron.get("minute"),
			"validity":{
				"active":self.bellValidityActive,
				"value":self.bellValidity.get("value")
			},
			"weekdays":self.bellDays,
			"name":self.bellName,
			"image":{
				"option":self.bellImage.get("option"),
				"path":defaultImgPath
			},
			"sound":{
				"option":self.bellSound.get("option"),
				"path":self.bellSound.get("path")
			},
			"play":{
				"duration":self.bellDuration,
				"start":self.bellStartIn
			},
			"active":self.bellActive,
			"soundDefaultPath":self.bellSound.get("defaultPath")
		}
	
	#def initValues

	def _loadSoundPath(self,bell):
		
		soundConfig=self.bellsConfig[bell]["sound"]

		path=soundConfig["path"]
		option=soundConfig["option"]
		error=False
		
		if option in ["url","url_list"]:
			self.loadError=True
			return {"status":True,"path":_("ERROR: Current option for sound not supported")}
			
		if not os.path.exists(path):
			self.loadError=True
			return {"status":True,"path":_("ERROR: File or directory not available")}

		if option=="file":
			return {"status":False,"path":os.path.basename(path)}

		return {"status":False,"path":path}

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

		bellId=bellToLoad.get("bellId")

		if not duplicateBell:
			self.bellToLoad=bellId

		tmpConfig=self.bellsConfig[bellId]	
		self.currentBellConfig=tmpConfig

		self.bellCron={
			"hour":tmpConfig["hour"],
			"minute":tmpConfig["minute"]
		}
		
		self.bellDays=tmpConfig.get("weekdays")
		
		validity=tmpConfig.get("validity",{})
		self.bellValidityActive=validity.get("active",False)
		tmpValidityValue=validity.get("value","")
		self.bellValidity={
			"value":validity.get("value",""),
			"rangeOption":False if "-" not in tmpValidityValue else True,
			"daysInRange": [tmpValidityValue] if "-" not in tmpValidityValue else self.getDaysInRange(tmpValidityValue)
		}
		tmpConfig["validity"]={"active":self.bellValidityActive,"value":self.bellValidity.get("value")}

		self.enableBellValidity=self.areDaysChecked(self.bellDays)
		self.bellName=tmpConfig["name"]

		imgConfig=tmpConfig["image"]
		imgIndex=(
			self._getImageIndexFromPath(imgConfig["path"])
			if imgConfig["option"]=="stock"
			else 1
		)

		self.bellImage={
			"option":imgConfig["option"],
			"index":imgIndex,
			"path":imgConfig["path"],
			"error":bellToLoad.get("isImgError")
		}

		soundConfig=tmpConfig["sound"]
		tmpSoundPath=soundConfig["path"]
		soundDefaultPath=True

		if soundConfig["option"]=="file" and self.soundsPath not in tmpSoundPath:
			soundDefaultPath=False
		
		self.bellSound={
			"option":soundConfig["option"],
			"path":tmpSoundPath,
			"error":bellToLoad.get("isSoundError"),
			"defaultPath":soundDefaultPath
		}
		
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
		
		checkValidity=True
		checkImage={"status":True,"code":"","data":""}
		checkSound={"status":True,"code":"","data":""}

		if not data.get("name"):
			return {"status":False,"code":BellManager.MISSING_BELL_NAME_ERROR,"data":""}

		validity=data.get("validity",{})

		if validity.get("active"):
			checkValidity=self.checkValidity(data.get("weekdays",{}),validity.get("value",""))
			
			if not checkValidity.get("status"):
				return checkValidity

		imgConfig=data.get("image",{})

		if imgConfig.get("option")=="custom":
			imgPath=imgConfig.get("path")
			if not imgPath:
				return {"status":False,"code":BellManager.MISSING_IMAGE_FILE_ERROR,"data":""}

			checkImage=self.checkMimetypes(imgPath,"image")
			
			if not checkImage.get("status"):
				return checkImage

		soundConfig=data.get("sound",{})
		soundOption=soundConfig.get("option")
		soundPath=soundConfig.get("path")

		if soundOption=="file":
			if not soundPath:
				return {"status":False,"code":BellManager.MISSING_SOUND_FILE_ERROR,"data":""}
	
			checkSound=self.checkMimetypes(soundPath,"audio")
			
			if not checkSound.get("status"):
				return checkSound

			return self.checkAudiofile(soundPath,"file")
		
		if soundOption=="directory":
			if not soundPath:
				return {"status":False,"code":BellManager.MISSING_SOUND_FOLDER_ERROR,"data":""}

			return self.checkDirectory(soundPath)

		return {"status":True,"code":"","data":""}	
					
	#def checkData

	def checkMimetypes(self,file,check):

		mime = MimeTypes()
		fileMimeType,_= mime.guess_type(file)
		
		if check=="audio":
			if not fileMimeType or (not fileMimeType.startswith("audio") and not fileMimeType.startswith("video")):
				return {"status":False,"code":BellManager.INVALID_SOUND_FILE_ERROR,"data":""}
		else:
			if not fileMimeType or not fileMimeType.startswith("image"):
				return {"status":False,"code":BellManager.INVALID_IMAGE_FILE_ERROR,"data":""}

		return {"status":True,"code":"","data":""}

	#def checkMimetypes			
				
	def checkAudiofile(self,file,type):
		
		ffprobeArgs = [
			"ffprobe",
        	"-v", "error",
        	"-show_entries", "stream=codec_type:format=duration",
        	"-of", "compact=p=0:nk=1"
    	]
		
		if type!="file":
			downloader="yt-dlp" if shutil.which("yt-dlp") else "youtube-dl"

			try:
				urlCmd=[downloader,"-g",file]
				urlOutput=subprocess.run(urlCmd,capture_output=True,text=True,check=True)
				urls=[line.strip() for line in urlOutput.stdout.splitlines() if line.strip()]

				if not urls:
					return {"status":False,"code":BellManager.SOUND_FILE_URL_NOT_VALID_ERROR,"data":""}	

				targetUrl=urls[1] if len(urls)>1 else urls[0]
				ffprobeArgs.extend(["-i",targetUrl])

			except (subprocess.CalledProcessError,FileNotFoundError):
				return {"status":False,"code":BellManager.SOUND_FILE_URL_NOT_VALID_ERROR,"data":""}	

		else:
			ffprobeArgs.extend(["-i",file.strip('\'"')])
		
		try:
			result=subprocess.run(ffprobeArgs,capture_output=True,text=True,timeout=10)

			if not result.stdout.strip():
				return {"status":False,"code":BellManager.SOUND_FILE_URL_NOT_VALID_ERROR,"data":""}	

			return {"status":True,"code":BellManager.ACTION_SUCCESSFUL,"data":""}

		except subprocess.TimeoutExpired:
			return {"status":False,"code":BellManager.ERROR_TIMEOUT_EXPIRED,"data":""}

		except FileNotFoundError:
			return {"status":False,"code":BellManager.ERROR_FFPROBE_MISSING_,"data":""}	


	#def checkAudiofile	

	def checkDirectory(self,directory):

		for root,dirs,files in os.walk(directory):
			for file in files:
				fullPath=os.path.join(root,file)
				checkFile=self.checkMimetypes(fullPath,"audio")
				if checkFile.get("status"):
					checkRun=self.checkAudiofile(fullPath,'file')
					if checkRun.get("status"):
						return {"status":True,"code":BellManager.ACTION_SUCCESSFUL,"data":""}

		return {"status":False,"code":BellManager.FOLDER_WITH_INCORRECT_FILES_ERROR,"data":""}

	#def checkDirectory		

	def saveData(self,data):

		bellsConfig=copy.deepcopy(self.bellsConfig)

		if self.bellToLoad:
			order=self.bellToLoad
			action="edit"
		else:
			nextId=max([int(k) for k in self.bellsConfig.keys()],default=0)+1
			order=str(nextId)
			action="add"

		bellData={
			"hour":data["hour"],
			"minute":data["minute"],
			"weekdays":data["weekdays"],
			"name":data["name"],
			"play":data["play"]
		}

		if not data.get("validity").get("value"):
			data["validity"]["active"]=False

		bellData["validity"]=data["validity"]

		origImgPath=""
		bellData["image"]=copy.deepcopy(data["image"])

		if data["image"].get("option")=="custom":
			origImgPath=data["image"].get("path")
			bellData["image"]["path"]=os.path.join(self.imagesPath,os.path.basename(origImgPath))

		origSoundPath=""
		bellData["sound"]=copy.deepcopy(data["sound"])

		if data["sound"].get("option")=="file" and data.get("soundDefaultPath"):
			origSoundPath=data["sound"].get("path")
			destSoundPath=os.path.join(self.soundsPath,os.path.basename(origSoundPath))
			bellData["sound"]["path"]=os.path.join(self.soundsPath,os.path.basename(origSoundPath))


		if self.areDaysChecked(data["weekdays"]):
			activeBell=data["active"] if action=="edit" else True
		else:
			activeBell=False

		bellData["active"]=activeBell
		bellsConfig[order]=bellData

		retCopy=self._copyMediaFiles(origImgPath,origSoundPath)

		if not retCopy.get("status"):
			return {"status":False,"code":retCopy.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}	

		retSave=self._saveConf(bellsConfig,order,action)
		
		if not retSave.get("status"):
			return {"status":False,"code":retSave.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

		retReadConfig=self.readConf()
		if not retReadConfig.get("status"):
			return {"status":False,"code":retReadConfig.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

		code=BellManager.BELL_EDITED_SUCCESSFULLY if action=="edit" else BellManager.BELL_ADDED_SUCCESSFULLY
		
		return {"status":True,"code":code,"type":BellManager.KIRIGAMI_MSG_OK}	

	#def saveData

	def changeBellStatus(self,allBells,active,bellToEdit=None):

		if allBells:
			
			if not self._checkBellStatus(active):
				code=BellManager.BELLS_ALREADY_ACTIVATED if active else BellManager.BELLS_ALREADY_DEACTIVATED
				return {"status":True,"code":code,"type":BellManager.KIRIGAMI_MSG_OK}

			retChangeStatus=self.changeActivationStatus(active)
			
			if not retChangeStatus.get('status'):
				return {"status":False,"code":retChangeStatus.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

			retReadConfig=self.readConf()

			if not retReadConfig.get("status"):
				return {"status":False,"code":retReadConfig.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

			return {"status":True,"code":retChangeStatus.get("code"),"type":BellManager.KIRIGAMI_MSG_OK}

		else:
			if not self.areDaysChecked(self.bellsConfig[bellToEdit]["weekdays"]):
				return {"status":False,"code":BellManager.BELL_ACTIVATION_ERROR,"type":BellManager.KIRIGAMI_MSG_ERROR}
		
		self.bellsConfig[bellToEdit]["active"]=active
		ret=self._saveConf(self.bellsConfig,bellToEdit,"active")

		if not ret.get("status"):
			return {"status":False,"code":ret.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

		self._updateBellsConfigData("bellActivated",active,bellToEdit)
		code=BellManager.BELL_ACTIVATED_SUCCESSFULLY if active else BellManager.BELL_DEACTIVATED_SUCCESSFULLY

		return {"status":True,"code":code,"type":BellManager.KIRIGAMI_MSG_OK}

	#def changeBellStatus

	def _checkBellStatus(self,active):

		for bell in self.bellsConfig.values():
			if bell.get("active")!=active:
				return True

		return False

	#def _checkBellStatus

	def _updateBellsConfigData(self,param,value,bellId):

		item=self.bellsMap.get(bellId)
		
		if item:
			if item[param]!=value:
				item[param]=value

	#def _updateBellsConfigData

	def removeBell(self,allBells,bellToRemove=None):

		if allBells:
			if not self.bellsConfig:
				return {"status":True,"code":BellManager.BELLS_ALREADY_REMOVED,"type":BellManager.KIRIGAMI_MSG_OK}

			retRemove=self._removeAllBells()
			if not retRemove.get('status'):
				return {"status":False,"code":retRemove.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

			retReadConfig=self.readConf()
			if not retReadConfig.get("status"):
				return {"status":False,"code":retReadConfig.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

			return {"status":True,"code":retRemove["code"],"type":BellManager.KIRIGAMI_MSG_OK}
			
				
		bellsConfig=copy.deepcopy(self.bellsConfig)

		if bellsConfig.pop(bellToRemove,None) is None:
			return {"status":False,"code":BellManager.BELL_NOT_FOUND_ERROR,"type":BellManager.KIRIGAMI_MSG_ERROR}

		ret=self._saveConf(bellsConfig,bellToRemove,"remove")
		if not ret.get("status"):
			return {"status":False,"code":ret.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

		self.bellsConfig=bellsConfig
		self.bellsConfigData=[item for item in self.bellsConfigData if item.get("id")!=bellToRemove]

		return {"status":True,"code":BellManager.BELL_REMOVED_SUCCESSFULLY,"type":BellManager.KIRIGAMI_MSG_OK}
	
	#def removeBell

	def _getOrderBell(self,info=None):
	
		dataSource=self.bellsConfig if info is None else info

		if not dataSource:
			return []

		currentDay=datetime.combine(date.today(),datetime.min.time())
		tmp=[]

		for itemId,bellData in dataSource.items():
			timeStr=f"{bellData.get("hour",0)}:{bellData.get("minute",0)}"
			try:
				timeF=datetime.strptime(timeStr,"%H:%M")
			except ValueError:
				timeF=datetime.strptime("00:00","%H:%M")

			dateF=currentDay
			validityValue=bellData.get("validity",{}).get("value","")
			if validityValue:
				dateToFormat=validityValue.split("-")[0] if "-" in validityValue else validityValue
				try:
					dateF=datetime.strptime(dateToFormat.strip(),"%d/%m/%Y")
				except ValueError:
					dateF=currentDay

			tmp.append((itemId,timeF,dateF))

		tmp.sort(key=lambda bell:(bell[1],bell[2]))

		return [bell[0] for bell in tmp]
		
		
	#def _getOrderBells
	
	def formatTime(self,item):
	
		bell=self.bellsConfig.get(item,{})
		hour=bell.get("hour",0)
		minute=bell.get("minute",0)

		hourStr=f"{hour:02d}"
		minuteStr=f"{minute:02d}"
		cron=f"{hourStr}:{minuteStr}"

		return [hourStr,minuteStr,cron]

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
		
		result["type"]=BellManager.KIRIGAMI_MSG_OK if result.get("status") else BellManager.KIRIGAMI_MSG_ERROR
		
		return result

	#def exportBellsConf

	def importBellBackup(self,origFile):

		backup=True
		resultImport=self._importBellsConfifg(origFile,backup)

		if not resultImport.get('status'):
			return {"status":False,"data":resultImport.get("data")}

		retReadConfig=self.readConf()
		if retReadConfig.get("status"):
			return {"status":True,"code":resultImport.get("code"),"type":BellManager.KIRIGAMI_MSG_OK}
		else:
			return {"status":False,"code":retReadConfig.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

	#def importBellBackup

	def _importBellsConfifg(self,origFile,backup):
		
		user=os.environ["USER"]
		result=self.client.BellSchedulerManager.import_bells_conf(origFile,user,backup)
		self._debug("Import bells config: ",result)	
		
		return result

	#def importBellsConfig

	def recoveryBellBackup(self,origFile):

		resultRecovery=self._recoveryBellsConfig(origFile,backup)
		
		if not resultRecovery.get("status"):
			return {"status":False,"code":resultRecovery.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

		retReadConfig=self.readConf()

		if retReadConfig.get("status"):
			return {"status":False,"code":BellManager.RECOVERY_BELLS_CONFIG,"type":BellManager.KIRIGAMI_MSG_ERROR}
		else:
			return {"status":False,"code":retReadConfig.get("code"),"type":BellManager.KIRIGAMI_MSG_ERROR}

	#def recoveryBellBackup

	def _recoveryBellsConfig(self,origFile,backup):
		
		user=os.environ["USER"]
		result=self.client.BellSchedulerManager.import_bells_conf(origFile,user,backup)
		self._debug("Recovery bells config: ",result)	
		
		return result

	#def recoveryBellsConfig	

	def changeActivationStatus(self,active):

		action="activate" if active else "deactivate"
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

		if not validity:
			return {"status":True,"code":"","data":""}

		daysInValidity=self.getDaysInRange(validity)
		weeksValidity=set()

		for item in daysInValidity:
			tmpDay=datetime.strptime(item,"%d/%m/%Y")
			weeksValidity.add(tmpDay.weekday())

		weekdaysSelected=[int(i) for i,active in weekdays.items() if active]

		for item in weekdaysSelected:
			if item not in weeksValidity:
				return {"status":False,"code":BellManager.DAY_NOT_IN_VALIDITY_ERROR,"data":""}

		return {"status":True,"code":"","data":""}

		
	#def checkValidity

	def getDaysInRange(self,day):	

		listDays=[]

		if not day:
			return listDays

		if "-" in day:
			tmp=day.split("-")
			date1=datetime.strptime(tmp[0].strip(),'%d/%m/%Y')
			date2=datetime.strptime(tmp[1].strip(),'%d/%m/%Y')
		else:
			date1=datetime.strptime(day.strip(),'%d/%m/%Y')
			date2=date1
		
		delta=date2-date1
		for i in range(delta.days + 1):
			tmpDay=(date1 + timedelta(days=i)).strftime('%d/%m/%Y')
			listDays.append(tmpDay)

		return listDays	

	#def getDaysInRange

	def checkGlobalOptionStatus(self):

		return bool(self.bellsConfig)
	
	#def checkGlobalOptionStatus

	def checkIfAreBellsWithDirectory(self):

		return any(bell.get("sound",{}).get("option")=="directory" for bell in self.bellsConfig.values())

	#def checkIfAreBellsWithRandom

	def checkHolidayManagerStatus(self):

		return os.path.exists(self.holidayToken)
	
	#def checkHolidayManagerStatus

	def checkIfAreHolidaysConfigured(self,):

		return self.client.HolidayListManager.are_days_configured().get("status")

	#def checkIfAreHolidaysConfigured

	def changeHolidayControl(self,action):

		result=self.client.BellSchedulerManager.enable_holiday_control(action)
		self._debug("Change holiday control: ",result)	
		
		result["type"]=BellManager.KIRIGAMI_MSG_OK if result.get("status") else BellManager.KIRIGAMI_MSG_ERROR
		return result

	#def changeHolidayControl

	def checkChangeStatusBellsOption(self):

		totalBells=len(self.bellsConfig)

		if totalBells==0:
			return {"allActivated":False,"allDetactivated":False,"enableFilter":False}

		countActivated=sum(1 for bell in self.bellsConfig.values() if bell.get("active"))

		allActivated=(countActivated==totalBells)
		allDeactivated=(countActivated==0)
		enableStatusFilter=not(allActivated or allDeactivated)

		return {"allActivated":allActivated,"allDeactivated":allDeactivated,"enableFilter":enableStatusFilter}

	#def checkChangeStatusBellsOption

	def checkDuplicateBellCron(self,data):

		today=datetime.today()

		currentTime=(data.get("hour"),data.get("minute"))
		
		currentWeekDays={int(k) for k,active in data.get("weekdays",{}).items() if active}
		
		currentValidityActive=data.get("validity",{}).get("active",False)
		currentValidityValue=data.get("validity",{}).get("value","")
		currentDays=set(self.getDaysInRange(currentValidityValue))

		for itemId,bell in self.bellsConfig.items():
			if itemId==self.bellToLoad:
				continue

			if (bell.get("hour"),bell.get("minute")) != currentTime:
				continue

			tmpWeekDays={int(k) for k,active in bell.get("weekdays",{}).items() if active}
			
			if not currentWeekDays.intersection(tmpWeekDays):
				continue

			tmpValidityActive=bell.get("validity",{}).get("active",False)
			tmpValidityValue=bell.get("validity",{}).get("value","")
			
			duplicateValidity=False

			if currentValidityActive==tmpValidityActive and currentValidityValue==tmpValidityValue:
				duplicateValidity=True

			elif not currentValidityActive and not tmpValidityActive:
				duplicateValidity=True

			else:
				tmpDays=set(self.getDaysInRange(tmpValidityValue))

				if currentDays and tmpDays:
					if currentDays.intersection(tmpDays):
						duplicateValidity=True
				
				elif currentDays:
					duplicateValidity=any(today<datetime.strptime(d,"%d/%m/%Y") for d in currentDays)
				
				elif tmpDays:
					duplicateValidity=any(today<datetime.strptime(d,"%d/%m/%Y") for d in tmpDays)

				else:
					duplicateValidity=True

			if duplicateValidity:
				return False
		
		return True

	#def checkDuplicateBellCron	

	def _getAudioDeviceConfig(self):

		result=self.client.BellSchedulerManager.read_audio_device_config()
		self._debug("Read audio device config: ",result)
		
		deviceValue=result.get("data") if isinstance(result,dict) else ""

		if deviceValue:
			self.isAudioDeviceConfigurated=True
			self.currentAudioDevice=0

			for i,device in enumerate(self.audioDevicesData):
				if device.get("value")==deviceValue:
					self.currentAudioDevice=i
					break
		else:
			self.isAudioDeviceConfigurated=False
			self.currentAudioDevice=0

	#def _getAudioDeviceConfig

	def changeAudioDeviceControl(self,status,audioDevice):

		if status==self.isAudioDeviceConfigurated and audioDevice==self.currentAudioDevice:
			 return {"status":True,"code":BellManager.AUDIO_DEVICE_ALREADY_CONFIGURATED,"type":BellManager.KIRIGAMI_MSG_OK}

		if not status:
			newValue=""

		else:
			if 0<=audioDevice<len(self.audioDevicesData):
				newValue=self.audioDevicesData[audioDevice]["value"]
			else:
				newValue=""

		result=self.client.BellSchedulerManager.write_audio_device_config(newValue)
		self._debug("Write audio device config:",result)

		self._getAudioDeviceConfig()
		result["type"]=BellManager.KIRIGAMI_MSG_OK if result.get("status") else BellManager.KIRIGAMI_MSG_ERROR
		
		return result

	#def writeAudioDeviceConfig
	
	def _getAudioDevices(self):

	 	self.audioDevicesData = []

	 	try:
	 		cmd = "LC_ALL=C aplay -l"
	 		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	 		stdout,stderr = p.communicate()
	 		poutput = stdout.decode('utf-8', errors='ignore').splitlines()
	 	except Exception as e:
	 		self._debug("_getAudioDevices. Error:", e)
	 		poutput = []

	 	pattern = re.compile(r"card\s+(\d+):\s*([^,]+),\s*device\s+(\d+):\s*(.*)")

	 	for item in poutput:
	 		match = pattern.search(item)
	 		if match:
	 			card_code = match.group(1)
	 			card_name = match.group(2).strip()
	 			disp_code = match.group(3)
	 			disp_name = match.group(4).strip()

	 			self.audioDevicesData.append({
	 				"name": f"{card_name}-{disp_name}",
	 				"value": f"hw:{card_code},{disp_code}"
	 			})

	 	if len(self.audioDevicesData) > 1:
	 		self.audioDevicesData.insert(0, {
	 			"name": _("Default audio output"),
	 			"value": "default"
	 			})
	 		self.enableAudioDeviceConfiguration = True
	 	else:
	 		self.enableAudioDeviceConfiguration = False
	
	#def _getAudioDevices()
	
#class BellManager 		
