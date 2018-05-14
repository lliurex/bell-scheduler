#!/usr/bin/env python3

import os
import json
import codecs
import datetime
from mimetypes import MimeTypes
import xmlrpc.client as n4dclient
import ssl
import tempfile
import shutil
import subprocess



class BellManager(object):

	def __init__(self):

		super(BellManager, self).__init__()

		self.dbg=0
		self.credentials=[]
		server='localhost'
		context=ssl._create_unverified_context()
		self.n4d = n4dclient.ServerProxy("https://"+server+":9779",context=context,allow_none=True)
		

	#def __init__	

	def _debug(self,function,msg):

		if self.dbg==1:
			print("[BELLSCHEDULER]: "+ str(function) + str(msg))

	#def _debug		

	def sync_with_cron(self):

		result=self.n4d.sync_with_cron(self.credentials,'BellSchedulerManager')
		self._debug("Sync_with_cron: ",result)
		return result

		
	#def sync_with_cron


	def read_conf(self):
		
		result=self.n4d.read_conf(self.credentials,'BellSchedulerManager')
		self._debug("Read configuration file: ",result)
		self.bells_config=result["data"]
		return result
		

	#def read_conf	

	
	def save_conf(self,info,last_change,action):

		self.bells_config=info
		change=str(last_change)
				
		result=self.n4d.save_changes(self.credentials,'BellSchedulerManager',info,change,action)
		self._debug("Save configuration file: ",result)
		return result

	#def save_conf		

	def check_data(self,name,files):
		
		check_image=None
		check_sound=None
		if name=="":
			return {"result":False,"code":1}
			

		if len(files)>0:
									
			if files["image"]!="":
				if files["image"]!=None:
					check_image=self.check_mimetypes(files["image"],"image")
					
				else:
					return {"result":False,"code":5}
			
			if check_image==None:
				if files["sound"]!="":
					if files["sound"]!=None:
						check_sound=self.check_mimetypes(files["sound"],"audio")
						if check_sound==None:
							return self.check_audiofile(files["sound"],"file")
						else:
							return check_sound
					else:
						return {"result":False,"code":3}
				
				if files["url"]!=None:
					if files["url"]=="":
						return {"result":False,"code":6}
					else:
						return self.check_audiofile(files["url"],"url")

				if files["directory"]!="":
					if files["directory"]==None:
						return {"result":False,"code":7}
					else:
						return {"result":True,"code":0}		
			else:
				return check_image			
		'''
		if duration==0:
			return {"result":False,"code":8}			
		'''
		return {"result":True,"code":0}			
	
	#def check_data
	
	def check_mimetypes(self,file,check):
	
		mime = MimeTypes()
		mime_type = mime.guess_type(file)
		
		if check=="audio":
			sound_mime=mime.guess_type(file)
			if not 'audio' in sound_mime[0] and not 'video' in sound_mime[0]:
				return {"result":False,"code":2}
				
		else:
			image_mime=mime.guess_type(file)
			if not 'image' in image_mime[0]: 
				return {"result":False,"code":4}
		
	#def check_mimetypes			
				
	def check_audiofile(self,file,type):
		
		params=' -show_entries stream=codec_type,duration -of compact=p=0:nk=1'
		
		if type=="file":
			cmd='ffprobe -i "'+file +'"'+ params
		else:
			cmd='ffprobe -i $(youtube-dl -g "'+file+'" |sed -n 2p) '+params

			
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()[0]
		
		if len(poutput)==0:
			return {"result":False, "code":8}	
		else:
			return {"result":True,"code":0}
	
	
	#def check_audiofile		
			
	def get_order_bell(self,info=None):
	
		tmp=[]
		order_bells=[]
		if info==None:
			if len(self.bells_config)>0:
				for item in self.bells_config:
					time=str(self.bells_config[item]["hour"])+":"+str(self.bells_config[item]["minute"])
					time_f=datetime.datetime.strptime(time,"%H:%M")
					x=()
					x=item,time_f
					tmp.append(x)
		else:
			for item in info:
				time=str(info[item]["hour"])+":"+str(info[item]["minute"])
				time_f=datetime.datetime.strptime(time,"%H:%M")
				x=()
				x=item,time_f
				tmp.append(x)		

		tmp.sort(key=lambda bell:bell[1])
		for item in tmp:
			order_bells.append(item[0])

		return order_bells	

	#def get_order_bells
	

	def format_time(self,item):
	
		time=[]
		hour=self.bells_config[item]["hour"]
		minute=self.bells_config[item]["minute"]

		if hour<10:
			hour='0'+str(hour)

		if minute<10:
			minute='0'+str(minute)

		cron=str(hour)+":"+str(minute)
		time=[hour,minute,cron]
		return time		

	#def format_time	

	def copy_media_files(self,image,sound):

		result=self.n4d.copy_media_files(self.credentials,'BellSchedulerManager',image,sound)
		self._debug("Copy files: ",result)
		return result

	#def copy_media_files	


	def export_bells_conf(self,dest_file):

		user=os.environ["USER"]
		result=self.n4d.export_bells_conf(self.credentials,'BellSchedulerManager',dest_file,user)
		self._debug("Export bells conf : ",result)
		return result

	#def export_bells_conf	


	def import_bells_conf(self,orig_file,backup):
		user=os.environ["USER"]
		result=self.n4d.import_bells_conf(self.credentials,'BellSchedulerManager',orig_file,user,backup)
		self._debug("Import bells conf: ",result)	
		return result

	#def import_bells_conf	


	def recovery_bells_conf(self,orig_file,backup):
		user=os.environ["USER"]
		result=self.n4d.import_bells_conf(self.credentials,'BellSchedulerManager',orig_file,user,backup)
		self._debug("Recovery bells conf: ",result)	
		return result

	#def recovery_bells_conf	

	def enable_holiday_control(self,action):

		result=self.n4d.enable_holiday_control(self.credentials,'BellSchedulerManager',action)
		self._debug("Enable holiday control: ",result)	
		return result

	#def enable_holiday	

#class BellManager 		