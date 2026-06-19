from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from . import ImagesModel

NEW_BELL_CONFIG=1
LOAD_BELL_CONFIG=2
DUPLICATE_BELL_CONFIG=17
CHECK_DATA=3
SAVE_DATA=4

class LoadBell(QThread):

	bellLoaded=Signal()

	def __init__(self,manager,newBell,bellInfo,duplicateBell):

		super().__init__()
		self.manager=manager
		self.newBell=newBell
		self.bellInfo=bellInfo
		self.duplicateBell=duplicateBell

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		ret=self.manager.initValues()
		if not self.newBell:
			ret=self.manager.loadBellConfig(self.bellInfo,self.duplicateBell)
		
		self.bellLoaded.emit()

	#def run

#class LoadBell

class CheckData(QThread):

	dataChecked=Signal(dict)

	def __init__(self,manager,data):

		super().__init__()
		self.manager=manager
		self.dataToCheck=data
	
	#def __init__

	def run(self,*args):

		time.sleep(0.2)
		ret=self.manager.checkData(self.dataToCheck)
		if ret.get("status"):
			ret["checkDuplicate"]=self.manager.checkDuplicateBellCron(self.dataToCheck)

		self.dataChecked.emit(ret)
		
	#def run

#class CheckData

class SaveData(QThread):

	dataSaved=Signal(dict)

	def __init__(self,manager,data):

		super().__init__()
		self.manager=manager
		self.dataToSave=data

	#def __init__

	def run(self,*args):

		time.sleep(0.2)
		ret=self.manager.saveData(self.dataToSave)
		self.dataSaved.emit(ret)

	#def run

#class SaveData

