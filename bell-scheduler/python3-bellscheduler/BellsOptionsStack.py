from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from . import BellsModel

ACTIVE_BELL=5
ACTIVE_ALL_BELLS=6
DEACTIVE_BELL=7
DEACTIVE_ALLS_BELLS=8
REMOVING_BELL=9
REMOVING_ALL_BELLS=10
EXPORT_BELLS_CONFIG=11
IMPORT_BELLS_CONFIG=12
RECOVERY_BELLS_CONFIG=13
DISABLE_HOLIDAY_CONTROL=14
ENABLE_HOLIDAY_CONTROL=15
CONFIGURATING_AUDIO_DEVICE=18
NO_PLAY_LOG_FILE=59
NO_ERROR_LOG_FILE=60

class ChangeBellStatus(QThread):

	bellStatusChanged=Signal(dict)

	def __init__(self,manager,changeAllBells,active,bellToEdit):

		super().__init__(self)
		self.manager=manager
		self.allBells=changeAllBells
		self.active=active
		self.bellToEdit=bellToEdit

	#def __init__

	def run(self,*args):

		ret=self.manager.changeBellStatus(self.allBells,self.active,self.bellToEdit)
		self.bellStatusChanged.emit(ret)

	#def run

#class ChangeBellStatus

class RemoveBell(QThread):

	bellRemoved=Signal(dict)

	def __init__(self,manager,removeAll,bellToRemove):

		super().__init__(self)
		self.manager=manager
		self.allBells=removeAll
		self.bellToRemove=bellToRemove

	#def __init__

	def run(self,*args):

		ret=self.manager.removeBell(self.allBells,self.bellToRemove)
		self.bellRemoved.emit(ret)

	#def run

#class RemoveBell

class GenerateBackup(QThread):

	backupGenerated=Signal(dict)

	def __init__(self,manager,exportPath):

		super().__init__(self)
		self.manager=manager
		self.exportPath=exportPath

	#def __init__

	def run(self,*args):

		ret=self.manager.exportBellsConfig(self.exportPath)
		self.backupGenerated.emit(ret)

	#def run

#class GenerateBackup

