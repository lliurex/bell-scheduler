#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib
import os
import json
import codecs
from mimetypes import MimeTypes
import tempfile
import shutil
import subprocess
import threading
import glob
import random
import urllib.request
import n4d.client
from datetime import datetime, date,timedelta
import gettext
_ = gettext.gettext


class BellManager(object):

	
	MISSING_BELL_NAME_ERROR=-1
	INVALID_SOUND_FILE_ERROR=-2
	MISSING_SOUND_FILE_ERROR=-3
	INVALID_IMAGE_FILE_ERROR=-4
	MISSING_IMAGE_FILE_ERROR=-5
	MISSING_URL_ERROR=-6
	MISSING_SOUND_FOLDER_ERROR=-7
	SOUND_FILE_URL_NOT_VALID_ERROR=-8
	SOUND_PATH_UNAVAILABLE=-31
	FOLDER_WITH_INCORRECT_FILES_ERROR=-38
	MISSING_URL_LIST_ERROR=-39
	INCORRECT_URL_LIST_ERROR=-40
	TIME_OUT_VALIDATION_ERROR=-41
	FAILED_INTERNET_ERROR=-42
	URL_FILE_NOT_VALID_ERROR=-43
	DAY_NOT_IN_VALIDITY_ERROR=-56

	ACTION_SUCCESSFUL=0


	def __init__(self):

		super(BellManager, self).__init__()

		self.dbg=0
		self.credentials=[]
		self.server='localhost'
		self.bellsConfigData=[]
		self.imgNoDispPath="/usr/lib/python3/dist-packages/bellscheduler/rsrc/image_nodisp.svg"
		self.bannersPath="/usr/share/bell-scheduler/banners"
		self.imagesConfigData=[]
		self.getImagesConfig()
		self.initValues()
		'''
		context=ssl._create_unverified_context()
		self.n4d = n4dclient.ServerProxy("https://"+server+":9779",context=context,allow_none=True)
		'''

	#def __init__	

	def createN4dClient(self,ticket):

		ticket=ticket.replace('##U+0020##',' ')
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)

	#def create_n4dClient

	def _debug(self,function,msg):

		if self.dbg==1:
			print("[BELLSCHEDULER]: "+ str(function) + str(msg))

	#def _debug		

	def syncWithCron(self):

		result=self.client.BellSchedulerManager.sync_with_cron()
		self._debug("SyncWithCron: ",result)
		return result

	#def syncWithCron

	def readConf(self):
		
		self.loadError=False
		result=self.client.BellSchedulerManager.read_conf()
		self._debug("Read configuration file: ",result)
		self.bellsConfig=result["data"]
		print(self.bellsConfig)
		self.bellsConfigData=[]
		if result["status"]:
			self.getBellsConfig()
	
		return result

	#def readConf	

	def getBellsConfig(self):

		orderBells=self.getOrderBell()

		for item in orderBells:
			soundError=False
			imgError=False
			tmp={}
			search=""
			tmp["id"]=item
			tmp["cron"]=self.formatTime(item)[2]
			search+=tmp["cron"]
			tmp["mo"]=self.bellsConfig[item]["weekdays"]["0"]
			if tmp["mo"]:
				search+=self._getDayToSearch(0)
			tmp["tu"]=self.bellsConfig[item]["weekdays"]["1"]
			if tmp["tu"]:
				search+=self._getDayToSearch(1)
			tmp["we"]=self.bellsConfig[item]["weekdays"]["2"]
			if tmp["we"]:
				search+=self._getDayToSearch(2)
			tmp["th"]=self.bellsConfig[item]["weekdays"]["3"]
			if tmp["th"]:
				search+=self._getDayToSearch(3)
			tmp["fr"]=self.bellsConfig[item]["weekdays"]["4"]
			if tmp["fr"]:
				search+=self._getDayToSearch(4)
			tmp["validity"]=self.bellsConfig[item]["validity"]["value"]
			search+=tmp["validity"]
			tmp["validityActivated"]=self.bellsConfig[item]["validity"]["active"]
			if os.path.exists(self.bellsConfig[item]["image"]["path"]):
				tmp["img"]=self.bellsConfig[item]["image"]["path"]
			else:
				imgError=True
				tmp["img"]=self.imgNoDispPath
				self.loadError=True

			tmp["name"]=self.bellsConfig[item]["name"]
			search+=tmp["name"]
			tmpRet=self._loadSoundPath(item)
			tmp["sound"]=tmpRet[1]
			if not tmpRet[0]:
				tmp["bellActivated"]=self.bellsConfig[item]["active"]
			else:
				soundError=True
				tmp["bellActivated"]=False
				self.bellsConfig[item]["active"]=False
				self.saveConf(self.bellsConfig,item,"active")
 
			tmp["metaInfo"]=search
			tmp["isSoundError"]=soundError
			tmp["isImgError"]=imgError

			self.bellsConfigData.append(tmp)

	
	#def getBellsConfig

	def getImagesConfig(self):

		self.imagesConfigData=[]

		tmpFiles=[]
		if os.path.exists(self.bannersPath):
			for item in os.listdir(self.bannersPath):
				tmpFiles.append(item)
			
			tmpFiles.sort()
			for item in tmpFiles:
				tmp={}
				tmp["imageSource"]="%s/%s"%(self.bannersPath,item)
				self.imagesConfigData.append(tmp)

	#def getImagesConfig

	def initValues(self):

		self.bellCron=[0,0]
		self.bellDays=[False,False,False,False,False]
		self.bellValidity=[False,""]
		self.validityRangeDate=True
		self.daysInRange=[]
		self.bellName=""
		self.bellImage=["stock",1,"/usr/share/bell-scheduler/banners/bell.png",False]
		self.bellSound=["file","",""]
		self.bellPlay=[0,0]
		self.bellActive=False
		self.currentBellConfig={}
		self.currentBellConfig["hour"]=self.bellCron[0]
		self.currentBellConfig["minute"]=self.bellCron[1]
		self.currentBellConfig["validity"]={}
		self.currentBellConfig["validity"]["active"]=self.bellValidity[0]
		self.currentBellConfig["validity"]["value"]=self.bellValidity[1]
		self.currentBellConfig["weekdays"]={}
		self.currentBellConfig["weekdays"]["0"]=self.bellDays[0]
		self.currentBellConfig["weekdays"]["1"]=self.bellDays[1]
		self.currentBellConfig["weekdays"]["2"]=self.bellDays[2]
		self.currentBellConfig["weekdays"]["3"]=self.bellDays[3]
		self.currentBellConfig["weekdays"]["4"]=self.bellDays[4]
		self.currentBellConfig["name"]=self.bellName
		self.currentBellConfig["image"]={}
		self.currentBellConfig["image"]["option"]=self.bellImage[0]
		self.currentBellConfig["image"]["path"]=self.imagesConfigData[self.bellImage[1]]["imageSource"]
		self.currentBellConfig["sound"]={}
		self.currentBellConfig["sound"]["option"]=self.bellSound[0]
		self.currentBellConfig["sound"]["path"]=self.bellSound[1]
		self.currentBellConfig["play"]={}
		self.currentBellConfig["play"]["duration"]=self.bellPlay[0]
		self.currentBellConfig["play"]["start"]=self.bellPlay[1]
		self.currentBellConfig["active"]=self.bellActive
	
	#def initValues

	def _loadSoundPath(self,bell):
		
		path=self.bellsConfig[bell]["sound"]["path"]
		option=self.bellsConfig[bell]["sound"]["option"]
		error=False
		
		if option!="url":
			if os.path.exists(path):
				if option=="file":
					file=os.path.basename(path)
					return [error,file]
				else:
					return [error,path]	
			else:
				self.loadError=True
				error=True
				msg=_("ERROR: File or directory not available")
				return [error,msg]	
		else:
				return [error,path]

	#def _loadSoundPath

	def _getDayToSearch(self,day):

		tmpDay=""
		if day==0:
			tmpDay+=_("Monday")
			tmpDay+=_("M")
			tmpDay+=("Mon")
		elif day==1:
			tmpDay+=_("Tuesday")
			tmpDay+=_("T")
			tmpDay+=_("Tue")
		elif day==2:
			tmpDay+=_("Wednesday")	
			tmpDay+=_("W")
			tmpDay+=_("Wed")
		elif day==3:
			tmpDay+=_("Thursday")
			tmpDay+=_("R")
			tmpDay+=_("Thu")
		elif day==4:
			tmpDay+=_("Friday")
			tmpDay+=_("F")	
			tmpDay+=_("Fri")

		return tmpDay

	#def _getDayToSearch

	def loadBellConfig(self,bellToLoad):

		self.currentBellConfig=self.bellsConfig[bellToLoad[0]]
		self.bellCron=[self.currentBellConfig["hour"],self.currentBellConfig["minute"]]
		self.bellDays=[self.currentBellConfig["weekdays"]["0"],self.currentBellConfig["weekdays"]["1"],self.currentBellConfig["weekdays"]["2"],self.currentBellConfig["weekdays"]["3"],self.currentBellConfig["weekdays"]["4"]]
		self.bellValidity=[self.currentBellConfig["validity"]["active"],self.currentBellConfig["validity"]["value"]]
		self.daysInRange=[]
		self._getValidityConfig(self.bellValidity[1])
		self.bellName=self.currentBellConfig["name"]
		if self.currentBellConfig["image"]["option"]=="stock":
			imgIndex=self._getImageIndexFromPath(self.currentBellConfig["image"]["path"])
		else:
			imgIndex=1
		self.bellImage=[self.currentBellConfig["image"]["option"],imgIndex,self.currentBellConfig["image"]["path"],bellToLoad[1]]
		tmpSoundFilePath=""
		tmpSoundDirectoryPath=""
		if self.currentBellConfig["sound"]["option"]=="file":
			tmpSoundFilePath=self.currentBellConfig["sound"]["path"]
		else:
			tmpSoundDirectoryPath=self.currentBellConfig["sound"]["path"]
		
		self.bellSound=[self.currentBellConfig["sound"]["option"],tmpSoundFilePath,tmpSoundDirectoryPath]
		self.bellPlay=[self.currentBellConfig["play"]["duration"],self.currentBellConfig["play"]["start"]]
		self.bellActive=self.currentBellConfig["active"]

	#def loadBellConfig

	def _getImageIndexFromPath(self,imagePath):

		for i in range(len(self.imagesConfigData)):
			if self.imagesConfigData[i]["imageSource"]==imagePath:
				return i

	#def _getImageIndexFromPath

	def _getValidityConfig(self,validityInfo):

		tmpValue=validityInfo

		if tmpValue!="":
			if "-" in tmpValue:
				self.validityRangeDate=True
				self.daysInRange=self.get_days_inrange(tmpValue)
			else:
				self.validityRangeDate=False
				self.daysInRange.append(tmpValue)

	#def _getValidityConfig
	
	def saveConf(self,info,last_change,action):

		self.bellsConfig=info
		change=str(last_change)
				
		result=self.client.BellSchedulerManager.save_changes(info,change,action)
		self._debug("Save configuration file: ",result)
		return result

	#def saveConf		

	def check_data(self,data):
		
		check_validity=None
		check_image=None
		check_sound=None

		if data["name"]=="":
			return {"result":False,"code":BellManager.MISSING_BELL_NAME_ERROR,"data":""}

		if data["validity"]["active"]:
			check_validity=self.check_validity(data["weekdays"],data["validity"]["value"])
		
		if check_validity==None:
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
		else:
			return check_validity			
				
	
	#def check_data
	
	def check_mimetypes(self,file,check):

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

		path=directory+"/*"
		content_directory=glob.glob(path)
		for item in content_directory:
			if os.path.isfile(item):
				print("ARCHIVO: %s"%item)
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
			
	def getOrderBell(self,info=None):
	
		tmp=[]
		order_bells=[]
		current_day=date.today().strftime('%d/%m/%Y')
		if info==None:
			if len(self.bellsConfig)>0:
				for item in self.bellsConfig:
					time=str(self.bellsConfig[item]["hour"])+":"+str(self.bellsConfig[item]["minute"])
					time_f=datetime.strptime(time,"%H:%M")
					try:
						if (self.bellsConfig[item]["validity"]["value"]!=""):
							if "-" in self.bellsConfig[item]["validity"]["value"]:
								date_toformat=self.bellsConfig[item]["validity"]["value"].split("-")[0]
								datef=datetime.strptime(date_toformat,"%d/%m/%Y")
							else:
								date_toformat=self.bellsConfig[item]["validity"]["value"]
								datef=datetime.strptime(date_toformat,"%d/%m/%Y")
						else:
							datef=datetime.strptime(current_day,"%d/%m/%Y")
					except:
						datef=datetime.strptime(current_day,"%d/%m/%Y")

					x=()
					x=item,time_f,datef
					tmp.append(x)
		else:
			
			for item in info:
				time=str(info[item]["hour"])+":"+str(info[item]["minute"])
				time_f=datetime.strptime(time,"%H:%M")
				try:
					if (info[item]["validity"]["value"]!=""):
						if "-" in info[item]["validity"]["value"]:
							date_toformat=info[item]["validity"]["value"].split("-")[0]
							datef=datetime.strptime(date_toformat,"%d/%m/%Y")
						else:
							date_toformat=info[item]["validity"]["value"]
							datef=datetime.strptime(date_toformat,"%d/%m/%Y")
					else:
						datef=datetime.strptime(current_day,"%d/%m/%Y")
				except:
					datef=datetime.strptime(current_day,"%d/%m/%Y")
				x=()
				x=item,time_f,datef
				tmp.append(x)		

		tmp.sort(key=lambda bell:(bell[1],bell[2]))
		for item in tmp:
			order_bells.append(item[0])

		return order_bells	

	#def getOrderBells
	

	def formatTime(self,item):
	
		time=[]
		hour=self.bellsConfig[item]["hour"]
		minute=self.bellsConfig[item]["minute"]

		if hour<10:
			hour='0'+str(hour)

		if minute<10:
			minute='0'+str(minute)

		cron=str(hour)+":"+str(minute)
		time=[hour,minute,cron]
		return time		

	#def formatTime	

	def copy_media_files(self,image,sound):

		#Old n4d:result=self.n4d.copy_media_files(self.credentials,'BellSchedulerManager',image,sound)
		result=self.client.BellSchedulerManager.copy_media_files(image,sound)
		self._debug("Copy files: ",result)
		return result

	#def copy_media_files	


	def export_bells_conf(self,dest_file):

		user=os.environ["USER"]
		#Old n4d: result=self.n4d.export_bells_conf(self.credentials,'BellSchedulerManager',dest_file,user)
		result=self.client.BellSchedulerManager.export_bells_conf(dest_file,user)
		self._debug("Export bells conf : ",result)
		return result

	#def export_bells_conf	


	def import_bells_conf(self,orig_file,backup):
		user=os.environ["USER"]
		#Old n4d: result=self.n4d.import_bells_conf(self.credentials,'BellSchedulerManager',orig_file,user,backup)
		result=self.client.BellSchedulerManager.import_bells_conf(orig_file,user,backup)
		self._debug("Import bells conf: ",result)	
		return result

	#def import_bells_conf	


	def recovery_bells_conf(self,orig_file,backup):
		user=os.environ["USER"]
		#Old n4d: result=self.n4d.import_bells_conf(self.credentials,'BellSchedulerManager',orig_file,user,backup)
		result=self.client.BellSchedulerManager.import_bells_conf(orig_file,user,backup)
		self._debug("Recovery bells conf: ",result)	
		return result

	#def recovery_bells_conf	

	def enable_holiday_control(self,action):

		#Old n4d: result=self.n4d.enable_holiday_control(self.credentials,'BellSchedulerManager',action)
		result=self.client.BellSchedulerManager.enable_holiday_control(action)
		self._debug("Enable holiday control: ",result)	
		return result

	#def enable_holiday	

	def change_activation_status(self,action):

		#Old n4d: result=self.n4d.change_activation_status(self.credentials,'BellSchedulerManager',action)
		result=self.client.BellSchedulerManager.change_activation_status(action)
		self._debug("Activation/Deactivation process: ",result)	
		return result

	#def change_activation_status	

	def remove_all_bells(self):

		#Old n4d: result=self.n4d.remove_all_bells(self.credentials,'BellSchedulerManager')
		result=self.client.BellSchedulerManager.remove_all_bells()
		self._debug("Remove all bells process: ",result)	
		return result

	#def remove_all_bells

	def check_validity(self,weekdays,validity):

		days_in_validity=[]
		weekdays_selected=[]
		weekdays_validity=[]
		no_match_day=0
		
		if validity!="":
			if "-" in validity:
				days_in_validity=self.get_days_inrange(validity)
			else:
				days_in_validity.append(validity)

			for item in days_in_validity:
				tmp_day=datetime.strptime(item,"%d/%m/%Y")
				tmp_weekday=tmp_day.weekday()
				if tmp_weekday not in weekdays_validity:
					weekdays_validity.append(tmp_weekday)

			for i in range(len(weekdays)):
				if weekdays[i]:
					weekdays_selected.append(i)

			for item in weekdays_selected:
				if item not in weekdays_validity:
					no_match_day+=1

			if no_match_day>0:
				return {"result":False,"code":BellManager.DAY_NOT_IN_VALIDITY_ERROR,"data":""}

	#def check_validity

	def get_days_inrange(self,day):	

		list_days=[]
		tmp=day.split("-")
		date1=datetime.strptime(tmp[0],'%d/%m/%Y')
		date2=datetime.strptime(tmp[1],'%d/%m/%Y')
		delta=date2-date1
		for i in range(delta.days + 1):
			tmp_day=(date1 + timedelta(days=i)).strftime('%d/%m/%Y')
			list_days.append(tmp_day)

		return list_days	

	#def get_days_inrange


							

#class BellManager 		