class Bridge(QObject):

	bellCronChanged=Signal()
	bellDaysChanged=Signal()
	bellValidityActiveChanged=Signal()
	bellValidityChanged=Signal()
	enableBellValidityChanged=Signal()
	bellNameChanged=Signal()
	bellImageChanged=Signal()
	bellSoundChanged=Signal()
	bellStartInChanged=Signal()
	bellDurationChanged=Signal()
	showBellFormMessageChanged=Signal()
	bellCurrentOptionChanged=Signal()
	showChangesInBellDialogChanged=Signal()
	changesInBellChanged=Signal()
	actionTypeChanged=Signal()
	showBellDuplicateDialogChanged=Signal()

	def __init__(self):

		super().__init__()
		self.core=Core.Core.get_core()
		self.bellManager=self.core.bellManager
		self._imagesModel=ImagesModel.ImagesModel()
		self._bellCron=self.bellManager.bellCron
		self._bellDays=self.bellManager.bellDays
		self._bellValidityActive=self.bellManager.bellValidityActive
		self._bellValidity=self.bellManager.bellValidity
		self._enableBellValidity=False
		self._bellName=self.bellManager.bellName
		self._bellImage=self.bellManager.bellImage
		self._bellSound=self.bellManager.bellSound
		self._bellStartIn=self.bellManager.bellStartIn
		self._bellDuration=self.bellManager.bellDuration
		self._bellCurrentOption=0
		self._showBellFormMessage={"show":False,"msgCode":""}
		self._showChangesInBellDialog=False
		self._changesInBell=False
		self._actionType="add"
		self._showBellDuplicateDialog=False

	#def _init_

	@Property('QVariant',notify=bellCronChanged)
	def bellCron(self):

		return self._bellCron

	#def bellCron

	@bellCron.setter
	def bellCron(self,bellCron):

		if self._bellCron!=bellCron:
			self._bellCron=bellCron
			self.bellCronChanged.emit()

	#def bellCron

	@Property('QVariant',notify=bellDaysChanged)
	def bellDays(self):

		return self._bellDays

	#def bellDays

	@bellDays.setter
	def bellDays(self,bellDays):

		if self._bellDays!=bellDays:
			self._bellDays=bellDays
			self.bellDaysChanged.emit()

	#def bellDays

	@Property(bool,notify=bellValidityActiveChanged)
	def bellValidityActive(self):

		return self._bellValidityActive

	#def bellValidityActive

	@bellValidityActive.setter
	def bellValidityActive(self,bellValidityActive):

		if self._bellValidityActive!=bellValidityActive:
			self._bellValidityActive=bellValidityActive
			self.bellValidityActiveChanged.emit()

	#def bellValidityActive

	@Property('QVariant',notify=bellValidityChanged)
	def bellValidity(self):

		return self._bellValidity

	#def bellValidity

	@bellValidity.setter
	def bellValidity(self,bellValidity):

		if self._bellValidity!=bellValidity:
			self._bellValidity=bellValidity
			self.bellValidityChanged.emit()

	#def bellValidityValue

	@Property(bool,notify=enableBellValidityChanged)
	def enableBellValidity(self):

		return self._enableBellValidity

	#def enableBellValidity

	@enableBellValidity.setter
	def enableBellValidity(self,enableBellValidity):

		if self._enableBellValidity!=enableBellValidity:
			self._enableBellValidity=enableBellValidity
			self.enableBellValidityChanged.emit()

	#def enableBellValidity

	@Property(str,notify=bellNameChanged)
	def bellName(self):

		return self._bellName

	#def bellName

	@bellName.setter
	def bellName(self,bellName):

		if self._bellName!=bellName:
			self._bellName=bellName
			self.bellNameChanged.emit()

	#def _setBellName 

	@Property('QVariant',notify=bellImageChanged)
	def bellImage(self):

		return self._bellImage

	#def bellImage

	@bellImage.setter
	def bellImage(self,bellImage):

		if self._bellImage!=bellImage:
			self._bellImage=bellImage
			self.bellImageChanged.emit()

	#def bellImage

	@Property('QVariant',notify=bellSoundChanged)
	def bellSound(self):

		return self._bellSound

	#def bellSound

	@bellSound.setter
	def bellSound(self,bellSound):

		if self._bellSound!=bellSound:
			self._bellSound=bellSound
			self.bellSoundChanged.emit()

	#def bellSound

	@Property(int,notify=bellStartInChanged)
	def bellStartIn(self):

		return self._bellStartIn

	#def bellStartIn

	@bellStartIn.setter
	def bellStartIn(self,bellStartIn):

		if self._bellStartIn!=bellStartIn:
			self._bellStartIn=bellStartIn
			self.bellStartInChanged.emit()

	#def bellStartIn

	@Property(int,notify=bellDurationChanged)
	def bellDuration(self):

		return self._bellDuration

	#def bellDuration

	@bellDuration.setter
	def bellDuration(self,bellDuration):

		if self._bellDuration!=bellDuration:
			self._bellDuration=bellDuration
			self.bellDurationChanged.emit()

	#def _setBellDuration

	@Property('QVariant',notify=showBellFormMessageChanged)
	def showBellFormMessage(self):

		return self._showBellFormMessage

	#def showBellFormMessage

	@showBellFormMessage.setter
	def showBellFormMessage(self,showBellFormMessage):

		if self._showBellFormMessage!=showBellFormMessage:
			self._showBellFormMessage=showBellFormMessage
			self.showBellFormMessageChanged.emit()

	#def showBellFormMessage

	@Property(int,notify=bellCurrentOptionChanged)
	def bellCurrentOption(self):

		return self._bellCurrentOption

	#def bellCurrentOption	

	@bellCurrentOption.setter
	def bellCurrentOption(self,bellCurrentOption):
		
		if self._bellCurrentOption!=bellCurrentOption:
			self._bellCurrentOption=bellCurrentOption
			self.bellCurrentOptionChanged.emit()

	#def bellCurrentOption

	@Property(bool,notify=showChangesInBellDialogChanged)
	def showChangesInBellDialog(self):

		return self._showChangesInBellDialog

	#def showChangesInBellDialog

	@showChangesInBellDialog.setter
	def showChangesInBellDialog(self,showChangesInBellDialog):

		if self._showChangesInBellDialog!=showChangesInBellDialog:
			self._showChangesInBellDialog=showChangesInBellDialog
			self.showChangesInBellDialogChanged.emit()

	#def showChangesInBellDialog

	@Property(bool,notify=changesInBellChanged)
	def  changesInBell(self):

		return self._changesInBell

	#def changesInBell

	@changesInBell.setter
	def changesInBell(self,changesInBell):

		if self._changesInBell!=changesInBell:
			self._changesInBell=changesInBell
			self.changesInBellChanged.emit()

	#def changesInBell
	
	@Property(str,notify=actionTypeChanged)
	def actionType(self):

		return self._actionType

	#def actionType

	@actionType.setter
	def actionType(self,actionType):

		if self._actionType!=actionType:
			self._actionType=actionType
			self.actionTypeChanged.emit()

	#def actionType

	@Property(bool,notify=showBellDuplicateDialogChanged)
	def showBellDuplicateDialog(self):

		return self._showBellDuplicateDialog

	#def showBellDuplicateDialog

	@showBellDuplicateDialog.setter
	def showBellDuplicateDialog(self,showBellDuplicateDialog):

		if self._showBellDuplicateDialog!=showBellDuplicateDialog:
			self._showBellDuplicateDialog=showBellDuplicateDialog
			self.showBellDuplicateDialogChanged.emit()

	#def _setShowBellDuplicateDialog

	def _getImagesModel(self):

		return self._imagesModel

	#def _getImagesModel	

	def updateImagesModel(self):

		ret=self._imagesModel.clear()
		imagesEntries=self.bellManager.imagesConfigData
		for item in imagesEntries:
			if item["imageSource"]!="":
				self._imagesModel.appendRow(item["imageSource"])
	
	#def updateImagesModel

	@Slot()
	def addNewBell(self,soundFile=None):

		self.fileFromMenu=soundFile
		duplicateBell=False
		actionType="add"
		
		if self.fileFromMenu==None:
			self.core.mainStack.showPopUp={"show":True,"msgCode":NEW_BELL_CONFIG}
			self.core.bellsOptionsStack.showMainMessage={"show":False,"msgCode":"","type":""}
		
		self.newBellT=LoadBell(self.bellManager,True,"",duplicateBell)
		self.newBellT.start()
		self.newBellT.bellLoaded.connect(self._addNewBellRet)
		self.newBellT.finished.connect(self.newBellT.deleteLater)

	#def addNewBell

	@Slot()
	def _addNewBellRet(self):

		self.currentBellConfig=copy.deepcopy(self.bellManager.currentBellConfig)
		self._initializeVars()
		if self.fileFromMenu==None:
			self.core.mainStack.showPopUp={"show":False,"msgCode":""}
		else:
			tmpSound={
				"option":"file",
				"path":self.fileFromMenu,
				"defaultPath":True
			}
			self.updateSoundValues(tmpSound)
		
		self.core.mainStack.currentStack=2
		self.bellCurrentOption=1

	#def _addNewBellRet

	def _initializeVars(self):

		self.bellCron=self.bellManager.bellCron
		self.bellDays=self.bellManager.bellDays
		self.bellValidityActive=self.bellManager.bellValidityActive
		self.bellValidity=self.bellManager.bellValidity
		self.enableBellValidity=self.bellManager.enableBellValidity
		self.bellName=self.bellManager.bellName
		self.bellImage=self.bellManager.bellImage
		self.bellSound=self.bellManager.bellSound
		self.bellStartIn=self.bellManager.bellStartIn
		self.bellDuration=self.bellManager.bellDuration
		self.showBellFormMessage={"show":False,"msgCode":""}
		self.changesInBell=False

	#def _initializeVars

	@Slot()
	def goHome(self):

		if not self.changesInBell:
			self.core.mainStack.currentStack=1
			self.core.mainStack.mainCurrentOption=0
			self.bellCurrentOption=0
			self.core.mainStack.moveToStack=""
		else:
			self.showChangesInBellDialog=True
			self.core.mainStack.moveToStack=1

	#def goHome

	@Slot('QJSValue')
	def loadBell(self,bellToLoad):

		bellToLoad=bellToLoad.toVariant()

		self.core.mainStack.showPopUp={"show":True,"msgCode":LOAD_BELL_CONFIG}
		self.core.bellsOptionsStack.showMainMessage={"show":False,"msgCode":"","typ":""}
		duplicateBell=False
		self.actionType="edit"
		self.editBellT=LoadBell(self.bellManager,False,bellToLoad,duplicateBell)
		self.editBellT.start()
		self.editBellT.bellLoaded.connect(self._loadBellRet)
		self.editBellT.finished.connect(self.editBellT.deleteLater)

	#def loadBell

	@Slot()
	def _loadBellRet(self):

		self.currentBellConfig=copy.deepcopy(self.bellManager.currentBellConfig)
		self._initializeVars()
		self.core.mainStack.showPopUp={"show":False,"msgCode":""}
		self.core.mainStack.currentStack=2
		self.bellCurrentOption=1

	#def _loadBellRet

	@Slot('QJSValue')
	def duplicateBell(self,bellToDuplicate):

		bellToDuplicate=bellToDuplicate.toVariant()

		self.core.mainStack.showPopUp={"show":True,"msgCode":DUPLICATE_BELL_CONFIG}
		self.core.bellsOptionsStack.showMainMessage={"show":False,"msgCode":"","type":""}
		self.actionType="duplicate"
		duplicateBell=True
		self.cloneBellT=LoadBell(self.bellManager,False,bellToDuplicate,duplicateBell)
		self.cloneBellT.start()
		self.cloneBellT.bellLoaded.connect(self._cloneBellRet)
		self.cloneBellT.finished.connect(self.cloneBellT.deleteLater)

	#def duplicateBell

	@Slot()
	def _cloneBellRet(self):

		self.currentBellConfig=copy.deepcopy(self.bellManager.currentBellConfig)
		self._initializeVars()
		self.core.mainStack.showPopUp={"show":False,"msgCode":""}
		self.core.mainStack.currentStack=2
		self.bellCurrentOption=1

	#def _cloneBellRet

	@Slot('QJSValue')
	def updateClockValues(self,data):

		data=data.toVariant()
		changes={key:value for key,value in data.items() if self.bellCron[key]!=value}

		if changes:
			self.bellCron={**self.bellCron,**changes}
			self.currentBellConfig["hour"]=self.bellCron["hour"]
			self.currentBellConfig["minute"]=self.bellCron["minute"]
		
		if self.currentBellConfig!=self.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateClockValues

	@Slot('QJSValue')
	def updateWeekDaysValues(self,data):

		data=data.toVariant()
		changes={key:value for key,value in data.items() if self.bellDays[key]!=value}

		if changes:
			self.bellDays={**self.bellDays,**changes}
			self.currentBellConfig["weekdays"]=self.bellDays
		
		self.enableBellValidity=self.bellManager.areDaysChecked(self.currentBellConfig["weekdays"])
		
		if self.currentBellConfig!=self.bellManager.currentBellConfig:
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

		if self.currentBellConfig!=self.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def _updateBellValidityActive

	@Slot('QJSValue')
	def updateBellValidity(self,data):

		data=data.toVariant()
		changes={key:value for key,value in data.items() if self.bellValidity[key]!=value}

		if changes:
			changes["daysInRange"]=self.bellManager.getDaysInRange(changes.get("value"))
			self.bellValidity={**self.bellValidity,**changes}
			self.currentBellConfig["validity"]["value"]=self.bellValidity.get("value")

		if data.get("value")!="":
			if self.currentBellConfig!=self.bellManager.currentBellConfig:
				self.changesInBell=True
			else:
				self.changesInBell=False
		else:
			self._updateBellValidityActive(False)

	#def updateBellValidity

	@Slot(str)
	def updateBellNameValue(self,value):

		if value!=self.bellName:
			self.bellName=value
			self.currentBellConfig["name"]=self.bellName

		if self.currentBellConfig!=self.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateBellNameValue

	@Slot(str,result=bool)
	def checkMimetypeImage(self,imagePath):

		return self.bellManager.checkMimetypes(imagePath,"image").get("status")

	#def checkMimetypeImage

	@Slot('QJSValue')
	def updateImageValues(self,data):

		data=data.toVariant()

		if data.get("option")=="stock":
			data["path"]=self.bellManager.imagesConfigData[data.get("index")]["imageSource"]
		
		data["error"]=False if os.path.exists(data.get("path")) else True

		if self.bellImage!=data:
			self.bellImage=data
			self.currentBellConfig["image"]["option"]=self.bellImage.get("option")
			self.currentBellConfig["image"]["path"]=self.bellImage.get("path")
	
		if self.currentBellConfig!=self.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateImageValues

	@Slot(str,result=bool)
	def checkMimetypeSound(self,soundPath):

		return self.bellManager.checkMimetypes(soundPath,"audio").get("status")

	#def checkMimetypeSound

	@Slot('QJSValue')
	def updateSoundValues(self,data):

		data=data.toVariant()
		data["error"]=False if os.path.exists(data.get("path")) else True

		if self.bellSound!=data:
			self.bellSound=data
			self.currentBellConfig["sound"]["option"]=self.bellSound.get("option")
			self.currentBellConfig["sound"]["path"]=self.bellSound.get("path")
			self.currentBellConfig["soundDefaultPath"]=self.bellSound.get("defaultPath")

		if self.currentBellConfig!=self.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateSoundValues

	@Slot(int)
	def updateStartInValue(self,value):

		if value!=self.bellStartIn:
			self.bellStartIn=value
			self.currentBellConfig["play"]["start"]=self.bellStartIn

		if self.currentBellConfig!=self.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateStartInValue

	@Slot(int)
	def updateDurationValue(self,value):

		if value!=self.bellDuration:
			self.bellDuration=value
			self.currentBellConfig["play"]["duration"]=self.bellDuration

		if self.currentBellConfig!=self.bellManager.currentBellConfig:
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

		self.core.mainStack.showPopUp={"show":True,"msgCode":CHECK_DATA}
		self.core.mainStack.closeGui=False
		self.checkDataT=CheckData(self.bellManager,self.currentBellConfig)
		self.checkDataT.start()
		self.checkDataT.dataChecked.connect(self._checkDataRet)
		self.checkDataT.finished.connect(self.checkDataT.deleteLater)

	#def _applyBellChanges

	@Slot(dict)
	def _checkDataRet(self,ret):

		if ret.get("status"):
			if ret.get("checkDuplicate"):
				self.saveDataChanges()
			else:
				self.core.mainStack.showPopUp={"show":False,"msgCode":""}
				self.showBellDuplicateDialog=True
		else:
			self.core.mainStack.showPopUp={"show":False,"msgCode":""}
			self.showBellFormMessage={"show":True,"msgCode":ret.get("code")}

	#def _checkDataRet

	@Slot(bool)

	def manageDuplicateDialog(self,response):

		self.showBellDuplicateDialog=False
		if response:
			self.saveDataChanges()

	#def manageDuplicateDialog

	def saveDataChanges(self):

		self.core.mainStack.showPopUp={"show":True,"msgCode":SAVE_DATA}
		self.saveDataT=SaveData(self.bellManager,self.currentBellConfig)
		self.saveDataT.start()
		self.saveDataT.dataSaved.connect(self._saveDataRet)
		self.saveDataT.finished.connect(self.saveDataT.deleteLater)

	#def saveData

	@Slot(dict)
	def _saveDataRet(self,ret):

		if ret.get("status"):
			self.core.bellsOptionsStack._updateBellsModel()
		
		self.core.bellsOptionsStack.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
	
		self.core.bellsOptionsStack.enableGlobalOptions=self.bellManager.checkGlobalOptionStatus()
		self.core.bellsOptionsStack.enableChangeStatusOptions=self.bellManager.checkChangeStatusBellsOption()
		self.core.bellsOptionsStack.showExportBellsWarning=self.bellManager.checkIfAreBellsWithDirectory()
		self.changesInBell=False
		self.core.mainStack.closeGui=True
		self.core.mainStack.moveToStack=1
		self.core.mainStack.manageGoToStack()
		self.core.mainStack.showPopUp={"show":False,"msgCode":""}

	#def _saveDataRet

	@Slot()
	def cancelBellChanges(self):

		self._cancelBellChanges()

	#def cancellBellChanges

	def _cancelBellChanges(self):

		self.changesInBell=False
		self.core.mainStack.closeGui=True
		self.core.mainStack.moveToStack=1
		self.core.mainStack.manageGoToStack()

	#def _cancelBellChanges

	imagesModel=Property(QObject,_getImagesModel,constant=True)

#class Bridge

from . import Core


