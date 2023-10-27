from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
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

class EnableHolidayControl(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.action=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.bellManager.enableHolidayControl(self.action)

	#def run

#class EnableHolidayControl

class Bridge(QObject):

	def __init__(self):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.bellManager=self.core.bellManager
		self._bellsModel=BellsModel.BellsModel()
		self._showMainMessage=[False,"","Ok"]
		self._showRemoveBellDialog=[False,False]
		self._enableGlobalOptions=False
		self._showExportBellsWarning=False
		self._isHolidayControlEnabled=False
		self.bellSchedulerPlayerLog="/var/log/BELL-SCHEDULER-PLAYER.log"

	#def _init__
	
	def loadConfig(self):

		self._updateBellsModel()
		self.enableGlobalOptions=Bridge.bellManager.checkGlobalOptionStatus()
		self.showExportBellsWarning=Bridge.bellManager.checkIfAreBellsWithDirectory()
		self.isHolidayControlEnabled=Bridge.bellManager.checkHolidayManagerStatus()
	
	#def loadConfig

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

	def _getShowExportBellsWarning(self):

		return self._showExportBellsWarning

	#def _getShowExportBellsWarning

	def _setShowExportBellsWarning(self,showExportBellsWarning):

		if self._showExportBellsWarning!=showExportBellsWarning:
			self._showExportBellsWarning=showExportBellsWarning
			self.on_showExportBellsWarning.emit()

	#def _setShowExportBellsWarning

	def _getIsHolidayControlEnabled(self):

		return self._isHolidayControlEnabled

	#def _getIsHolidayControlEnabled

	def _setIsHolidayControlEnabled(self,isHolidayControlEnabled):

		if self._isHolidayControlEnabled!=isHolidayControlEnabled:
			self._isHolidayControlEnabled=isHolidayControlEnabled
			self.on_isHolidayControlEnabled.emit()

	#def _setIsHolidayControlEnabled

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

	@Slot('QVariantList')
	def changeBellStatus(self,data):

		self.core.mainStack.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.changeAllBells=data[0]
		active=data[1]
		if self.changeAllBells:
			bellToEdit=None
		else:
			bellToEdit=data[2]
		if self.changeAllBells:
			if active:
				self.core.mainStack.closePopUp=[False,ACTIVE_ALL_BELLS]
			else:
				self.core.mainStack.closePopUp=[False,DEACTIVE_ALLS_BELLS]
		else:
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

		self.enableGlobalOptions=Bridge.bellManager.checkGlobalOptionStatus()
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
		self.mainStack.closePopUp=[False,IMPORT_BELLS_CONFIG]
		self.importBackup=ImportBackup(importPath)
		self.importBackup.start()
		self.importBackup.finished.connect(self._importBackupRet)

	#def importBellsConfig

	def _importBackupRet(self):

		if self.importBackup.ret[0]:
			self._updateBellsModel()
			self.core.mainStack.closeGui=True
			self.core.mainStack.closePopUp=[True,""]
			self.showMainMessage=[True,self.importBackup.ret[1],"Ok"]
			self.enableGlobalOptions=Bridge.bellManager.checkGlobalOptionStatus()

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
		self.enableGlobalOptions=Bridge.bellManager.checkGlobalOptionStatus()

	#def _recoveryConfigRet

	@Slot()
	def manageHolidayControl(self):

		if self.isHolidayControlEnabled:
			action="disable"
			msgCode=DISABLE_HOLIDAY_CONTROL 
		else:
			action="enable"
			msgCode=ENABLE_HOLIDAY_CONTROL

		self.core.mainStack.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.core.mainStack.closePopUp=[False,msgCode]
		self.changeHolidayControl=EnableHolidayControl(action)
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

		self.isHolidayControlEnabled=Bridge.bellManager.checkHolidayManagerStatus()

	#def _changeHolidayControlRet
	
	on_showMainMessage=Signal()
	showMainMessage=Property('QVariantList',_getShowMainMessage,_setShowMainMessage, notify=on_showMainMessage)
	
	on_showRemoveBellDialog=Signal()
	showRemoveBellDialog=Property('QVariantList',_getShowRemoveBellDialog,_setShowRemoveBellDialog,notify=on_showRemoveBellDialog)

	on_enableGlobalOptions=Signal()
	enableGlobalOptions=Property(bool,_getEnableGlobalOptions,_setEnableGlobalOptions,notify=on_enableGlobalOptions)

	on_showExportBellsWarning=Signal()
	showExportBellsWarning=Property(bool,_getShowExportBellsWarning,_setShowExportBellsWarning,notify=on_showExportBellsWarning)

	on_isHolidayControlEnabled=Signal()
	isHolidayControlEnabled=Property(bool,_getIsHolidayControlEnabled,_setIsHolidayControlEnabled,notify=on_isHolidayControlEnabled)
	
	bellsModel=Property(QObject,_getBellsModel,constant=True)

#class Bridge

from . import Core


