from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,Qt,QModelIndex
from PySide2.QtGui import QDesktopServices
import os 
import sys
import time

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

CREATE_BELL_FROM_MENU_ERROR=-38
LOADING_HOLIDAY_LIST=16

class GatherInfo(QThread):

	infoGathered=Signal(dict)

	def __init__(self,manager):
		
		super().__init__()
		self.manager=manager

	#def _init__

	def run(self,*args):
		
		time.sleep(0.2)
		ret=self.manager.syncWithCron()
		if ret.get("status"):
			ret=self.manager.readConf()

		self.infoGathered.emit(ret)

	#def run

#class GatherInfo

class LoadHoliday(QThread):

	holidayLoaded=Signal()

	def __init__(self,*args):

		super().__init__()
		self.core=Core.Core.get_core()

	#def __init__

	def run(self,*args):

		time.sleep(0.2)
		self.core.holidayStack.initBridge()

		self.holidayLoaded.emit()

	#def run

#class LoadHoliday

class Bridge(QObject):

	currentStackChanged=Signal()
	mainCurrentOptionChanged=Signal()
	showLoadErrorMessageChanged=Signal()
	showPopUpChanged=Signal()
	closeGuiChanged=Signal()

	def __init__(self):

		super().__init__()
		self.core=Core.Core.get_core()
		self.bellManager=self.core.bellManager
		self._currentStack=0
		self._mainCurrentOption=0
		self._showPopUp={"show":False,"msgCode":""}
		self.moveToStack=""
		self._closeGui=True
		self._showLoadErrorMessage={"show":False,"msgCode":""}
		self.bellManager.createN4dClient(sys.argv[1])

	#def _init_

	@Property(int,notify=currentStackChanged)
	def currentStack(self):

		return self._currentStack

	#def currentStack	

	@currentStack.setter
	def currentStack(self,currentStack):

		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.currentStackChanged.emit()

	#def currentStack

	@Property(int,notify=mainCurrentOptionChanged)
	def mainCurrentOption(self):

		return self._mainCurrentOption

	#def mainCurrentOption	

	@mainCurrentOption.setter
	def mainCurrentOption(self,mainCurrentOption):
		
		if self._mainCurrentOption!=mainCurrentOption:
			self._mainCurrentOption=mainCurrentOption
			self.mainCurrentOptionChanged.emit()

	#def mainCurrentOption

	@Property('QVariant',notify=showLoadErrorMessageChanged)
	def showLoadErrorMessage(self):

		return self._showLoadErrorMessage

	#def _showLoadErrorMessage

	@showLoadErrorMessage.setter
	def showLoadErrorMessage(self,showLoadErrorMessage):

		if self._showLoadErrorMessage!=showLoadErrorMessage:
			self._showLoadErrorMessage=showLoadErrorMessage
			self.showLoadErrorMessageChanged.emit()

	#def showLoadErrorMessage

	@Property('QVariant',notify=showPopUpChanged)
	def showPopUp(self):

		return self._showPopUp

	#def showPopUp

	@showPopUp.setter
	def showPopUp(self,showPopUp):

		if self._showPopUp!=showPopUp:
			self._showPopUp=showPopUp
			self.showPopUpChanged.emit()

	#def showPopUp

	@Property(bool, notify=closeGuiChanged)
	def closeGui(self):

		return self._closeGui

	#def closeGui	

	@closeGui.setter
	def closeGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui
			self.closeGuiChanged.emit()

	#def closeGui

	def _getSystemLocale(self):

		return self._systemLocale

	#def _getSystemLocale

	def initBridge(self):

		self.currentStack=0
		self.closeGui=False
		self.gatherInfoT=GatherInfo(self.bellManager)
		self.gatherInfoT.start()
		self.gatherInfoT.infoGathered.connect(self._loadConfig)
		self.gatherInfoT.finished.connect(self.gatherInfoT.deleteLater)
	
	#def initBridge
	
	@Slot(dict)
	def _loadConfig(self,ret):

		self.closeGui=True

		if not ret.get('status'):
			self.showLoadErrorMessage={"show":True,"msgCode":ret.get('code')}
		else:
			self.core.bellsOptionsStack.loadConfig()
			self.core.bellStack.updateImagesModel()
			self._systemLocale=self.bellManager.systemLocale
			
			if len(sys.argv)<3:
				if self.bellManager.loadError:
					self.core.bellsOptionsStack.showMainMessage={"show":True,"msgCode":self.bellManager.BELLS_WITH_ERRORS,"type":self.bellManager.KIRIGAMI_MSG_ERROR}
				
				self.currentStack=1
			else:
				tmpFile=sys.argv[2]
				if os.path.exists(tmpFile):
					self.core.bellStack.addNewBell(tmpFile)
				else:
					self.showLoadErrorMessage={"show":True,"msgCode":CREATE_BELL_FROM_MENU_ERROR}
			
	#def _loadConfig

	@Slot(int)
	def moveToMainOptions(self,stack):

		if self.mainCurrentOption!=stack:
			if stack==0:
				self.core.holidayStack.showMainMessage={"show":False,"msgCode":"","type":""}
				self.core.bellsOptionsStack.enableHolidayControl=self.bellManager.checkIfAreHolidaysConfigured()
				self.mainCurrentOption=stack
				if not self.core.bellsOptionsStack.enableHolidayControl:
					if self.core.bellsOptionsStack.isHolidayControlActive:
						self.core.bellsOptionsStack.manageHolidayControl()
			else:
				self.core.bellsOptionsStack.showMainMessage={"show":False,"msgCode":"","type":""}
				self._loadHolidayStack()

	#def moveToMainOptions	

	def _loadHolidayStack(self):

		self.closeGui=False
		self.showPopUp={"show":True,"msgCode":LOADING_HOLIDAY_LIST}
		self.loadHolidayConfigT=LoadHoliday()
		self.loadHolidayConfigT.start()
		self.loadHolidayConfigT.holidayLoaded.connect(self._loadHolidayConfigRet)
		self.loadHolidayConfigT.finished.connect(self.loadHolidayConfigT.deleteLater)

	#def _loadHolidayStack

	@Slot()
	def _loadHolidayConfigRet(self):

		self.closeGui=True
		self.showPopUp={"show":False,"msgCode":""}
		self.mainCurrentOption=1

	#def _loadHolidayConfigRet

	def manageGoToStack(self):

		if self.moveToStack!="":
			self.currentStack=self.moveToStack
			self.mainCurrentOption=0
			self.moveToStack=""

	#def _manageGoToStack

	@Slot()
	def openHelp(self):
		
		if 'valencia' in self._systemLocale:
			helpUrl='https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Bell-Scheduler.'
		else:
			helpUrl='https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Bell-Scheduler'
		
		QDesktopServices.openUrl(helpUrl)

	#def openHelp

	@Slot()
	def closeBellScheduler(self):

		if self.core.bellStack.changesInBell:
			self.closeGui=False
			self.core.bellStack.showChangesInBellDialog=True

	#def closeBellScheduler
	
	systemLocale=Property(str,_getSystemLocale,constant=True)

#class Bridge

from . import Core