class ImportBackup(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.importPath=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=self.bellManager.importBellBackup(self.importPath)

	#def run

#class ImportBackup

class RecoveryConfig(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.recoveryPath=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=self.bellManager.recoveryBellBackup(self.recoveryPath)

	#def run

#class RecoveryConfig

class ChangeHolidayControl(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.action=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=self.bellManager.changeHolidayControl(self.action)

	#def run

#class ChangeHolidayControl

class ChangeAudioDeviceControl(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.audioDeviceConfigurated=args[0]
		self.audioDeviceValue=args[1]

	def run(self):

		time.sleep(0.5)
		self.ret=self.bellManager.changeAudioDeviceControl(self.audioDeviceConfigurated,self.audioDeviceValue)
	
	#def run

#class ChangeAudioDeviceControl		

class Bridge(QObject):

	showMainMessageChanged=Signal()
	showRemoveBellDialogChanged=Signal()
	enableGlobalOptionsChanged=Signal()
	enableChangeStatusOptionsChanged=Signal()
	showExportBellsWarningChanged=Signal()
	isHolidayControlActiveChanged=Signal()
	enableHolidayControlChanged=Signal()
	enableAudioDeviceConfigurationChanged=Signal()
	currentAudioDeviceChanged=Signal()
	isAudioDeviceConfiguratedChanged=Signal()
	filterStatusValueChanged=Signal()

	def __init__(self):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		self.bellManager=self.core.bellManager
		self._bellsModel=BellsModel.BellsModel()
		self._showMainMessage={"show":False,"msgCode":"","type":""}
		self._showRemoveBellDialog={"show":False,"removeAll":False}
		self._enableGlobalOptions=False
		self._enableChangeStatusOptions={"allActivated":False,"allDeactivated":False,"enableFilter":False}
		self._showExportBellsWarning=False
		self._isHolidayControlActive=False
		self._enableHolidayControl=False
		self._audioDevicesModel=self.bellManager.audioDevicesData
		self._enableAudioDeviceConfiguration=False
		self._currentAudioDevice=""
		self._isAudioDeviceConfigurated=False
		self.bellSchedulerPlayerLog="/var/log/BELL-SCHEDULER-PLAYER.log"
		self.n4dBellScedulerManagerLog="/var/log/N4D-BELLSCHEDULER-MANAGER.log"
		self._filterStatusValue="all"

	#def _init__

	@Property(dict,notify=showMainMessageChanged)
	def showMainMessage(self):

		return self._showMainMessage

	#def showMainMessage

	@showMainMessage.setter
	def showMainMessage(self,showMainMessage):

		if self._showMainMessage!=showMainMessage:
			self._showMainMessage=showMainMessage
			self.showMainMessageChanged.emit()

	#def showMainMessage

	@Property(dict,notify=showRemoveBellDialogChanged)
	def showRemoveBellDialog(self):

		return self._showRemoveBellDialog

	#def showRemoveBellDialog

	@showRemoveBellDialog.setter
	def showRemoveBellDialog(self,showRemoveBellDialog):

		if self._showRemoveBellDialog!=showRemoveBellDialog:
			self._showRemoveBellDialog=showRemoveBellDialog
			self.showRemoveBellDialogChanged.emit()

	#def showRemoveBellDialog

	@Property(bool,notify=enableGlobalOptionsChanged)
	def enableGlobalOptions(self):

		return self._enableGlobalOptions

	#def enableGlobalOptions

	@enableGlobalOptions.setter
	def enableGlobalOptions(self,enableGlobalOptions):

		if self._enableGlobalOptions!=enableGlobalOptions:
			self._enableGlobalOptions=enableGlobalOptions
			self.enableGlobalOptionsChanged.emit()

	#def enableGlobalOptions

	@Property(dict,notify=enableChangeStatusOptionsChanged)
	def enableChangeStatusOptions(self):

		return self._enableChangeStatusOptions

	#def enableChangeStatusOptions

	@enableChangeStatusOptions.setter
	def enableChangeStatusOptions(self,enableChangeStatusOptions):

		if self._enableChangeStatusOptions!=enableChangeStatusOptions:
			self._enableChangeStatusOptions=enableChangeStatusOptions
			self.enableChangeStatusOptionsChanged.emit()

	#def enableChangeStatusOptions

	@Property(bool,notify=showExportBellsWarningChanged)
	def showExportBellsWarning(self):

		return self._showExportBellsWarning

	#def showExportBellsWarning

	@showExportBellsWarning.setter
	def showExportBellsWarning(self,showExportBellsWarning):

		if self._showExportBellsWarning!=showExportBellsWarning:
			self._showExportBellsWarning=showExportBellsWarning
			self.showExportBellsWarningChanged.emit()

	#def showExportBellsWarning

	@Property(bool,notify=isHolidayControlActiveChanged)
	def isHolidayControlActive(self):

		return self._isHolidayControlActive

	#def isHolidayControlActive

	@isHolidayControlActive.setter
	def isHolidayControlActive(self,isHolidayControlActive):

		if self._isHolidayControlActive!=isHolidayControlActive:
			self._isHolidayControlActive=isHolidayControlActive
			self.isHolidayControlActiveChanged.emit()

	#def isHolidayControlActive

	@Property(bool,notify=enableHolidayControlChanged)
	def enableHolidayControl(self):

		return self._enableHolidayControl

	#def enableHolidayControl

	@enableHolidayControl.setter
	def enableHolidayControl(self,enableHolidayControl):

		if self._enableHolidayControl!=enableHolidayControl:
			self._enableHolidayControl=enableHolidayControl
			self.enableHolidayControlChanged.emit()

	#def enableHolidayControl

	@Property(bool,notify=enableAudioDeviceConfigurationChanged)
	def enableAudioDeviceConfiguration(self):

		return self._enableAudioDeviceConfiguration

	#def enableAudioDeviceConfiguration

	@enableAudioDeviceConfiguration.setter
	def enableAudioDeviceConfiguration(self,enableAudioDeviceConfiguration):

		if self._enableAudioDeviceConfiguration!=enableAudioDeviceConfiguration:
			self._enableAudioDeviceConfiguration=enableAudioDeviceConfiguration
			self.enableAudioDeviceConfigurationChanged.emit()

	#def _setEnableAudioDeviceConfiguration
	
	@Property(int,notify=currentAudioDeviceChanged)
	def currentAudioDevice(self):

		return self._currentAudioDevice

	#def currentAudioDevice

	@currentAudioDevice.setter
	def currentAudioDevice(self,currentAudioDevice):

		if self._currentAudioDevice!=currentAudioDevice:
			self._currentAudioDevice=currentAudioDevice
			self.currentAudioDeviceChanged.emit()

	#def currentAudioDevice

	@Property(bool,notify=isAudioDeviceConfiguratedChanged)
	def isAudioDeviceConfigurated(self):

		return self._isAudioDeviceConfigurated

	#def isAudioDeviceConfigurated

	@isAudioDeviceConfigurated.setter
	def isAudioDeviceConfigurated(self,isAudioDeviceConfigurated):

		if self._isAudioDeviceConfigurated!=isAudioDeviceConfigurated:
			self._isAudioDeviceConfigurated=isAudioDeviceConfigurated
			self.isAudioDeviceConfiguratedChanged.emit()

	#def isAudioDeviceConfigurated

	@Property(str,notify=filterStatusValueChanged)
	def filterStatusValue(self):

		return self._filterStatusValue

	#def filterStatusValue

	@filterStatusValue.setter
	def filterStatusValue(self,filterStatusValue):

		if self._filterStatusValue!=filterStatusValue:
			self._filterStatusValue=filterStatusValue
			self.filterStatusValueChanged.emit()

	#def _setFilterStatusValue


	@Property(QObject,constant=True)
	def bellsModel(self):

		return self._bellsModel

	#def bellsModel

	@Property('QVariant',constant=True)
	def audioDevicesModel(self):

		return self._audioDevicesModel

	#def audioDevicesModel

	def loadConfig(self):

		self._updateBellsModel()
		self.showExportBellsWarning=self.bellManager.checkIfAreBellsWithDirectory()
		self._manageOptions()
		self._getCurrentAudioConfiguration()	
	
	#def loadConfig

	def _manageOptions(self):

		self.enableGlobalOptions=self.bellManager.checkGlobalOptionStatus()
		self.enableChangeStatusOptions=self.bellManager.checkChangeStatusBellsOption()
		self.isHolidayControlActive=self.bellManager.checkHolidayManagerStatus()
		self.enableHolidayControl=self.bellManager.checkIfAreHolidaysConfigured()

	#def _manageOptions

	def _getCurrentAudioConfiguration(self):

		self.currentAudioDevice=int(self.bellManager.currentAudioDevice)
		self.isAudioDeviceConfigurated=self.bellManager.isAudioDeviceConfigurated
		self.enableAudioDeviceConfiguration=self.bellManager.enableAudioDeviceConfiguration

	#def _getCurrentAudioConfiguration

	def _updateBellsModel(self):

		ret=self._bellsModel.clear()
		bellsEntries=self.bellManager.bellsConfigData
		for item in bellsEntries:
			if item["id"]!="":
				self._bellsModel.appendRow(item["id"],item["cron"],item["mo"],item["tu"],item["we"],item["th"],item["fr"],item["validity"],item["validityActivated"],item["img"],item["name"],item["sound"],item["bellActivated"],item["metaInfo"],item["isSoundError"],item["isImgError"])
	
	#def _updateBellsModel

	def _updateBellsModelInfo(self,param):

		updatedInfo=self.bellManager.bellsConfigData
		if len(updatedInfo)>0:
			for i in range(len(updatedInfo)):
				index=self._bellsModel.index(i)
				self._bellsModel.setData(index,param,updatedInfo[i][param])

	#def _updateBellsModelInfo

	@Slot(str)
	def manageStatusFilter(self,value):

		self.filterStatusValue=value

	#def manageStatusFilter

	@Slot('QVariantList')
	def changeBellStatus(self,data):

		self.core.mainStack.closeGui=False
		self.showMainMessage={"show":False,"msgCode":"","type":""}
		self.changeAllBells=data[0]
		active=data[1]
		if self.changeAllBells:
			bellToEdit=None
			if active:
				self.core.mainStack.showPopUp={"show":True,"msgCode":ACTIVE_ALL_BELLS}
			else:
				self.core.mainStack.showPopUp={"show":True,"msgCode":DEACTIVE_ALLS_BELLS}
		
		else:
			bellToEdit=data[2]
			code=ACTIVE_BELL if active else DEACTIVE_BELL
			self.core.mainStack.showPopUp={"show":False,"msgCode":code}
		
		self.changeStatusT=ChangeBellStatus(self.bellManager,self.changeAllBells,active,bellToEdit)
		self.changeStatusT.start()
		self.changeStatusT.bellStatusChanged.connect(self._changeBellStatusRet)
		self.changeStatus.finished.connect(self.changeStatusT.deleteLater)

	#def changeBellStatus

	@Slot(dict)
	def _changeBellStatusRet(self,ret):

		if ret.get("status"):
			if self.changeAllBells:
				self._updateBellsModel()
			else:
				self._updateBellsModelInfo('bellActivated')
		
		self.showMainMessage={"show":True,"msgCode":ret.get("msgCode"),"tỳpe":ret.get("type")}

		self.enableChangeStatusOptions=self.bellManager.checkChangeStatusBellsOption()
		self.filterStatusValue="all"
		self.core.mainStack.showPopUp={"show":False,"msgCode":""}
		self.core.mainStack.closeGui=True

	#def _changeBellStatusRet

	@Slot()
	def openPlayLogFile(self):

		self.showMainMessage={"show":False,"msgCode":"","type":""}
		if os.path.exists(self.bellSchedulerPlayerLog):
			cmd="xdg-open %s"%self.bellSchedulerPlayerLog
			os.system(cmd)
		else:
			self.showMainMessage={"show":True,"msgCode":NO_PLAY_LOG_FILE,"type":bellManager.KIRIGAMI_MSG_INFO}

	#def openPlayLogFile

	@Slot()
	def openErrorLogFile(self):

		self.showMainMessage={"show":False,"msgCode":"","type":""}
		
		if os.path.exists(self.n4dBellScedulerManagerLog):
			cmd="xdg-open %s"%self.n4dBellScedulerManagerLog
			os.system(cmd)
		else:
			self.showMainMessage={"show":True,"msgCode":NO_ERROR_LOG_FILE,"type":bellManager.KIRIGAMI_MSG_INFO}

	#def openErrorLogFile

	@Slot('QVariantList')
	def removeBell(self,data):

		self.showMainMessage={"show":False,"msgCode":"","type":""}
		self.removeAllBells=data[0]
		self.bellToRemove=None if self.removeAllBells else data[1]
	
		self.showRemoveBellDialog={"show":True,"removeAll":self.removeAllBells}

	#def removeBell

	@Slot(str)
	def manageRemoveBellDialog(self,response):

		self.showRemoveBellDialog={"show":False,"removeAll":False}
		if response=="Accept":
			self._launchRemoveBellProcess()

	#def manageRemoveBellDialog

	def _launchRemoveBellProcess(self):

		self.core.mainStack.closeGui=False
		code=REMOVING_ALL_BELLS if self.removeAllBells else REMOVING_BELL
		self.core.mainStack.showPopUp={"show":True,"msgCode":REMOVING_ALL_BELLS}

		self.removeBellProcessT=RemoveBell(self.bellManager,self.removeAllBells,self.bellToRemove)
		self.removeBellProcessT.start()
		self.removeBellProcessT.bellRemoved.connect(self._removeBellProcessRet)
		self.removeBellProcessT.finished.connect(self.removeBellProcessT.deleteLater)

	#def _launchRemoveBellProcess

	@Slot(dict)
	def _removeBellProcessRet(self,ret):

		if ret.get("status"):
			self._updateBellsModel()
		
		self.showMainMessage={"show":True,"msgCode":ret.get("msgCode"),"type:"ret.get("type")}
	
		self._manageOptions()
		self.filterStatusValue="all"
		self.core.mainStack.showPopUp={"show":False,"msgCode":""}
		self.core.mainStack.closeGui=True

	#def _removeBellProcessRet

	@Slot(str)
	def exportBellsConfig(self,exportPath):

		self.core.mainStack.closeGui=False
		self.showMainMessage={"show":False,"msCode":"","type":""}
		self.core.mainStack.showPopUp={"show":True,"msgCode":EXPORT_BELLS_CONFIG}
		self.generateBackupT=GenerateBackup(self.bellManager,exportPath)
		self.generateBackupT.start()
		self.generateBackupT.backupGenerated.connect(self._exportBellsConfigRet)
		self.generateBackupT.finished.connect(self.generateBackupT.deleteLater)

	#def exportBellsConfig

	@Slot(dict)
	def _exportBellsConfigRet(self,ret):

		self.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
		self.core.mainStack.closeGui=True
		self.core.mainStack.showPopUp={"show":False,"msgCode":""}			

	#def _exportBellsConfigRet

	@Slot(str)
	def importBellsConfig(self,importPath):

		self.core.mainStack.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.core.mainStack.showPopUp={"show":True,"msgCode":IMPORT_BELLS_CONFIG}
		self.importBackup=ImportBackup(importPath)
		self.importBackup.start()
		self.importBackup.finished.connect(self._importBackupRet)

	#def importBellsConfig

	def _importBackupRet(self):

		if self.importBackup.ret[0]:
			self._updateBellsModel()
			self.core.mainStack.closeGui=True
			self.core.mainStack.showPopUp={"show":False,"msgCode":""}
			if self.bellManager.loadError:
				self.showMainMessage=[True,self.bellManager.BELLS_WITH_ERRORS,"Error"]
			else:
				self.showMainMessage=[True,self.importBackup.ret[1],"Ok"]
			self._manageOptions()
			self.filterStatusValue="all"
		else:
			self.core.mainStack.showPopUp={"show":True,"msgCode":RECOVERY_BELLS_CONFIG}
			self.recoveryConfig=RecoveryConfig(self.importBackup.ret[1])
			self.recoveryConfig.start()
			self.recoveryConfig.finished.connect(self._recoveryConfigRet)		

	#def _importBackupRet

	def _recoveryConfigRet(self):

		self._updateBellsModel()
		self.core.mainStack.showPopUp={"show":False,"msgCode":""}
		self.core.mainStack.closeGui=True
		self.showMainMessage=[True,self.recoveryConfig.ret[1],"Error"]
		self._manageOptions()
		self.filterStatusValue="all"

	#def _recoveryConfigRet

	@Slot()
	def manageHolidayControl(self):

		if self.isHolidayControlActive:
			action="disable"
			msgCode=DISABLE_HOLIDAY_CONTROL 
		else:
			action="enable"
			msgCode=ENABLE_HOLIDAY_CONTROL

		self.core.mainStack.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.core.mainStack.showPopUp={"show":True,"msgCode":msgCode}
		self.changeHolidayControl=ChangeHolidayControl(action)
		self.changeHolidayControl.start()
		self.changeHolidayControl.finished.connect(self._changeHolidayControlRet)

	#def _manageHolidayControl

	def _changeHolidayControlRet(self):

		self.core.mainStack.showPopUp={"show":False,"msgCode":""}
		self.core.mainStack.closeGui=True

		if self.changeHolidayControl.ret["status"]:
			self.showMainMessage=[True,self.changeHolidayControl.ret["code"],"Ok"]
		else:
			self.showMainMessage=[True,self.changeHolidayControl.ret["code"],"Error"]

		self.isHolidayControlActive=self.bellManager.checkHolidayManagerStatus()

	#def _changeHolidayControlRet

	@Slot('QVariantList')
	def manageAudioDeviceControl(self,data):

		self.core.mainStack.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		isAudioDeviceConfigurated=data[0]
		currentAudioDevice=data[1]
		self.core.mainStack.showPopUp={"show":True,"msgCode":CONFIGURATING_AUDIO_DEVICE}
		self.changeAudioDeviceControl=ChangeAudioDeviceControl(isAudioDeviceConfigurated,currentAudioDevice)
		self.changeAudioDeviceControl.start()
		self.changeAudioDeviceControl.finished.connect(self._changeAudioDeviceControlRet)

	#def manageAudioDeviceControl

	def _changeAudioDeviceControlRet(self):

		self.core.mainStack.showPopUp={"show":False,"msgCode":""}
		self.core.mainStack.closeGui=True

		if self.changeAudioDeviceControl.ret["status"]:
			self.showMainMessage=[True,self.changeAudioDeviceControl.ret["code"],"Ok"]
		else:
			self.showMainMessage=[True,self.changeAudioDeviceControl.ret["code"],"Error"]

		self._getCurrentAudioConfiguration()


	#def _changeAudioDeviceControlRet
	
	

#class Bridge

from . import Core


