from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
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

	def __init__(self,*args):

		QThread.__init__(self)
		self.newBell=args[0]
		self.bellInfo=args[1]
		self.duplicateBell=args[2]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		ret=Bridge.bellManager.initValues()
		if not self.newBell:
			ret=Bridge.bellManager.loadBellConfig(self.bellInfo,self.duplicateBell)

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
		self.ret=Bridge.bellManager.checkData(self.dataToCheck)

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
		self.ret=Bridge.bellManager.saveData(self.dataToSave)

	#def run

#class SaveData

class Bridge(QObject):

	
	def __init__(self):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.bellManager=self.core.bellManager
		self._imagesModel=ImagesModel.ImagesModel()
		self._bellCron=Bridge.bellManager.bellCron
		self._bellDays=Bridge.bellManager.bellDays
		self._bellValidityActive=Bridge.bellManager.bellValidityActive
		self._bellValidityValue=Bridge.bellManager.bellValidityValue
		self._bellValidityRangeOption=True
		self._bellValidityDaysInRange=[]
		self._enableBellValidity=False
		self._bellName=Bridge.bellManager.bellName
		self._bellImage=Bridge.bellManager.bellImage
		self._bellSound=Bridge.bellManager.bellSound
		self._bellStartIn=Bridge.bellManager.bellStartIn
		self._bellDuration=Bridge.bellManager.bellDuration
		self._bellCurrentOption=0
		self._showBellFormMessage=[False,"","Ok"]
		self._showChangesInBellDialog=False
		self._changesInBell=False
		self._actionType="add"

	#def _init__

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

	def _getBellCurrentOption(self):

		return self._bellCurrentOption

	#def _getBellCurrentOption	

	def _setBellCurrentOption(self,bellCurrentOption):
		
		if self._bellCurrentOption!=bellCurrentOption:
			self._bellCurrentOption=bellCurrentOption
			self.on_bellCurrentOption.emit()

	#def _setBellCurrentOption

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

	def _getShowBellFormMessage(self):

		return self._showBellFormMessage

	#def _getShowBellFormMessage

	def _setShowBellFormMessage(self,showBellFormMessage):

		if self._showBellFormMessage!=showBellFormMessage:
			self._showBellFormMessage=showBellFormMessage
			self.on_showBellFormMessage.emit()

	#def _setShowBellFormMessage

	def _getActionType(self):

		return self._actionType

	#def _getActionType

	def _setActionType(self,actionType):

		if self._actionType!=actionType:
			self._actionType=actionType
			self.on_actionType.emit()

	#def _setActionType

	def _getImagesModel(self):

		return self._imagesModel

	#def _getImagesModel	

	def updateImagesModel(self):

		ret=self._imagesModel.clear()
		imagesEntries=Bridge.bellManager.imagesConfigData
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
			self.core.mainStack.closePopUp=[False,NEW_BELL_CONFIG]
			self.core.bellsOptionsStack.showMainMessage=[False,"","Ok"]
		self.newBell=LoadBell(True,"",duplicateBell)
		self.newBell.start()
		self.newBell.finished.connect(self._addNewBellRet)

	#def addNewBell

	def _addNewBellRet(self):

		self.currentBellConfig=copy.deepcopy(Bridge.bellManager.currentBellConfig)
		self._initializeVars()
		if self.fileFromMenu==None:
			self.core.mainStack.closePopUp=[True,""]
		else:
			tmpSound=[]
			tmpSound.append("file")
			tmpSound.append(sys.argv[2])
			tmpSound.append(True)
			self.updateSoundValues(tmpSound)
		self.core.mainStack.currentStack=2
		self.bellCurrentOption=1

	#def _addNewBellRet

	def _initializeVars(self):

		self.bellCron=Bridge.bellManager.bellCron
		self.bellDays=Bridge.bellManager.bellDays
		self.bellValidityActive=Bridge.bellManager.bellValidityActive
		self.bellValidityValue=Bridge.bellManager.bellValidityValue
		self.bellValidityRangeOption=Bridge.bellManager.bellValidityRangeOption
		self.bellValidityDaysInRange=Bridge.bellManager.bellValidityDaysInRange
		self.enableBellValidity=Bridge.bellManager.enableBellValidity
		self.bellName=Bridge.bellManager.bellName
		self.bellImage=Bridge.bellManager.bellImage
		self.bellSound=Bridge.bellManager.bellSound
		self.bellStartIn=Bridge.bellManager.bellStartIn
		self.bellDuration=Bridge.bellManager.bellDuration
		self.showBellFormMessage=[False,"","Ok"]
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

	@Slot('QVariantList')
	def loadBell(self,bellToLoad):

		self.core.mainStack.closePopUp=[False,LOAD_BELL_CONFIG]
		self.core.bellsOptionsStack.showMainMessage=[False,"","Ok"]
		duplicateBell=False
		self.actionType="edit"
		self.editBell=LoadBell(False,bellToLoad,duplicateBell)
		self.editBell.start()
		self.editBell.finished.connect(self._loadBellRet)

	#def loadBell

	def _loadBellRet(self):

		self.currentBellConfig=copy.deepcopy(Bridge.bellManager.currentBellConfig)
		self._initializeVars()
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.currentStack=2
		self.bellCurrentOption=1

	#def _loadBellRet

	@Slot('QVariantList')
	def duplicateBell(self,bellToDuplicate):

		self.core.mainStack.closePopUp=[False,DUPLICATE_BELL_CONFIG]
		self.core.bellsOptionsStack.showMainMessage=[False,"","Ok"]
		self.actionType="duplicate"
		duplicateBell=True
		self.cloneBell=LoadBell(False,bellToDuplicate,duplicateBell)
		self.cloneBell.start()
		self.cloneBell.finished.connect(self._duplicateBellRet)

	#def duplicateBell

	def _duplicateBellRet(self):

		self.currentBellConfig=copy.deepcopy(Bridge.bellManager.currentBellConfig)
		self._initializeVars()
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.currentStack=2
		self.bellCurrentOption=1

	#def _duplicateBellRet

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

		if self.currentBellConfig!=Bridge.bellManager.currentBellConfig:
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

		self.enableBellValidity=Bridge.bellManager.areDaysChecked(self.currentBellConfig["weekdays"])
		
		if self.currentBellConfig!=Bridge.bellManager.currentBellConfig:
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

		if self.currentBellConfig!=Bridge.bellManager.currentBellConfig:
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
			self.bellValidityDaysInRange=Bridge.bellManager.getDaysInRange(self.bellValidityValue)

		if value[0]!="":
			if self.currentBellConfig!=Bridge.bellManager.currentBellConfig:
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

		if self.currentBellConfig!=Bridge.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateBellNameValue

	@Slot(str,result=bool)
	def checkMimetypeImage(self,imagePath):

		return Bridge.bellManager.checkMimetypes(imagePath,"image")["result"]

	#def checkMimetypeImage

	@Slot('QVariantList')
	def updateImageValues(self,values):

		tmpImage=[]
		tmpImage.append(values[0])
		tmpImage.append(values[1])

		if values[0]=="stock":
			tmpPath=Bridge.bellManager.imagesConfigData[values[1]]["imageSource"]
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
	
		if self.currentBellConfig!=Bridge.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateImageValues

	@Slot(str,result=bool)
	def checkMimetypeSound(self,soundPath):

		return Bridge.bellManager.checkMimetypes(soundPath,"audio")["result"]

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

		if self.currentBellConfig!=Bridge.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateSoundValues

	@Slot(int)
	def updateStartInValue(self,value):

		if value!=self.bellStartIn:
			self.bellStartIn=value
			self.currentBellConfig["play"]["start"]=self.bellStartIn

		if self.currentBellConfig!=Bridge.bellManager.currentBellConfig:
			self.changesInBell=True
		else:
			self.changesInBell=False

	#def updateStartInValue

	@Slot(int)
	def updateDurationValue(self,value):

		if value!=self.bellDuration:
			self.bellDuration=value
			self.currentBellConfig["play"]["duration"]=self.bellDuration

		if self.currentBellConfig!=Bridge.bellManager.currentBellConfig:
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

		self.core.mainStack.closePopUp=[False,CHECK_DATA]
		self.core.mainStack.closeGui=False
		self.checkData=CheckData(self.currentBellConfig)
		self.checkData.start()
		self.checkData.finished.connect(self._checkDataRet)

	#def _applyBellChanges

	def _checkDataRet(self):

		if self.checkData.ret["result"]:
			self.core.mainStack.closePopUp=[False,SAVE_DATA]
			self.saveData=SaveData(self.currentBellConfig)
			self.saveData.start()
			self.saveData.finished.connect(self._saveDataRet)

		else:
			self.core.mainStack.closePopUp=[True,""]
			self.showBellFormMessage=[True,self.checkData.ret["code"],"Error"]

	#def _checkDataRet

	def _saveDataRet(self):

		if self.saveData.ret[0]:
			self.core.bellsOptionsStack._updateBellsModel()
			self.core.bellsOptionsStack.showMainMessage=[True,self.saveData.ret[1],"Ok"]
		else:
			self.core.bellsOptionsStack.showMainMessage=[True,self.saveData.ret[1],"Error"]	

		self.core.bellsOptionsStack.enableGlobalOptions=Bridge.bellManager.checkGlobalOptionStatus()
		self.core.bellsOptionsStack.enableChangeStatusOptions=Bridge.bellManager.checkChangeStatusBellsOption()
		self.core.bellsOptionsStack.showExportBellsWarning=Bridge.bellManager.checkIfAreBellsWithDirectory()
		self.changesInBell=False
		self.core.mainStack.closeGui=True
		self.core.mainStack.moveToStack=1
		self.core.mainStack.manageGoToStack()
		self.core.mainStack.closePopUp=[True,""]

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

	on_showBellFormMessage=Signal()
	showBellFormMessage=Property('QVariantList',_getShowBellFormMessage,_setShowBellFormMessage, notify=on_showBellFormMessage)

	on_bellCurrentOption=Signal()
	bellCurrentOption=Property(int,_getBellCurrentOption,_setBellCurrentOption, notify=on_bellCurrentOption)

	on_showChangesInBellDialog=Signal()
	showChangesInBellDialog=Property(bool,_getShowChangesInBellDialog,_setShowChangesInBellDialog,notify=on_showChangesInBellDialog)

	on_changesInBell=Signal()
	changesInBell=Property(bool,_getChangesInBell,_setChangesInBell,notify=on_changesInBell)

	on_actionType=Signal()
	actionType=Property(str,_getActionType,_setActionType,notify=on_actionType)

	imagesModel=Property(QObject,_getImagesModel,constant=True)

#class Bridge

from . import Core


