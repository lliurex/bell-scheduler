#!/usr/bin/env python3

import sys


from . import BellManager
from . import BellStack
from . import BellsOptionsStack
from . import MainStack
import holidaymanager.HolidayStack as HolidayStack

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

	
		self.bellManager=BellManager.BellManager()
		self.bellStack=BellStack.Bridge()
		self.bellsOptionsStack=BellsOptionsStack.Bridge()
		self.mainStack=MainStack.Bridge()
		
		self.holidayStack=HolidayStack.Bridge("Bell-Scheduler")
		self.mainStack.initBridge()
	
		
	#def init

	def dprint(self,msg):
		
		if Core.DEBUG:
			
			print("[CORE] %s"%msg)
	
	#def  dprint
