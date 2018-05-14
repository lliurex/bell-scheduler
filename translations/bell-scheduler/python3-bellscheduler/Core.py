#!/usr/bin/env python3

import sys


from . import bellmanager
from . import MainWindow
from . import BellBox
from . import EditBox
from . import settings

import holidaymanager.HolidayBox as HolidayBox


class Core:
	
	singleton=None
	DEBUG=False
	
	@classmethod
	def get_core(self):
		
		if Core.singleton==None:
			Core.singleton=Core()
			Core.singleton.init()

		return Core.singleton
		
	
	def __init__(self,args=None):

	
		self.dprint("Init...")
		
	#def __init__
	
	def init(self):

		self.rsrc_dir= settings.RSRC_DIR + "/"
		self.ui_path= settings.RSRC_DIR + "/bell-scheduler.ui"
		self.images_path="/usr/local/share/bellScheduler/images"
		self.sounds_path="/usr/local/share/bellScheduler/sounds"

		
		self.bellmanager=bellmanager.BellManager()
		self.bellBox=BellBox.BellBox()
		self.editBox=EditBox.EditBox()
		self.holidayBox=HolidayBox.HolidayBox("BELL SCHEDULER")
		self.mainWindow=MainWindow.MainWindow()
				
			
		self.mainWindow.load_gui()
		self.mainWindow.start_gui()
			
		
		
	#def init
	
	
	
	def dprint(self,msg):
		
		if Core.DEBUG:
			
			print("[CORE] %s"%msg)
	
	#def  dprint
