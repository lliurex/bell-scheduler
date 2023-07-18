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

class Bridge(QObject):

	bellMan=BellManager.BellManager()

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self._bellsModel=BellsModel.BellsModel()
		self._imagesModel=ImagesModel.ImagesModel()
		self._bellCron=Bridge.bellMan.bellCron
		self._bellDays=Bridge.bellMan.bellDays
		self._bellValidity=Bridge.bellMan.bellValidity
		self._validityRangeDate=True
		self._daysInRange=[]
		self._bellName=Bridge.bellMan.bellName
		self._bellImage=Bridge.bellMan.bellImage
		self._bellSound=Bridge.bellMan.bellSound
		self._bellPlay=Bridge.bellMan.bellPlay
		self._currentStack=0
		self._mainCurrentOption=0
		self._bellCurrentOption=0
		self._closeGui=False
		self._showMainMessage=[False,"","Ok"]
		self._showLoadErrorMessage=[False,""]

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

	def _getValidityRangeDate(self):

		return self._validityRangeDate

	#def _getValidityRangeDate

	def _setValidityRangeDate(self,validityRangeDate):

		if self._validityRangeDate!=validityRangeDate:
			self._validityRangeDate=validityRangeDate
			self.on_validityRangeDate.emit()

	#def _setValidityRangeDate

	def _getDaysInRange(self):

		return self._daysInRange

	#def _getDaysInRange

	def _setDaysInRange(self,daysInRange):

		if self._daysInRange!=daysInRange:
			self._daysInRange=daysInRange
			self.on_daysInRange.emit()

	#def _setDaysInRange

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

	@Slot()
	def addNewBell(self):

		self._initializeVars()
		self.currentStack=2
		self.bellCurrentOption=0
		
	#def addNewBell

	def _initializeVars(self):

		Bridge.bellMan.initValues()
		self.currentBellConfig=copy.deepcopy(Bridge.bellMan.initBellConfig)
		self.bellCron=Bridge.bellMan.bellCron
		self.bellDays=Bridge.bellMan.bellDays
		self.bellValidity=Bridge.bellMan.bellValidity
		self.validityRangeDate=Bridge.bellMan.validityRangeDate
		self.daysInRange=Bridge.bellMan.daysInRange
		self.bellName=Bridge.bellMan.bellName
		self.bellImage=Bridge.bellMan.bellImage
		self.bellSound=Bridge.bellMan.bellSound
		self.bellPlay=Bridge.bellMan.bellPlay

	#def _initializeVars

	def _updateImagesModel(self):

		ret=self._imagesModel.clear()
		imagesEntries=Bridge.bellMan.imagesConfigData
		for item in imagesEntries:
			if item["imageSource"]!="":
				self._imagesModel.appendRow(item["imageSource"])
	
	#def _updateImagesModel

	@Slot()
	def goHome(self):

		self.currentStack=1
		self.mainCurrentOption=0			

	#def goHome

	@Slot(str)
	def loadBell(self,bellId):

		Bridge.bellMan.initValues()
		Bridge.bellMan.loadBellConfig(bellId)
		self.currentBellConfig=copy.deepcopy(Bridge.bellMan.currentBellConfig)
		self.bellCron=Bridge.bellMan.bellCron
		self.bellDays=Bridge.bellMan.bellDays
		self.bellValidity=Bridge.bellMan.bellValidity
		self.validityRangeDate=Bridge.bellMan.validityRangeDate
		self.daysInRange=Bridge.bellMan.daysInRange
		self.bellName=Bridge.bellMan.bellName
		self.bellImage=Bridge.bellMan.bellImage
		self.bellSound=Bridge.bellMan.bellSound
		self.bellPlay=Bridge.bellMan.bellPlay
		self.currentStack=2
		self.bellCurrentOption=0

	#def loadBell

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

		self.closeGui=True

	#def closeBellScheduler
	
	on_bellCron=Signal()
	bellCron=Property('QVariantList',_getBellCron,_setBellCron,notify=on_bellCron)

	on_bellDays=Signal()
	bellDays=Property('QVariantList',_getBellDays,_setBellDays,notify=on_bellDays)

	on_bellValidity=Signal()
	bellValidity=Property('QVariantList',_getBellValidity,_setBellValidity,notify=on_bellValidity)

	on_validityRangeDate=Signal()
	validityRangeDate=Property(bool,_getValidityRangeDate,_setValidityRangeDate,notify=on_validityRangeDate)

	on_daysInRange=Signal()
	daysInRange=Property('QVariantList',_getDaysInRange,_setDaysInRange,notify=on_daysInRange)

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

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	imagesModel=Property(QObject,_getImagesModel,constant=True)
	bellsModel=Property(QObject,_getBellsModel,constant=True)

#class Bridge

if __name__=="__main__":

	pass
