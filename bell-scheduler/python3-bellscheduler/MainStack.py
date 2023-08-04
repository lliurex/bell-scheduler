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
LOADING_HOLIDADY_LIST=116

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
		self.ret=Bridge.bellMan.changeBellStatus(self.allBells,self.active,self.bellToEdit)

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
		self.ret=Bridge.bellMan.removeBell(self.allBells,self.bellToRemove)

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
		self.ret=Bridge.bellMan.exportBellsConfig(self.exportPath)

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
		self.ret=Bridge.bellMan.importBellBackup(self.importPath)

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
		self.ret=Bridge.bellMan.recoveryBellBackup(self.recoveryPath)

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
		self.ret=Bridge.bellMan.enableHolidayControl(self.action)

	#def run

#class EnableHolidayControl

class LoadHoliday(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.core=Core.Core.get_core()

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.core.holidayStack.initBridge()

	#def run

#class LoadHoliday

class Bridge(QObject):

	def __init__(self,ticket=None):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.bellMan=self.core.bellmanager
		self._bellsModel=BellsModel.BellsModel()
		self._currentStack=0
		self._mainCurrentOption=0
		self._closePopUp=[True,""]
		self.moveToStack=""
		self._closeGui=True
		self._showMainMessage=[False,"","Ok"]
		self._showLoadErrorMessage=[False,""]
		self._showRemoveBellDialog=[False,False]
		self._enableGlobalOptions=False
		self._showExportBellsWarning=False
		self._isHolidayControlEnabled=False
		Bridge.bellMan.createN4dClient(sys.argv[1])

	#def _init__

	def initBridge(self):

		self.currentStack=0
		self.closeGui=False
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)
	
	#def initBridge
	
	def _loadConfig(self):

		self.closeGui=True
		if self.gatherInfo.syncWithCron['status']:
			if self.gatherInfo.readConf['status']:
				self._updateBellsModel()
				self.core.bellStack._updateImagesModel()
				self.enableGlobalOptions=Bridge.bellMan.checkGlobalOptionStatus()
				self.showExportBellsWarning=Bridge.bellMan.checkIfAreBellsWithDirectory()
				self.isHolidayControlEnabled=Bridge.bellMan.checkHolidayManagerStatus()
				self._systemLocale=Bridge.bellMan.systemLocale
				if Bridge.bellMan.loadError:
					self.showMainMessage=[True,Bridge.bellMan.BELLS_WITH_ERRORS,"Error"]
				self.currentStack=1
			else:
				self.showLoadErrorMessage=[True,self.gatherInfo.readConf['code']]
		else:
			self.showLoadErrorMessage=[True,self.gatherInfo.syncWithCron['code']]
	
	#def _loadConfig

	def _getSystemLocale(self):

		return self._systemLocale

	#def _getSystemLocale

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

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp

	def _setClosePopUp(self,closePopUp):

		if self._closePopUp!=closePopUp:
			self._closePopUp=closePopUp
			self.on_closePopUp.emit()

	#def _setClosePopUp

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

		updatedInfo=Bridge.bellMan.bellsConfigData
		if len(updatedInfo)>0:
			for i in range(len(updatedInfo)):
				index=self._bellsModel.index(i)
				self._bellsModel.setData(index,param,updatedInfo[i][param])

	#def _updateBellsModelInfo

	@Slot(int)
	def moveToMainOptions(self,stack):

		if stack==0:
			self.mainCurrentOption=stack
		else:
			self._loadHolidayStack()

	#def moveToMainOptions

	def _loadHolidayStack(self):

		self.closeGui=False
		self.closePopUp=[False,LOADING_HOLIDADY_LIST]
		self.loadHolidayConfig=LoadHoliday()
		self.loadHolidayConfig.start()
		self.loadHolidayConfig.finished.connect(self._loadHolidayConfigRet)

	#def _loadHolidayStack

	def _loadHolidayConfigRet(self):

		self.closeGui=True
		self.closePopUp=[True,""]
		self.mainCurrentOption=1

	#def _loadHolidayConfigRet

	@Slot('QVariantList')
	def changeBellStatus(self,data):

		self.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.changeAllBells=data[0]
		active=data[1]
		if self.changeAllBells:
			bellToEdit=None
		else:
			bellToEdit=data[2]
		if self.changeAllBells:
			if active:
				self.closePopUp=[False,ACTIVE_ALL_BELLS]
			else:
				self.closePopUp=[False,DEACTIVE_ALLS_BELLS]
		else:
			if active:
				self.closePopUp=[False,ACTIVE_BELL]
			else:
				self.closePopUp=[False,DEACTIVE_BELL]

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

		self.closePopUp=[True,""]
		self.closeGui=True

	#def _changeBellStatusRet

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

		self.closeGui=False
		if self.removeAllBells:
			self.closePopUp=[False,REMOVING_ALL_BELLS]
		else:
			self.closePopUp=[False,REMOVING_BELL]

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

		self.enableGlobalOptions=Bridge.bellMan.checkGlobalOptionStatus()
		self.closePopUp=[True,""]
		self.closeGui=True

	#def _removeBellProcessRet

	@Slot(str)
	def exportBellsConfig(self,exportPath):

		self.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.closePopUp=[False,EXPORT_BELLS_CONFIG]
		self.generateBackup=GenerateBackup(exportPath)
		self.generateBackup.start()
		self.generateBackup.finished.connect(self._exportBellsConfigRet)

	#def exportBellsConfig

	def _exportBellsConfigRet(self):

		if self.generateBackup.ret["status"]:
			self.showMainMessage=[True,self.generateBackup.ret["code"],"Ok"]
		else:
			self.showMainMessage=[True,self.generateBackup.ret["code"],"Error"]
		
		self.closeGui=True
		self.closePopUp=[True,""]			

	#def _exportBellsConfigRet

	@Slot(str)
	def importBellsConfig(self,importPath):

		self.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.closePopUp=[False,IMPORT_BELLS_CONFIG]
		self.importBackup=ImportBackup(importPath)
		self.importBackup.start()
		self.importBackup.finished.connect(self._importBackupRet)

	#def importBellsConfig

	def _importBackupRet(self):

		if self.importBackup.ret[0]:
			self._updateBellsModel()
			self.closeGui=True
			self.closePopUp=[True,""]
			self.showMainMessage=[True,self.importBackup.ret[1],"Ok"]

		else:
			self.closePopUp=[False,RECOVERY_BELLS_CONFIG]
			self.recoveryConfig=RecoveryConfig(self.importBackup.ret[1])
			self.recoveryConfig.start()
			self.recoveryConfig.finished.connect(self._recoveryConfigRet)		

	#def _importBackupRet

	def _recoveryConfigRet(self):

		self._updateBellsModel()
		self.closePopUp=[True,""]
		self.closeGui=True
		self.showMainMessage=[True,self.recoveryConfig.ret[1],"Error"]

	#def _recoveryConfigRet

	@Slot()
	def manageHolidayControl(self):

		if self.isHolidayControlEnabled:
			action="disable"
			msgCode=DISABLE_HOLIDAY_CONTROL 
		else:
			action="enable"
			msgCode=ENABLE_HOLIDAY_CONTROL

		self.closeGui=False
		self.showMainMessage=[False,"","Ok"]
		self.closePopUp=[False,msgCode]
		self.changeHolidayControl=EnableHolidayControl(action)
		self.changeHolidayControl.start()
		self.changeHolidayControl.finished.connect(self._changeHolidayControlRet)

	#def _manageHolidayControl

	def _changeHolidayControlRet(self):

		self.closePopUp=[True,""]
		self.closeGui=True

		if self.changeHolidayControl.ret["status"]:
			self.showMainMessage=[True,self.changeHolidayControl.ret["code"],"Ok"]
		else:
			self.showMainMessage=[True,self.changeHolidayControl.ret["code"],"Error"]

		self.isHolidayControlEnabled=Bridge.bellMan.checkHolidayManagerStatus()

	def manageGoToStack(self):

		if self.moveToStack!="":
			self.currentStack=self.moveToStack
			self.mainCurrentOption=0
			self.moveToStack=""

	#def _manageGoToStack

	@Slot()
	def openHelp(self):
		
		if 'valencia' in Bridge.bellMan.systemLocale:
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

		if self.core.bellStack.changesInBell:
			self.closeGui=False
			self.showChangesInBellDialog=True

	#def closeBellScheduler
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_mainCurrentOption=Signal()
	mainCurrentOption=Property(int,_getMainCurrentOption,_setMainCurrentOption, notify=on_mainCurrentOption)

	on_showMainMessage=Signal()
	showMainMessage=Property('QVariantList',_getShowMainMessage,_setShowMainMessage, notify=on_showMainMessage)
	
	on_showLoadErrorMessage=Signal()
	showLoadErrorMessage=Property('QVariantList',_getShowLoadErrorMessage,_setShowLoadErrorMessage, notify=on_showLoadErrorMessage)

	on_closePopUp=Signal()
	closePopUp=Property('QVariantList',_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_showRemoveBellDialog=Signal()
	showRemoveBellDialog=Property('QVariantList',_getShowRemoveBellDialog,_setShowRemoveBellDialog,notify=on_showRemoveBellDialog)

	on_enableGlobalOptions=Signal()
	enableGlobalOptions=Property(bool,_getEnableGlobalOptions,_setEnableGlobalOptions,notify=on_enableGlobalOptions)

	on_showExportBellsWarning=Signal()
	showExportBellsWarning=Property(bool,_getShowExportBellsWarning,_setShowExportBellsWarning,notify=on_showExportBellsWarning)

	on_isHolidayControlEnabled=Signal()
	isHolidayControlEnabled=Property(bool,_getIsHolidayControlEnabled,_setIsHolidayControlEnabled,notify=on_isHolidayControlEnabled)
	
	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)

	systemLocale=Property(str,_getSystemLocale,constant=True)
	bellsModel=Property(QObject,_getBellsModel,constant=True)

#class Bridge

from . import Core


