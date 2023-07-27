from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from . import BellManager
from . import BellsModel
from . import ImagesModel

NEW_BELL_CONFIG=1
LOAD_BELL_CONFIG=2
CHANGE_BELL_STATUS=5

class GatherInfo(QThread):

	def __init__(self,*args):
		
		QThread.__init__(self)

	#def _init__

	def run(self,*args):
		
		time.sleep(1)
		self.syncWithCron=Bridge.bellMan.syncWithCron()
		if self.syncWithCron:
			self.readConf=Bridge.bellMan.readConf()

	#def run

#class GatherInfo

class LoadBell(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.newBell=args[0]
		self.bellInfo=args[1]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		ret=Bridge.bellMan.initValues()
		if not self.newBell:
			ret=Bridge.bellMan.loadBellConfig(self.bellInfo)

	#def run

#class LoadBell

class CheckData(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.dataToCheck=args[0]
		self.ret={}

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.bellMan.checkData(self.dataToCheck)

	#def run

#class CheckData

class SaveData(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.dataToSave=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.bellMan.saveData(self.dataToSave)

	#def run

#class SaveData

class ChangeBellStatus(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.data=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.bellMan.changeBellStatus(self.data[0],self.data[1])

	#def run

#class ChangeBellStatus

class RemoveBell(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.bellToRemove=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.bellMan.removeBell(self.bellToRemove)

	#def run

#class RemoveBell

class Bridge(QObject):

	bellMan=BellManager.BellManager()

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self._systemLocale=Bridge.bellMan.systemLocale
		self._bellsModel=BellsModel.BellsModel()
		self._imagesModel=ImagesModel.ImagesModel()
		self._bellCron=Bridge.bellMan.bellCron
		self._bellDays=Bridge.bellMan.bellDays
		self._bellValidityActive=Bridge.bellMan.bellValidityActive
		self._bellValidityValue=Bridge.bellMan.bellValidityValue
		self._bellValidityRangeOption=True
		self._bellValidityDaysInRange=[]
		self._enableBellValidity=False
		self._bellName=Bridge.bellMan.bellName
		self._bellImage=Bridge.bellMan.bellImage
		self._bellSound=Bridge.bellMan.bellSound
		self._bellStartIn=Bridge.bellMan.bellStartIn
		self._bellDuration=Bridge.bellMan.bellDuration
		self._currentStack=0
		self._mainCurrentOption=0
		self._bellCurrentOption=0
		self._closePopUp=[True,""]
		self.moveToStack=""
		self._closeGui=False
		self._showMainMessage=[False,"","Ok"]
		self._showLoadErrorMessage=[False,""]
		self._showBellFormMessage=[False,"","Ok"]
		self._showChangesInBellDialog=False
		self._changesInBell=False
		self._showRemoveBellDialog=False
		Bridge.bellMan.createN4dClient(ticket)
		self.initBridge()

	#def _init__

	def initBridge(self):

		self.currentStack=0
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)
	
	#def initBridge
	
	def _loadConfig(self):

		if self.gatherInfo.syncWithCron['status']:
			if self.gatherInfo.readConf['status']:
				self.currentStack=1
				self._updateBellsModel()
				self._updateImagesModel()
				if Bridge.bellMan.loadError:
					self.showMainMessage=[True,Bridge.bellMan.BELLS_WITH_ERRORS,"Error"]
			else:
				self.showLoadErrorMessage=[True,self.gatherInfo.readConf['code']]
		else:
			self.showLoadErrorMessage=[True,self.gatherInfo.syncWithCron['code']]
	
	#def _loadConfig

	def _getSystemLocale(self):

		return self._systemLocale

	#def _getSystemLocale

	def _getBellCron(self):

		return self._bellCron

	#def _getBellCron

	def _setBellCron(self,bellCron):

		if self._bellCron!=bellCron:
			self._bellCron=bellCron
			self.on_bellCron.emit()

	#def _setBellCron

	def _getBellDays(self):

		return self._bellDays

	#def _getBellDays

	def _setBellDays(self,bellDays):

		if self._bellDays!=bellDays:
			self._bellDays=bellDays
			self.on_bellDays.emit()

	#def _setBellDays

	def _getBellValidityActive(self):

		return self._bellValidityActive

	#def _getBellValidityActive

	def _setBellValidityActive(self,bellValidityActive):

		if self._bellValidityActive!=bellValidityActive:
			self._bellValidityActive=bellValidityActive
			self.on_bellValidityActive.emit()

	#def _setBellValidityActive

	def _getBellValidityValue(self):

		return self._bellValidityValue

	#def _getBellValidityValue

	def _setBellValidityValue(self,bellValidityValue):

		if self._bellValidityValue!=bellValidityValue:
			self._bellValidityValue=bellValidityValue
			self.on_bellValidityValue.emit()

	#def _setBellValidityValue

	def _getBellValidityRangeOption(self):

		return self._bellValidityRangeOption

	#def _getBellValidityRangeOption

	def _setBellValidityRangeOption(self,bellValidityRangeOption):

		if self._bellValidityRangeOption!=bellValidityRangeOption:
			self._bellValidityRangeOption=bellValidityRangeOption
			self.on_bellValidityRangeOption.emit()

	#def _setBellValidityRangeOption

	def _getBellValidityDaysInRange(self):

		return self._bellValidityDaysInRange

	#def _getBellValidityDaysInRange

	def _setBellValidityDaysInRange(self,bellValidityDaysInRange):

		if self._bellValidityDaysInRange!=bellValidityDaysInRange:
			self._bellValidityDaysInRange=bellValidityDaysInRange
			self.on_bellValidityDaysInRange.emit()

	#def _setBellValidityDaysInRange

	def _getEnableBellValidity(self):

		return self._enableBellValidity

	#def _getEnableBellValidity

	def _setEnableBellValidity(self,enableBellValidity):

		if self._enableBellValidity!=enableBellValidity:
			self._enableBellValidity=enableBellValidity
			self.on_enableBellValidity.emit()

	#def _setEnableBellValidity

	def _getBellName(self):

		return self._bellName

	#def _getBellName

	def _setBellName(self,bellName):

		if self._bellName!=bellName:
			self._bellName=bellName
			self.on_bellName.emit()

	#def _setBellName 

	def _getBellImage(self):

		return self._bellImage

	#def _getBellImage

	def _setBellImage(self,bellImage):

		if self._bellImage!=bellImage:
			self._bellImage=bellImage
			self.on_bellImage.emit()

	#def _setBellImage

	def _getBellSound(self):

		return self._bellSound

	#def _getBellSound

	def _setBellSound(self,bellSound):

		if self._bellSound!=bellSound:
			self._bellSound=bellSound
			self.on_bellSound.emit()

	#def _setBellSound

	def _getBellStartIn(self):

		return self._bellStartIn

	#def _getBellStartIn

	def _setBellStartIn(self,bellStartIn):

		if self._bellStartIn!=bellStartIn:
			self._bellStartIn=bellStartIn
			self.on_bellStartIn.emit()

	#def _setBellStartIn

	def _getBellDuration(self):

		return self._bellDuration

	#def _getBellDuration

	def _setBellDuration(self,bellDuration):

		if self._bellDuration!=bellDuration:
			self._bellDuration=bellDuration
			self.on_bellDuration.emit()

	#def _setBellDuration

	def _getCurrentStack(self):

		return self._currentStack

	#def _getCurrentStack	

	def _setCurrentStack(self,currentStack):
		
		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.on_currentStack.emit()

	#def _setCurentStack

	def _getMainCurrentOption(self):

		return self._mainCurrentOption

	#def _getMainCurrentOption	

	def _setMainCurrentOption(self,mainCurrentOption):
		
		if self._mainCurrentOption!=mainCurrentOption:
			self._mainCurrentOption=mainCurrentOption
			self.on_mainCurrentOption.emit()

	#def _setMainCurrentOption

	def _getBellCurrentOption(self):

		return self._bellCurrentOption

	#def _getBellCurrentOption	

	def _setBellCurrentOption(self,bellCurrentOption):
		
		if self._bellCurrentOption!=bellCurrentOption:
			self._bellCurrentOption=bellCurrentOption
			self.on_bellCurrentOption.emit()

	#def _setBellCurrentOption

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp

	def _setClosePopUp(self,closePopUp):

		if self._closePopUp!=closePopUp:
			self._closePopUp=closePopUp
			self.on_closePopUp.emit()

	#def _setClosePopUp

	def _getShowChangesInBellDialog(self):

		return self._showChangesInBellDialog

	#def _getShowChangesInBellDialog

	def _setShowChangesInBellDialog(self,showChangesInBellDialog):

		if self._showChangesInBellDialog!=showChangesInBellDialog:
			self._showChangesInBellDialog=showChangesInBellDialog
			self.on_showChangesInBellDialog.emit()

	#def _setShowChangesInBellDialog

	def _getChangesInBell(self):

		return self._changesInBell

	#def _getChangesInBell

	def _setChangesInBell(self,changesInBell):

		if self._changesInBell!=changesInBell:
			self._changesInBell=changesInBell
			self.on_changesInBell.emit()

	#def _setChangesInBell

	def _getShowRemoveBellDialog(self):

		return self._showRemoveBellDialog

	#def _getShowRemoveBellDialog

	def _setShowRemoveBellDialog(self,showRemoveBellDialog):

		if self._showRemoveBellDialog!=showRemoveBellDialog:
			self._showRemoveBellDialog=showRemoveBellDialog
			self.on_showRemoveBellDialog.emit()

	#def _setShowRemoveBellDialog

	def _getBellsModel(self):

		return self._bellsModel

	#def _getBellsModel

	def _getShowMainMessage(self):

		return self._showMainMessage

	#def _getShowMainMessage

	def _setShowMainMessage(self,showMainMessage):

		if self._showMainMessage!=showMainMessage:
			self._showMainMessage=showMainMessage
			self.on_showMainMessage.emit()

	#def _setShowMainMessage

	def _getShowLoadErrorMessage(self):

		return self._showLoadErrorMessage

	#def _getShowLoadErrorMessage

	def _setShowLoadErrorMessage(self,showLoadErrorMessage):

		if self._showLoadErrorMessage!=showLoadErrorMessage:
			self._showLoadErrorMessage=showLoadErrorMessage
			self.on_showLoadErrorMessage.emit()

	#def _setShowLoadErrorMessage

	def _getShowBellFormMessage(self):

		return self._showBellFormMessage

	#def _getShowBellFormMessage

	def _setShowBellFormMessage(self,showBellFormMessage):

		if self._showBellFormMessage!=showBellFormMessage:
			self._showBellFormMessage=showBellFormMessage
			self.on_showBellFormMessage.emit()

	#def _setShowBellFormMessage

	def _getImagesModel(self):

		return self._imagesModel

	#def _getImagesModel	

	def _getCloseGui(self):

		return self._closeGui

	#def _getCloseGui	

	def _setCloseGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui
			self.on_closeGui.emit()

	#def _setCloseGui	

	def _updateBellsModel(self):

		ret=self._bellsModel.clear()
		bellsEntries=Bridge.bellMan.bellsConfigData
		for item in bellsEntries:
			if item["id"]!="":
				self._bellsModel.appendRow(item["id"],item["cron"],item["mo"],item["tu"],item["we"],item["th"],item["fr"],item["validity"],item["validityActivated"],item["img"],item["name"],item["sound"],item["bellActivated"],item["metaInfo"],item["isSoundError"],item["isImgError"])
	
	#def _updateBellsModel

	def _updateBellsModelInfo(self,param):

		updatedInfo=Bridge.onedriveMan.bellsConfigData
		if len(updatedInfo)>0:
			for i in range(len(updatedInfo)):
				index=self._bellsModel.index(i)
				self._bellsModel.setData(index,param,updatedInfo[i][param])

	#def _updateBellsModelInfo

	def _updateImagesModel(self):

		ret=self._imagesModel.clear()
		imagesEntries=Bridge.bellMan.imagesConfigData
		for item in imagesEntries:
			if item["imageSource"]!="":
				self._imagesModel.appendRow(item["imageSource"])
	
	#def _updateImagesModel

	@Slot()
	def addNewBell(self):

		self.closePopUp=[False,NEW_BELL_CONFIG]
		self.newBell=LoadBell(True,"")
		self.newBell.start()
		self.newBell.finished.connect(self._addNewBellRet)

	#def addNewBell

	def _addNewBellRet(self):

		self.currentBellConfig=copy.deepcopy(Bridge.bellMan.currentBellConfig)
		self._initializeVars()
		self.closePopUp=[True,""]
		self.currentStack=2
		self.bellCurrentOption=0

	#def _addNewBellRet

	def _initializeVars(self):

		self.bellCron=Bridge.bellMan.bellCron
		self.bellDays=Bridge.bellMan.bellDays
		self.bellValidityActive=Bridge.bellMan.bellValidityActive
		self.bellValidityValue=Bridge.bellMan.bellValidityValue
		self.bellValidityRangeOption=Bridge.bellMan.bellValidityRangeOption
		self.bellValidityDaysInRange=Bridge.bellMan.bellValidityDaysInRange
		self.enableBellValidity=Bridge.bellMan.enableBellValidity
		self.bellName=Bridge.bellMan.bellName
		self.bellImage=Bridge.bellMan.bellImage
		self.bellSound=Bridge.bellMan.bellSound
		self.bellStartIn=Bridge.bellMan.bellStartIn
		self.bellDuration=Bridge.bellMan.bellDuration
		self.showBellFormMessage=[False,"","Ok"]
		self.changesInBell=False

	#def _initializeVars

	@Slot()
	def goHome(self):

		if not self.changesInBell:
			self.currentStack=1
			self.mainCurrentOption=0
			self.moveToStack=""
		else:
			self.showChangesInBellDialog=True
			self.moveToStack=1

	#def goHome

	@Slot('QVariantList')
	def loadBell(self,bellToLoad):

		self.closePopUp=[False,LOAD_BELL_CONFIG]
		self.editBell=LoadBell(False,bellToLoad)
		self.editBell.start()
		self.editBell.finished.connect(self._loadBellRet)

	#def loadBell

	def _loadBellRet(self):

		self.currentBellConfig=copy.deepcopy(Bridge.bellMan.currentBellConfig)
		self._initializeVars()
		self.closePopUp=[True,""]
		self.currentStack=2
		self.bellCurrentOption=0

	#def _loadBellRet

	@Slot('QVariantList')
	def updateClockValues(self,values):

		if values[0]=="H":
			if values[1]!=self.bellCron[0]:
				self.bellCron[0]=values[1]
				self.currentBellConfig["hour"]=self.bellCron[0]
		else:
			if values[1]!=self.bellCron[1]:
				self.bellCron[1]=values[1]
				self.currentBellConfig["minute"]=self.bellCron[1]

		if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateClockValues

	@Slot('QVariantList')
	def updateWeekDaysValues(self,values):

		if values[0]=="MO":
			if values[1]!=self.bellDays[0]:
				self.bellDays[0]=values[1]
				self.currentBellConfig["weekdays"]["0"]=self.bellDays[0]
		elif values[0]=="TU":
			if values[1]!=self.bellDays[1]:
				self.bellDays[1]=values[1]
				self.currentBellConfig["weekdays"]["1"]=self.bellDays[1]
		elif values[0]=="WE":
			if values[1]!=self.bellDays[2]:
				self.bellDays[2]=values[1]
				self.currentBellConfig["weekdays"]["2"]=self.bellDays[2]
		elif values[0]=="TH":
			if values[1]!=self.bellDays[3]:
				self.bellDays[3]=values[1]
				self.currentBellConfig["weekdays"]["3"]=self.bellDays[3]
		elif values[0]=="FR":
			if values[1]!=self.bellDays[4]:
				self.bellDays[4]=values[1]
				self.currentBellConfig["weekdays"]["4"]=self.bellDays[4]

		self.enableBellValidity=Bridge.bellMan.areDaysChecked(self.currentBellConfig["weekdays"])
		
		if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateWeekDaysValues

	@Slot(bool)
	def updateBellValidityActive(self,value):

		self._updateBellValidityActive(value)

	#updateBellValidityActive

	def _updateBellValidityActive(self,value):

		if value!=self.bellValidityActive:
			self.bellValidityActive=value
			self.currentBellConfig["validity"]["active"]=self.bellValidityActive

		if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def _updateBellValidityActive

	@Slot('QVariantList')
	def updateBellValidityValue(self,value):

		if value[0]!=self.bellValidityValue:
			self.bellValidityValue=value[0]
			self.currentBellConfig["validity"]["value"]=self.bellValidityValue
			self.bellValidityRangeOption=value[1]
			self.bellValidityDaysInRange=Bridge.bellMan.getDaysInRange(self.bellValidityValue)

		if value[0]!="":
			if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
				self.changesInBell=True
			else:
				self.changesInBell=False
		else:
			self._updateBellValidityActive(False)

	#def updateBellValidityValue

	@Slot(str)
	def updateBellNameValue(self,value):

		if value!=self.bellName:
			self.bellName=value
			self.currentBellConfig["name"]=self.bellName

		if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateBellNameValue

	@Slot(str,result=bool)
	def checkMimetypeImage(self,imagePath):

		return Bridge.bellMan.checkMimetypes(imagePath,"image")["result"]

	#def checkMimetypeImage

	@Slot('QVariantList')
	def updateImageValues(self,values):

		tmpImage=[]
		tmpImage.append(values[0])
		tmpImage.append(values[1])

		if values[0]=="stock":
			tmpPath=Bridge.bellMan.imagesConfigData[values[1]]["imageSource"]
		else:
			tmpPath=values[2]
		tmpImage.append(tmpPath)

		if os.path.exists(tmpPath):
			tmpImage.append(False)
		else:
			tmpImage.append(True)

		if tmpImage!=self.bellImage[0]:
			self.bellImage=tmpImage
			self.currentBellConfig["image"]["option"]=self.bellImage[0]
			self.currentBellConfig["image"]["path"]=self.bellImage[2]
	
		if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateImageValues

	@Slot(str,result=bool)
	def checkMimetypeSound(self,soundPath):

		return Bridge.bellMan.checkMimetypes(soundPath,"audio")["result"]

	#def checkMimetypeSound

	@Slot('QVariantList')
	def updateSoundValues(self,values):

		tmpSound=[]
		tmpSound.append(values[0])
		tmpSound.append(values[1])
		if os.path.exists(values[1]):
			tmpSound.append(False)
		else:
			tmpSound.append(True)
		tmpSound.append(values[2])
	
		if tmpSound!=self.bellSound:
			self.bellSound=tmpSound
			self.currentBellConfig["sound"]["option"]=self.bellSound[0]
			self.currentBellConfig["sound"]["path"]=self.bellSound[1]
			self.currentBellConfig["soundDefaultPath"]=self.bellSound[3]

		if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateSoundValues

	@Slot(int)
	def updateStartInValue(self,value):

		if value!=self.bellStartIn:
			self.bellStartIn=value
			self.currentBellConfig["play"]["start"]=self.bellStartIn

		if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateStartInValue

	@Slot(int)
	def updateDurationValue(self,value):

		if value!=self.bellDuration:
			self.bellDuration=value
			self.currentBellConfig["play"]["duration"]=self.bellDuration

		if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateDurationValue

	@Slot(str)
	def manageChangesDialog(self,action):

		self.showChangesInBellDialog=False

		if action=="Accept":
			self._applyBellChanges()
		elif action=="Discard":
			self._cancelBellChanges()
		elif action=="Cancel":
			pass

	#def manageChangesDialog

	@Slot()
	def applyBellChanges(self):

		self._applyBellChanges()

	#def applyBellChanges

	def _applyBellChanges(self):

		self.closePopUp=[False,3]
		self.closeGui=False
		self.checkData=CheckData(self.currentBellConfig)
		self.checkData.start()
		self.checkData.finished.connect(self._checkDataRet)

	#def _applyBellChanges

	def _checkDataRet(self):

		if self.checkData.ret["result"]:
			self.closePopUp=[False,4]
			self.saveData=SaveData(self.currentBellConfig)
			self.saveData.start()
			self.saveData.finished.connect(self._saveDataRet)

		else:
			self.closePopUp=[True,""]
			self.showBellFormMessage=[True,self.checkData.ret["code"],"Error"]

	#def _checkDataRet

	def _saveDataRet(self):

		if self.saveData.ret[0]:
			self._updateBellsModel()
			self.showMainMessage=[True,self.saveData.ret[1],"Ok"]
		else:
			self.showMainMessage=[True,self.saveData.ret[1],"Error"]	

		self.closePopUp=[True,""]
		self.changesInBell=False
		self.closeGui=True
		self.moveToStack=1
		self._manageGoToStack()

	#def _saveDataRet

	@Slot()
	def cancelBellChanges(self):

		self._cancelBellChanges()

	#def cancellBellChanges

	def _cancelBellChanges(self):

		self.changesInBell=False
		self.closeGui=True
		self.moveToStack=1
		self._manageGoToStack()

	#def _cancelBellChanges

	@Slot('QVariantList')
	def changeBellStatus(self,data):

		self.closeGui=False
		self.closePopUp=[False,CHANGE_BELL_STATUS]
		self.changeStatus=ChangeBellStatus(data)
		self.changeStatus.start()
		self.changeStatus.finished.connect(self._changeBellStatusRet)

	#def changeBellStatus

	def _changeBellStatusRet(self):

		if self.changeStatus.ret[0]:
			self._updateBellsModelInfo('bellActivated')
			self.showMainMessage=[True,self.changeStatus.ret[1],"Ok"]
		else:
			self.showMainMessage=[True,self.changeStatus.ret[1],"Error"]

		self.closePopUp=[True,""]
		self.closeGui=True

	#def _changeBellStatusRet

	@Slot(str)
	def removeBell(self,bellToRemove):

		self.bellToRemove=bellToRemove
		self.showRemoveBellDialog=True

	#def removeBell

	@Slot(str)
	def manageRemoveBellDialog(self,response):

		self.showRemoveBellDialog=False
		if response=="Accept":
			self._launchRemoveBellProcess()

	#def manageRemoveBellDialog

	def _launchRemoveBellProcess(self):

		self.closeGui=False
		self.closePopUp=[False,6]
		self.removeBellProcess=RemoveBell(self.bellToRemove)
		self.removeBellProcess.start()
		self.removeBellProcess.finished.connect(self._removeBellProcessRet)

	#def _launchRemoveBellProcess

	def _removeBellProcessRet(self):

		if self.removeBellProcess.ret[0]:
			self._updateBellsModel()
			self.showMainMessage=[True,self.removeBellProcess.ret[1],"Ok"]
		else:
			self.showMainMessage=[False,self.removeBellProcess.ret[1],"Error"]

		self.closePopUp=[True,""]
		self.closeGui=True

	#def _removeBellProcessRet

	def _manageGoToStack(self):

		if self.moveToStack!="":
			self.currentStack=self.moveToStack
			self.mainCurrentOption=0
			self.moveToStack=""

	#def _manageGoToStack

	@Slot()
	def openHelp(self):
		lang=os.environ["LANG"]

		if 'valencia' in lang:
			self.help_cmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Bell-Scheduler.'
		else:
			self.help_cmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Bell-Scheduler'
		
		self.open_help_t=threading.Thread(target=self._openHelp)
		self.open_help_t.daemon=True
		self.open_help_t.start()

	#def openHelp

	def _openHelp(self):

		os.system(self.help_cmd)

	#def _openHelp

	@Slot()
	def closeBellScheduler(self):

		#Bridge.onedriveMan.deleteTempConfig()

		if self.changesInBell:
			self.closeGui=False
			self.showChangesInBellDialog=True
		else:
			self.closeGui=True

	#def closeBellScheduler
	
	on_bellCron=Signal()
	bellCron=Property('QVariantList',_getBellCron,_setBellCron,notify=on_bellCron)

	on_bellDays=Signal()
	bellDays=Property('QVariantList',_getBellDays,_setBellDays,notify=on_bellDays)

	on_bellValidityActive=Signal()
	bellValidityActive=Property(bool,_getBellValidityActive,_setBellValidityActive,notify=on_bellValidityActive)

	on_bellValidityValue=Signal()
	bellValidityValue=Property(str,_getBellValidityValue,_setBellValidityValue,notify=on_bellValidityValue)
	
	on_bellValidityRangeOption=Signal()
	bellValidityRangeOption=Property(bool,_getBellValidityRangeOption,_setBellValidityRangeOption,notify=on_bellValidityRangeOption)

	on_bellValidityDaysInRange=Signal()
	bellValidityDaysInRange=Property('QVariantList',_getBellValidityDaysInRange,_setBellValidityDaysInRange,notify=on_bellValidityDaysInRange)

	on_enableBellValidity=Signal()
	enableBellValidity=Property(bool,_getEnableBellValidity,_setEnableBellValidity,notify=on_enableBellValidity)

	on_bellName=Signal()
	bellName=Property(str,_getBellName,_setBellName,notify=on_bellName)

	on_bellImage=Signal()
	bellImage=Property('QVariantList',_getBellImage,_setBellImage,notify=on_bellImage)

	on_bellSound=Signal()
	bellSound=Property('QVariantList',_getBellSound,_setBellSound,notify=on_bellSound)

	on_bellStartIn=Signal()
	bellStartIn=Property(int,_getBellStartIn,_setBellStartIn,notify=on_bellStartIn)

	on_bellDuration=Signal()
	bellDuration=Property(int,_getBellDuration,_setBellDuration,notify=on_bellDuration)

	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_mainCurrentOption=Signal()
	mainCurrentOption=Property(int,_getMainCurrentOption,_setMainCurrentOption, notify=on_mainCurrentOption)

	on_showMainMessage=Signal()
	showMainMessage=Property('QVariantList',_getShowMainMessage,_setShowMainMessage, notify=on_showMainMessage)
	
	on_showBellFormMessage=Signal()
	showBellFormMessage=Property('QVariantList',_getShowBellFormMessage,_setShowBellFormMessage, notify=on_showBellFormMessage)
	on_showLoadErrorMessage=Signal()
	showLoadErrorMessage=Property('QVariantList',_getShowLoadErrorMessage,_setShowLoadErrorMessage, notify=on_showLoadErrorMessage)

	on_bellCurrentOption=Signal()
	bellCurrentOption=Property(int,_getBellCurrentOption,_setBellCurrentOption, notify=on_bellCurrentOption)

	on_closePopUp=Signal()
	closePopUp=Property('QVariantList',_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_showChangesInBellDialog=Signal()
	showChangesInBellDialog=Property(bool,_getShowChangesInBellDialog,_setShowChangesInBellDialog,notify=on_showChangesInBellDialog)

	on_changesInBell=Signal()
	changesInBell=Property(bool,_getChangesInBell,_setChangesInBell,notify=on_changesInBell)

	on_showRemoveBellDialog=Signal()
	showRemoveBellDialog=Property(bool,_getShowRemoveBellDialog,_setShowRemoveBellDialog,notify=on_showRemoveBellDialog)

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	systemLocale=Property(str,_getSystemLocale,constant=True)
	imagesModel=Property(QObject,_getImagesModel,constant=True)
	bellsModel=Property(QObject,_getBellsModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
