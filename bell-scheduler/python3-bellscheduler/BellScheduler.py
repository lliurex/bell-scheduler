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


class Bridge(QObject):

	bellMan=BellManager.BellManager()

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self._bellsModel=BellsModel.BellsModel()
		self._imagesModel=ImagesModel.ImagesModel()
		self._bellCron=Bridge.bellMan.bellCron
		self._bellDays=Bridge.bellMan.bellDays
		self._bellValidity=Bridge.bellMan.bellValidity
		self._bellValidityRangeOption=True
		self._bellValidityDaysInRange=[]
		self._enableBellValidity=False
		self._bellName=Bridge.bellMan.bellName
		self._bellImage=Bridge.bellMan.bellImage
		self._bellSound=Bridge.bellMan.bellSound
		self._bellPlay=Bridge.bellMan.bellPlay
		self._currentStack=0
		self._mainCurrentOption=0
		self._bellCurrentOption=0
		self._closePopUp=[True,""]
		self.moveToStack=""
		self._closeGui=False
		self._showMainMessage=[False,"","Ok"]
		self._showLoadErrorMessage=[False,""]
		self._showChangesInBellDialog=False
		self._changesInBell=False
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
					self.showMainMessage=[True,Bridge.bellMan.SOUND_PATH_UNAVAILABLE,"Error"]
			else:
				self.showLoadErrorMessage=[True,self.gatherInfo.readConf['code']]
		else:
			self.showLoadErrorMessage=[True,self.gatherInfo.syncWithCron['code']]
	
	#def _loadConfig

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

	def _getBellValidity(self):

		return self._bellValidity

	#def _getBellValidity

	def _setBellValidity(self,bellValidity):

		if self._bellValidity!=bellValidity:
			self._bellValidity=bellValidity
			self.on_bellValidity.emit()

	#def _setBellValidity

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

	def _getBellPlay(self):

		return self._bellPlay

	#def _getBellPlay

	def _setBellPlay(self,bellPlay):

		if self._bellPlay!=bellPlay:
			self._bellPlay=bellPlay
			self.on_bellPlay.emit()

	#def _setBellPlay  

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
		self.bellValidity=Bridge.bellMan.bellValidity
		self.bellValidityRangeOption=Bridge.bellMan.bellValidityRangeOption
		self.bellValidityDaysInRange=Bridge.bellMan.bellValidityDaysInRange
		self.enableBellValidity=Bridge.bellMan.enableBellValidity
		self.bellName=Bridge.bellMan.bellName
		self.bellImage=Bridge.bellMan.bellImage
		self.bellSound=Bridge.bellMan.bellSound
		self.bellPlay=Bridge.bellMan.bellPlay

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

		self.enableBellValidity=Bridge.bellMan.checkIfValidityIsEnabled(self.bellDays)
		
		if self.currentBellConfig!=Bridge.bellMan.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateWeekDaysValues

	@Slot(str,result=bool)
	def checkMimetypeImage(self,imagePath):

		return Bridge.bellMan.checkMimetypes(imagePath,"image")

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

	@Slot(str)
	def manageChangesDialog(self,action):

		self.showChangesInBellDialog=False

		if action=="Accept":
			self.applyBellChanges()
		elif action=="Discard":
			self.cancelBellChanges()
		elif action=="Cancel":
			pass

	#def manageChangesDialog

	def applyBellChanges(self):

		self.changesInBell=False
		self.closeGui=True
		self.moveToStack=1
		self._manageGoToStack()

	#def applyBellChanges

	@Slot()
	def cancelBellChanges(self):

		self.changesInBell=False
		self.closeGui=True
		self.moveToStack=1
		self._manageGoToStack()	

	#def cancellBellChanges

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

	on_bellValidity=Signal()
	bellValidity=Property('QVariantList',_getBellValidity,_setBellValidity,notify=on_bellValidity)

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

	on_bellPlay=Signal()
	bellPlay=Property('QVariantList',_getBellPlay,_setBellPlay,notify=on_bellPlay)

	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_mainCurrentOption=Signal()
	mainCurrentOption=Property(int,_getMainCurrentOption,_setMainCurrentOption, notify=on_mainCurrentOption)

	on_showMainMessage=Signal()
	showMainMessage=Property('QVariantList',_getShowMainMessage,_setShowMainMessage, notify=on_showMainMessage)
	
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

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	imagesModel=Property(QObject,_getImagesModel,constant=True)
	bellsModel=Property(QObject,_getBellsModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
