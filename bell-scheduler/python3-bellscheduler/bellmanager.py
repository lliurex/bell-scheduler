#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib
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
import threading
import glob
import random
import urllib.request



class BellManager(object):

	MISSING_BELL_NAME_ERROR=-1
	INVALID_SOUND_FILE_ERROR=-2
	MISSING_SOUND_FILE_ERROR=-3
	INVALID_IMAGE_FILE_ERROR=-4
	MISSING_IMAGE_FILE_ERROR=-5
	MISSING_URL_ERROR=-6
	MISSING_SOUND_FOLDER_ERROR=-7
	SOUND_FILE_URL_NOT_VALID_ERROR=-8
	FOLDER_WITH_INCORRECT_FILES_ERROR=-38
	MISSING_URL_LIST_ERROR=-39
	INCORRECT_URL_LIST_ERROR=-40
	TIME_OUT_VALIDATION_ERROR=-41
	FAILED_INTERNET_ERROR=-42
	URL_FILE_NOT_VALID_ERROR=-43

	ACTION_SUCCESSFUL=0


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

	def check_data(self,data):

		'''
		Result code:
			-1: Missing bell name
			-3: Missing sound file
			-5: Missing image file
			-6: Missing url
			-7: Missing sound directory
			-39: Missing list url
			-42: Failed internet connection 

		'''	
		
		check_image=None
		check_sound=None

		if data["name"]=="":
			return {"result":False,"code":BellManager.MISSING_BELL_NAME_ERROR,"data":""}
			

						
		if data["image"]["option"]=="custom":						
			if data["image"]["file"]!=None:
				check_image=self.check_mimetypes(data["image"]["file"],"image")
				
			else:
				return {"result":False,"code":BellManager.MISSING_IMAGE_FILE_ERROR,"data":""}
		
		if check_image==None:
			if data["sound"]["option"]=="file":
				if data["sound"]["file"]!=None:
					check_sound=self.check_mimetypes(data["sound"]["file"],"audio")
					
					if check_sound==None:
						return self.check_audiofile(data["sound"]["file"],"file")
					else:
						return check_sound
				else:
					return {"result":False,"code":BellManager.MISSING_SOUND_FILE_ERROR,"data":""}

			elif data["sound"]["option"]=="directory":
				if data["sound"]["file"]==None:
					return {"result":False,"code":BellManager.MISSING_SOUND_FOLDER_ERROR,"data":""}
				else:
					self.correct_files=0
					return self.check_directory(data["sound"]["file"])	

			elif data["sound"]["option"]=="url":			
				if data["sound"]["file"]=="":
					return {"result":False,"code":BellManager.MISSING_URL_ERROR,"data":""}
				else:
					check_connection=self.check_connection()
					if check_connection:
						return self.check_audiofile(data["sound"]["file"],"url")
					else:
						return {"result":False,"code":BellManager.FAILED_INTERNET_ERROR,"data":""}	

			elif data["sound"]["option"]=="urlslist":				
				if data["sound"]["file"]!=None:
					check_connection=self.check_connection()
					if check_connection:
						return self.check_list(data["sound"]["file"])
					else:
						return {"result":False,"code":BellManager.FAILED_INTERNET_ERROR,"data":""}	
				else:		
					return {"result":False,"code":BellManager.MISSING_URL_LIST_ERROR,"data":""}
			
						
		else:
			return check_image			
				
	
	#def check_data
	
	def check_mimetypes(self,file,check):

		'''
		Result code:
			-2: Invalid sound file
			-4: Invalid image file
		
		'''	
	
		mime = MimeTypes()
		file_mime_type= mime.guess_type(file)
		error=False
		
		if check=="audio":
			if file_mime_type[0]!=None:
				if not 'audio' in file_mime_type[0] and not 'video' in file_mime_type[0]:
					error=True
			else:
				error=True
		else:
			if file_mime_type[0]!=None:
				if not 'image' in file_mime_type[0]: 
					error=True
			else:
				error=True

		if error:
			if check=="audio":
				return {"result":False,"code":BellManager.INVALID_SOUND_FILE_ERROR,"data":""}
			else:
				return {"result":False,"code":BellManager.INVALID_IMAGE_FILE_ERROR,"data":""}				
		
	#def check_mimetypes			
				
	def check_audiofile(self,file,type):

		'''
		Result code:
			-0: All correct
			-8: Sound file or ulr not valid
		
		'''	
		
		params=' -show_entries stream=codec_type,duration -of compact=p=0:nk=1'
		
		if type=="file":
			cmd='ffprobe -i "'+file +'"'+ params
		else:
			cmd='ffprobe -i $(youtube-dl -g "'+file+'" |sed -n 2p) '+params

			
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()[0]
		
		if len(poutput)==0:
			return {"result":False,"code":BellManager.SOUND_FILE_URL_NOT_VALID_ERROR,"data":""}	
		else:
			return {"result":True,"code":BellManager.ACTION_SUCCESSFUL,"data":""}
	
	
	#def check_audiofile	

	def check_directory(self,directory):

		'''
		Result code:
			-0: All correct
			-38: Not correct files in directory
		
		'''	

		
		path=directory+"/*"
		content_directory=glob.glob(path)
		for item in content_directory:
			if os.path.isfile(item):
				check_file=self.check_mimetypes(item,"audio")
				if check_file==None:
					check_run=self.check_audiofile(item,'file')
					if check_run["result"]:
						self.correct_files+=1
			else:
				if os.path.isdir(item):
					self.check_directory(item)			
		
		if self.correct_files>0:
			return {"result":True,"code":BellManager.ACTION_SUCCESSFUL,"data":""}
		else:
			return {"result":False,"code":BellManager.FOLDER_WITH_INCORRECT_FILES_ERROR,"data":""}

	#def check_directory		

	def check_list(self,url_list):

		'''
		Result code:
			-0: All correct
			-40: Url list with errors
			-41: time out validation
			-43: File not valid 
		
		'''	
		result=True
		data=""
		code=BellManager.ACTION_SUCCESSFUL
		self.url_invalid=[]
		self.error_lines=[]
		self.file=url_list
		self.sync_threads={}
		self.read_list()
		self.max_timeout=300
		self.current_timeout=0

		while self.worker():
			import time
			time.sleep(1)

		if self.worker_ret==0:	
			if len(self.sync_threads)>0:
				if len(self.url_invalid)>0 or len(self.error_lines):
					data=self.order_error_lines()
					result=False
					code=BellManager.INCORRECT_URL_LIST_ERROR
			else:
				result=False
				code=BellManager.URL_FILE_NOT_VALID_ERROR
							
		else:
			result=False
			code=BellManager.TIME_OUT_VALIDATION_ERROR

		return {"result":result,"code":code,"data":data}					

	#def check_list		
	
	def worker(self):

		self.current_timeout+=1
		self.worker_ret=1
		if self.current_timeout > self.max_timeout:
			self.worker_ret=-1
			return False

		for i in range(len(self.threads_alive)-1,-1,-1):
			if not self.threads_alive[i].is_alive():
				self.threads_alive.pop(i)

		if len(self.threads_alive)>0:
			return True

		self.worker_ret=0
		return False

	#def worker


	def generate_url_threads(self,item,line_num):
		
		id=int(random.random()*1000)		
		t=threading.Thread(target=self.check_url,args=(id,item,line_num))
		t.daemon=True
		t.start()
		self.sync_threads[id]={}
		self.sync_threads[id]["thread"]=t
		return t	

	#def generate_url_threads	

	def read_list(self):

		try:
			content=open(self.file,'r')
			self.threads_alive=[]
			line_num=1
			if os.stat(self.file).st_size>0:
				for line in content.readlines():
					if line!="\n":
						if line.startswith("http:") or line.startswith("https:"):
							t=self.generate_url_threads(line,line_num)
							self.threads_alive.append(t)
						else:
							self.error_lines.append(line_num)	
					line_num+=1
		except:
			pass			
		
	#def read_list		

	def	check_url(self,id,line,line_num):

		params=' -show_entries stream=codec_type,duration -of compact=p=0:nk=1'
		cmd='ffprobe -i $(youtube-dl -g "'+line+'" |sed -n 2p) '+params
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		poutput=p.communicate()[0]
		if len(poutput)==0:
			self.url_invalid.append(line_num)
	
	#def check_url	

	def order_error_lines(self):

		errors=""
		
		error_lines=sorted(self.url_invalid+self.error_lines)	
		for item in  error_lines:
			errors=errors+","+str(item)

		return errors[1:]

	#def get_lines_error	

	def check_connection(self):
	
		try:
			res=urllib.request.urlopen("http://lliurex.net")
			return True
			
		except:
			return False	

	#def check_connection		
			
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


	def change_activation_status(self,action):

		result=self.n4d.change_activation_status(self.credentials,'BellSchedulerManager',action)
		self._debug("Activation/Deactivation process: ",result)	
		return result

	#def change_activation_status	

	def remove_all_bells(self):

		result=self.n4d.remove_all_bells(self.credentials,'BellSchedulerManager')
		self._debug("Remove all bells process: ",result)	
		return result

	#def remove_all_bells			
							

#class BellManager 		
