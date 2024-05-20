from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from . import BellsModel
from . import AudioDevicesModel

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

class ChangeBellStatus(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.allBells=args[0]
		self.active=args[1]
		self.bellToEdit=args[2]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.bellManager.changeBellStatus(self.allBells,self.active,self.bellToEdit)

	#def run

#class ChangeBellStatus

class RemoveBell(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.allBells=args[0]
		self.bellToRemove=args[1]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.bellManager.removeBell(self.allBells,self.bellToRemove)

	#def run

#class RemoveBell

class GenerateBackup(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.exportPath=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.bellManager.exportBellsConfig(self.exportPath)

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
		self.ret=Bridge.bellManager.importBellBackup(self.importPath)

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
		self.ret=Bridge.bellManager.recoveryBellBackup(self.recoveryPath)

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
		self.ret=Bridge.bellManager.changeHolidayControl(self.action)

	#def run

#class ChangeHolidayControl

class Bridge(QObject):

	def __init__(self):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.bellManager=self.core.bellManager
		self._bellsModel=BellsModel.BellsModel()
		self._showMainMessage=[False,"","Ok"]
		self._showRemoveBellDialog=[False,False]
		self._enableGlobalOptions=False
		self._enableChangeStatusOptions=[False,False,False]
		self._showExportBellsWarning=False
		self._isHolidayControlActive=False
		self._enableHolidayControl=False
		self._audioDevicesModel=AudioDevicesModel.AudioDevicesModel()
		self._enableAudioDeviceConfiguration=False
		self._currentAudioDevice=""
		self.bellSchedulerPlayerLog="/var/log/BELL-SCHEDULER-PLAYER.log"
		self._filterStatusValue="all"

	#def _init__
	
	def loadConfig(self):

		self._updateBellsModel()
		self.showExportBellsWarning=Bridge.bellManager.checkIfAreBellsWithDirectory()
		self._manageOptions()	
	
	#def loadConfig

	def _manageOptions(self):

		self.enableGlobalOptions=Bridge.bellManager.checkGlobalOptionStatus()
		self.enableChangeStatusOptions=Bridge.bellManager.checkChangeStatusBellsOption()
		self.isHolidayControlActive=Bridge.bellManager.checkHolidayManagerStatus()
		self.enableHolidayControl=Bridge.bellManager.checkIfAreHolidaysConfigured()
		if (Bridge.bellManager.currentAudioDevice)!=""
			self.currentAudioDevice=int(Bridge.bellManager.currentAudioDevice)
		else:
			self.currentAudioDevice=Bridge.bellManager.currentAudioDevice
		self.enableAudioDeviceConfiguration=Bridge.bellManager.enableAudioDeviceConfiguration
		self._updateAudioDevicesModel()


	#def _manageOptions

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

	def _getEnableGlobalOptions(self):

		return self._enableGlobalOptions

	#def _getEnableGlobalOptions

	def _setEnableGlobalOptions(self,enableGlobalOptions):

		if self._enableGlobalOptions!=enableGlobalOptions:
			self._enableGlobalOptions=enableGlobalOptions
			self.on_enableGlobalOptions.emit()

	#def _setEnableGlobalOptions

	def _getEnableChangeStatusOptions(self):

		return self._enableChangeStatusOptions

	#def _getEnableChangeStatusOptions

	def _setEnableChangeStatusOptions(self,enableChangeStatusOptions):

		if self._enableChangeStatusOptions!=enableChangeStatusOptions:
			self._enableChangeStatusOptions=enableChangeStatusOptions
			self.on_enableChangeStatusOptions.emit()

	#def _setEnableChangeStatusOptions

	def _getShowExportBellsWarning(self):

		return self._showExportBellsWarning

	#def _getShowExportBellsWarning

	def _setShowExportBellsWarning(self,showExportBellsWarning):

		if self._showExportBellsWarning!=showExportBellsWarning:
			self._showExportBellsWarning=showExportBellsWarning
			self.on_showExportBellsWarning.emit()

	#def _setShowExportBellsWarning

	def _getIsHolidayControlActive(self):

		return self._isHolidayControlActive

	#def _getIsHolidayControlActive

	def _setIsHolidayControlActive(self,isHolidayControlActive):

		if self._isHolidayControlActive!=isHolidayControlActive:
			self._isHolidayControlActive=isHolidayControlActive
			self.on_isHolidayControlActive.emit()

	#def _setIsHolidayControlActive

	def _getEnableHolidayControl(self):

		return self._enableHolidayControl

	#def _getEnableHolidayControl

	def _setEnableHolidayControl(self,enableHolidayControl):

		if self._enableHolidayControl!=enableHolidayControl:
			self._enableHolidayControl=enableHolidayControl
			self.on_enableHolidayControl.emit()

	#def _setEnableHolidayControl

	def _getFilterStatusValue(self):

		return self._filterStatusValue

	#def _getFilterStatusValue

	def _setFilterStatusValue(self,filterStatusValue):

		if self._filterStatusValue!=filterStatusValue:
			self._filterStatusValue=filterStatusValue
			self.on_filterStatusValue.emit()

	#def _setFilterStatusValue

	def _getAudioDevicesModel(self):

		return self._audioDevicesModel

	#def _getAudioDevicesModel

	def _getEnableAudioDeviceConfiguration(self):

		return self._enableAudioDeviceConfiguration

	#def _getEnableAudioDeviceConfiguration

	def _setEnableAudioDeviceConfiguration(self,enableAudioDeviceConfiguration):

		if self._enableAudioDeviceConfiguration!=enableAudioDeviceConfiguration:
			self._enableAudioDeviceConfiguration=enableAudioDeviceConfiguration
			self.on_enableAudioDeviceConfiguration.emit()

	#def _setEnableAudioDeviceConfiguration

	def _getCurrentAudioDevice(self):

		return self._currentAudioDevice

	#def _getCurrentAudioDevice

	def _setCurrentAudioDevice(self,currentAudioDevice):

		if self._currentAudioDevice!=currentAudioDevice:
			self._currentAudioDevice=currentAudioDevice
			self.on_currentAudioDevice.emit()

	#def _setCurrentAudioDevice

	def _updateBellsModel(self):

		ret=self._bellsModel.clear()
		bellsEntries=Bridge.bellManager.bellsConfigData
		for item in bellsEntries:
			if item["id"]!="":
				self._bellsModel.appendRow(item["id"],item["cron"],item["mo"],item["tu"],item["we"],item["th"],item["fr"],item["validity"],item["validityActivated"],item["img"],item["name"],item["sound"],item["bellActivated"],item["metaInfo"],item["isSoundError"],item["isImgError"])
	
	#def _updateBellsModel

	def _updateBellsModelInfo(self,param):

		updatedInfo=Bridge.bellManager.bellsConfigData
		if len(updatedInfo)>0:
			for i in range(len(updatedInfo)):
				index=self._bellsModel.index(i)
				self._bellsModel.setData(index,param,updatedInfo[i][param])

	#def _updateBellsModelInfo

	def _updateAudioDevicesModel(self):

		ret=self._audioDevicesModel.clear()
		audioEntries=Bridge.bellManager.audioDevicesData
		for item in audioEntries:
			if item["idAudioDevice"]!="":
				self._audioDevicesModel.appendRow(item["idAudioDevice"],item["nameAudioDevice"])

	#def _updateAudioDevicesModel

	@Slot(str)
	def manageStatusFilter(self,value):

		self.filterStatusValue=value

	#def manageStatusFilter

	@Slot('QVariantList')
	def changeBellStatus(self,data):

		self.core.mainStack.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.changeAllBells=data[0]
		active=data[1]
		if self.changeAllBells:
			bellToEdit=None
			if active:
				self.core.mainStack.closePopUp=[False,ACTIVE_ALL_BELLS]
			else:
				self.core.mainStack.closePopUp=[False,DEACTIVE_ALLS_BELLS]
		
		else:
			bellToEdit=data[2]
			if active:
				self.core.mainStack.closePopUp=[False,ACTIVE_BELL]
			else:
				self.core.mainStack.closePopUp=[False,DEACTIVE_BELL]
		
		self.changeStatus=ChangeBellStatus(self.changeAllBells,active,bellToEdit)
		self.changeStatus.start()
		self.changeStatus.finished.connect(self._changeBellStatusRet)

	#def changeBellStatus

	def _changeBellStatusRet(self):

		if self.changeStatus.ret[0]:
			if self.changeAllBells:
				self._updateBellsModel()
			else:
				self._updateBellsModelInfo('bellActivated')
			self.showMainMessage=[True,self.changeStatus.ret[1],"Ok"]
		else:
			self.showMainMessage=[True,self.changeStatus.ret[1],"Error"]

		self.enableChangeStatusOptions=Bridge.bellManager.checkChangeStatusBellsOption()
		self.filterStatusValue="all"
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

	#def _changeBellStatusRet

	@Slot()
	def openLogFile(self):

		if os.path.exists(self.bellSchedulerPlayerLog):
			cmd="xdg-open %s"%self.bellSchedulerPlayerLog
			os.system(cmd)

	#def openLogFile

	@Slot('QVariantList')
	def removeBell(self,data):

		self.showMainMessage=[False,"","Ok"]
		self.removeAllBells=data[0]
		if self.removeAllBells:
			self.bellToRemove=None
		else:
			self.bellToRemove=data[1]

		self.showRemoveBellDialog=[True,self.removeAllBells]

	#def removeBell

	@Slot(str)
	def manageRemoveBellDialog(self,response):

		self.showRemoveBellDialog=[False,False]
		if response=="Accept":
			self._launchRemoveBellProcess()

	#def manageRemoveBellDialog

	def _launchRemoveBellProcess(self):

		self.core.mainStack.closeGui=False
		if self.removeAllBells:
			self.core.mainStack.closePopUp=[False,REMOVING_ALL_BELLS]
		else:
			self.core.mainStack.closePopUp=[False,REMOVING_BELL]

		self.removeBellProcess=RemoveBell(self.removeAllBells,self.bellToRemove)
		self.removeBellProcess.start()
		self.removeBellProcess.finished.connect(self._removeBellProcessRet)

	#def _launchRemoveBellProcess

	def _removeBellProcessRet(self):

		if self.removeBellProcess.ret[0]:
			self._updateBellsModel()
			self.showMainMessage=[True,self.removeBellProcess.ret[1],"Ok"]
		else:
			self.showMainMessage=[False,self.removeBellProcess.ret[1],"Error"]

		self._manageOptions()
		self.filterStatusValue="all"
		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

	#def _removeBellProcessRet

	@Slot(str)
	def exportBellsConfig(self,exportPath):

		self.core.mainStack.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.core.mainStack.closePopUp=[False,EXPORT_BELLS_CONFIG]
		self.generateBackup=GenerateBackup(exportPath)
		self.generateBackup.start()
		self.generateBackup.finished.connect(self._exportBellsConfigRet)

	#def exportBellsConfig

	def _exportBellsConfigRet(self):

		if self.generateBackup.ret["status"]:
			self.showMainMessage=[True,self.generateBackup.ret["code"],"Ok"]
		else:
			self.showMainMessage=[True,self.generateBackup.ret["code"],"Error"]
		
		self.core.mainStack.closeGui=True
		self.core.mainStack.closePopUp=[True,""]			

	#def _exportBellsConfigRet

	@Slot(str)
	def importBellsConfig(self,importPath):

		self.core.mainStack.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.core.mainStack.closePopUp=[False,IMPORT_BELLS_CONFIG]
		self.importBackup=ImportBackup(importPath)
		self.importBackup.start()
		self.importBackup.finished.connect(self._importBackupRet)

	#def importBellsConfig

	def _importBackupRet(self):

		if self.importBackup.ret[0]:
			self._updateBellsModel()
			self.core.mainStack.closeGui=True
			self.core.mainStack.closePopUp=[True,""]
			if Bridge.bellManager.loadError:
				self.showMainMessage=[True,Bridge.bellManager.BELLS_WITH_ERRORS,"Error"]
			else:
				self.showMainMessage=[True,self.importBackup.ret[1],"Ok"]
			self._manageOptions()
			self.filterStatusValue="all"
		else:
			self.core.mainStack.closePopUp=[False,RECOVERY_BELLS_CONFIG]
			self.recoveryConfig=RecoveryConfig(self.importBackup.ret[1])
			self.recoveryConfig.start()
			self.recoveryConfig.finished.connect(self._recoveryConfigRet)		

	#def _importBackupRet

	def _recoveryConfigRet(self):

		self._updateBellsModel()
		self.core.mainStack.closePopUp=[True,""]
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
		self.core.mainStack.closePopUp=[False,msgCode]
		self.changeHolidayControl=ChangeHolidayControl(action)
		self.changeHolidayControl.start()
		self.changeHolidayControl.finished.connect(self._changeHolidayControlRet)

	#def _manageHolidayControl

	def _changeHolidayControlRet(self):

		self.core.mainStack.closePopUp=[True,""]
		self.core.mainStack.closeGui=True

		if self.changeHolidayControl.ret["status"]:
			self.showMainMessage=[True,self.changeHolidayControl.ret["code"],"Ok"]
		else:
			self.showMainMessage=[True,self.changeHolidayControl.ret["code"],"Error"]

		self.isHolidayControlActive=Bridge.bellManager.checkHolidayManagerStatus()

	#def _changeHolidayControlRet
	
	on_showMainMessage=Signal()
	showMainMessage=Property('QVariantList',_getShowMainMessage,_setShowMainMessage, notify=on_showMainMessage)
	
	on_showRemoveBellDialog=Signal()
	showRemoveBellDialog=Property('QVariantList',_getShowRemoveBellDialog,_setShowRemoveBellDialog,notify=on_showRemoveBellDialog)

	on_enableGlobalOptions=Signal()
	enableGlobalOptions=Property(bool,_getEnableGlobalOptions,_setEnableGlobalOptions,notify=on_enableGlobalOptions)

	on_enableChangeStatusOptions=Signal()
	enableChangeStatusOptions=Property('QVariantList',_getEnableChangeStatusOptions,_setEnableChangeStatusOptions,notify=on_enableChangeStatusOptions)

	on_showExportBellsWarning=Signal()
	showExportBellsWarning=Property(bool,_getShowExportBellsWarning,_setShowExportBellsWarning,notify=on_showExportBellsWarning)

	on_isHolidayControlActive=Signal()
	isHolidayControlActive=Property(bool,_getIsHolidayControlActive,_setIsHolidayControlActive,notify=on_isHolidayControlActive)

	on_enableHolidayControl=Signal()
	enableHolidayControl=Property(bool,_getEnableHolidayControl,_setEnableHolidayControl,notify=on_enableHolidayControl)

	on_enableAudioDeviceConfiguration=Signal()
	enableAudioDeviceConfiguration=Property(bool,_getEnableAudioDeviceConfiguration,_setEnableAudioDeviceConfiguration,notify=on_enableAudioDeviceConfiguration)

	on_currentAudioDevice=Signal()
	currentAudioDevice=Property(int,_getCurrentAudioDevice,_setCurrentAudioDevice,notify=on_currentAudioDevice)
	
	on_filterStatusValue=Signal()
	filterStatusValue=Property(str,_getFilterStatusValue,_setFilterStatusValue,notify=on_filterStatusValue)

	bellsModel=Property(QObject,_getBellsModel,constant=True)
	audioDevicesModel=Property(QObject,_getAudioDevicesModel,constant=True)

#class Bridge

from . import Core


