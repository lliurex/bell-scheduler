from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
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

		ret=self.manager.initValues()
		if not self.newBell:
			ret=self.manager.loadBellConfig(self.bellInfo,self.duplicateBell)
		
		self.bellLoaded.emit()

	#def run

#class LoadBell

class CheckData(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.dataToCheck=args[0]
		self.retData={}
		self.retDuplicate={}

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.retData=self.bellManager.checkData(self.dataToCheck)
		if self.retData:
			self.retDuplicate=self.bellManager.checkDuplicateBellCron(self.dataToCheck)
		
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
		self.ret=self.bellManager.saveData(self.dataToSave)

	#def run

#class SaveData

class Bridge(QObject):

	bellCronChanged=Signal()
	bellDaysChanged=Signal()
	bellValidityActiveChanged=Signal()
	bellValidityValueChanged=Signal()
	bellValidityRangeOptionChanged=Signal()
	bellValidityDaysInRangeChanged=Signal()
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
		self._bellValidityValue=self.bellManager.bellValidityValue
		self._bellValidityRangeOption=True
		self._bellValidityDaysInRange=[]
		self._enableBellValidity=False
		self._bellName=self.bellManager.bellName
		self._bellImage=self.bellManager.bellImage
		self._bellSound=self.bellManager.bellSound
		self._bellStartIn=self.bellManager.bellStartIn
		self._bellDuration=self.bellManager.bellDuration
		self._bellCurrentOption=0
		self._showBellFormMessage={"show":False,"msgCode":"","type":""}
		self._showChangesInBellDialog=False
		self._changesInBell=False
		self._actionType="add"
		self._showBellDuplicateDialog=False

	#def _init_

	@Property(dict,notify=bellCronChanged)
	def bellCron(self):

		return self._bellCron

	#def bellCron

	@bellCron.setter
	def bellCron(self,bellCron):

		if self._bellCron!=bellCron:
			self._bellCron=bellCron
			self.bellCronChanged.emit()

	#def bellCron

	@Property(list,notify=bellDaysChanged)
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

	@Property(str,notify=bellValidityValueChanged)
	def bellValidityValue(self):

		return self._bellValidityValue

	#def bellValidityValue

	@bellValidityValue.setter
	def bellValidityValue(self,bellValidityValue):

		if self._bellValidityValue!=bellValidityValue:
			self._bellValidityValue=bellValidityValue
			self.bellValidityValueChanged.emit()

	#def bellValidityValue

	@Property(bool,notify=bellValidityRangeOptionChanged)
	def bellValidityRangeOption(self):

		return self._bellValidityRangeOption

	#def bellValidityRangeOption

	@bellValidityRangeOption.setter
	def bellValidityRangeOption(self,bellValidityRangeOption):

		if self._bellValidityRangeOption!=bellValidityRangeOption:
			self._bellValidityRangeOption=bellValidityRangeOption
			self.bellValidityRangeOptionChanged.emit()

	#def bellValidityRangeOption

	@Property(list,notify=bellValidityDaysInRangeChanged)
	def bellValidityDaysInRange(self):

		return self._bellValidityDaysInRange

	#def bellValidityDaysInRange

	@bellValidityDaysInRange.setter
	def bellValidityDaysInRange(self,bellValidityDaysInRange):

		if self._bellValidityDaysInRange!=bellValidityDaysInRange:
			self._bellValidityDaysInRange=bellValidityDaysInRange
			self.bellValidityDaysInRangeChanged.emit()

	#def bellValidityDaysInRange

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

	@Property(dict,notify=bellImageChanged)
	def bellImage(self):

		return self._bellImage

	#def bellImage

	@bellImage.setter
	def bellImage(self,bellImage):

		if self._bellImage!=bellImage:
			self._bellImage=bellImage
			self.bellImageChanged.emit()

	#def bellImage

	@Property(dict,notify=bellSoundChanged)
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

	@Property(dict,notify=showBellFormMessageChanged)
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

	@Property(QObject,constant=True)
	def imagesModel(self):

		return self._imagesModel

	#def imagesModel	

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
			self.core.mainStack.showPopup={"show":True,"msgCode":NEW_BELL_CONFIG}
			self.core.bellsOptionsStack.showMainMessage={"show":False,"msgCode":"","type":""}
		
		self.newBellT=LoadBell(self.bellManager,True,"",duplicateBell)
		self.newBellT.start()
		self.newBellT.bellLoaded.connect(self._addNewBellRet)
		self.newBell.finished.connect(self.newBellT.deleteLater)

	#def addNewBell

	@Slot()
	def _addNewBellRet(self):

		self.currentBellConfig=copy.deepcopy(self.bellManager.currentBellConfig)
		self._initializeVars()
		if self.fileFromMenu==None:
			self.core.mainStack.showPopup={"show":False,"msgCode":""}
		else:
			tmpSound=[]
			tmpSound.append("file")
			tmpSound.append(self.fileFromMenu)
			tmpSound.append(True)
			self.updateSoundValues(tmpSound)
		
		self.core.mainStack.currentStack=2
		self.bellCurrentOption=1

	#def _addNewBellRet

	def _initializeVars(self):

		self.bellCron=self.bellManager.bellCron
		self.bellDays=self.bellManager.bellDays
		self.bellValidityActive=self.bellManager.bellValidityActive
		self.bellValidityValue=self.bellManager.bellValidityValue
		self.bellValidityRangeOption=self.bellManager.bellValidityRangeOption
		self.bellValidityDaysInRange=self.bellManager.bellValidityDaysInRange
		self.enableBellValidity=self.bellManager.enableBellValidity
		self.bellName=self.bellManager.bellName
		self.bellImage=self.bellManager.bellImage
		self.bellSound=self.bellManager.bellSound
		self.bellStartIn=self.bellManager.bellStartIn
		self.bellDuration=self.bellManager.bellDuration
		self.showBellFormMessage={"show":False,"msgCode":"","type":""}
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

	@Slot(dict)
	def loadBell(self,bellToLoad):

		self.core.mainStack.showPopup={"show":True,"msgCode":LOAD_BELL_CONFIG}
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
		self.core.mainStack.showPopup={"show":False,"msgCode":""}
		self.core.mainStack.currentStack=2
		self.bellCurrentOption=1

	#def _loadBellRet

	@Slot('QVariantList')
	def duplicateBell(self,bellToDuplicate):

		self.core.mainStack.showPopup={"show":True,"msgCode":DUPLICATE_BELL_CONFIG}
		self.core.bellsOptionsStack.showMainMessage={"show":False,"msgCode":"","type":""}
		self.actionType="duplicate"
		duplicateBell=True
		self.cloneBellT=LoadBell(self.bellManager,False,bellToDuplicate,duplicateBell)
		self.cloneBellT.start()
		self.cloneBellT.bellLoaded.connect(self._duplicateBellRet)
		self.cloneBellT.finished.connect(cloneBellT.deleteLater)

	#def duplicateBell

	@Slot()
	def _duplicateBellRet(self):

		self.currentBellConfig=copy.deepcopy(self.bellManager.currentBellConfig)
		self._initializeVars()
		self.core.mainStack.showPopup={"show":False,"msgCode":""}
		self.core.mainStack.currentStack=2
		self.bellCurrentOption=1

	#def _duplicateBellRet

	@Slot('QVariantList')
	def updateClockValues(self,values):

		if values[0]=="H":
			if values[1]!=self.bellCron["hour"]:
				self.bellCron["hour"]=values[1]
				self.currentBellConfig["hour"]=self.bellCron["hour"]
		else:
			if values[1]!=self.bellCron["minute"]:
				self.bellCron["minute"]=values[1]
				self.currentBellConfig["minute"]=self.bellCron["minute"]

		if self.currentBellConfig!=self.bellManager.currentBellConfig:
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

	@Slot('QVariantList')
	def updateBellValidityValue(self,value):

		if value[0]!=self.bellValidityValue:
			self.bellValidityValue=value[0]
			self.currentBellConfig["validity"]["value"]=self.bellValidityValue
			self.bellValidityRangeOption=value[1]
			self.bellValidityDaysInRange=self.bellManager.getDaysInRange(self.bellValidityValue)

		if value[0]!="":
			if self.currentBellConfig!=self.bellManager.currentBellConfig:
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

		if self.currentBellConfig!=self.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateBellNameValue

	@Slot(str,result=bool)
	def checkMimetypeImage(self,imagePath):

		return self.bellManager.checkMimetypes(imagePath,"image")["result"]

	#def checkMimetypeImage

	@Slot('QVariantList')
	def updateImageValues(self,values):

		tmpImage=[]
		tmpImage.append(values[0])
		tmpImage.append(values[1])

		if values[0]=="stock":
			tmpPath=self.bellManager.imagesConfigData[values[1]]["imageSource"]
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
	
		if self.currentBellConfig!=self.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateImageValues

	@Slot(str,result=bool)
	def checkMimetypeSound(self,soundPath):

		return self.bellManager.checkMimetypes(soundPath,"audio")["result"]

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

		self.core.mainStack.showPopup={"show":True,"msgCode":CHECK_DATA}
		self.core.mainStack.closeGui=False
		self.checkData=CheckData(self.currentBellConfig)
		self.checkData.start()
		self.checkData.finished.connect(self._checkDataRet)

	#def _applyBellChanges

	def _checkDataRet(self):

		if self.checkData.retData["result"]:
			if self.checkData.retDuplicate["result"]:
				self.saveDataChanges()
			else:
				self.core.mainStack.showPopup={"show":False,"msgCode":""}
				self.showBellDuplicateDialog=True
		else:
			self.core.mainStack.showPopup={"show":False,"msgCode":""}
			self.showBellFormMessage={"show":True,"msgCode":self.checkData.retData["code"],"type":ret.get(type)}

	#def _checkDataRet

	@Slot(bool)

	def manageDuplicateDialog(self,response):

		self.showBellDuplicateDialog=False
		if response:
			self.saveDataChanges()

	#def manageDuplicateDialog

	def saveDataChanges(self):

		self.core.mainStack.showPopup={"show":True,"msgCode":SAVE_DATA}
		self.saveData=SaveData(self.currentBellConfig)
		self.saveData.start()
		self.saveData.finished.connect(self._saveDataRet)

	#def saveData

	def _saveDataRet(self):

		if self.saveData.ret[0]:
			self.core.bellsOptionsStack._updateBellsModel()
			self.core.bellsOptionsStack.showMainMessage=[True,self.saveData.ret[1],"Ok"]
		else:
			self.core.bellsOptionsStack.showMainMessage=[True,self.saveData.ret[1],"Error"]	

		self.core.bellsOptionsStack.enableGlobalOptions=self.bellManager.checkGlobalOptionStatus()
		self.core.bellsOptionsStack.enableChangeStatusOptions=self.bellManager.checkChangeStatusBellsOption()
		self.core.bellsOptionsStack.showExportBellsWarning=self.bellManager.checkIfAreBellsWithDirectory()
		self.changesInBell=False
		self.core.mainStack.closeGui=True
		self.core.mainStack.moveToStack=1
		self.core.mainStack.manageGoToStack()
		self.core.mainStack.showPopup={"show":False,"msgCode":""}

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

#class Bridge

from . import Core


