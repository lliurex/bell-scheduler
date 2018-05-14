 
import os
import json
import codecs
import shutil
import xmlrpclib as n4dclient
import ssl
import zipfile


class BellSchedulerManager(object):

	def __init__(self):

		self.config_dir=os.path.expanduser("/etc/bellScheduler/")
		self.config_file=self.config_dir+"bell_list"
		self.holiday_token=self.config_dir+"enabled_holiday_token"
		self.cron_dir="/etc/scheduler/tasks.d/"
		self.cron_file=os.path.join(self.cron_dir,"BellScheduler")

		self.images_folder="/usr/local/share/bellScheduler/images"
		self.sounds_folder="/usr/local/share/bellScheduler/sounds"
		self.media_files_folder="/usr/local/share/bellScheduler/"
	

		server='localhost'
		context=ssl._create_unverified_context()
		self.n4d = n4dclient.ServerProxy("https://"+server+":9779",context=context,allow_none=True)
		
		self._get_n4d_key()


	#def __init__	


	def _get_n4d_key(self):

		self.n4dkey=''
		with open('/etc/n4d/key') as file_data:
			self.n4dkey = file_data.readlines()[0].strip()

	#def _get_n4d_key

	def _create_conf(self):

		if not os.path.exists(self.config_dir):
			os.makedirs(self.config_dir)

		if not os.path.exists(self.images_folder):
			os.makedirs(self.images_folder)

		if not os.path.exists(self.sounds_folder):
			os.makedirs(self.sounds_folder)		
		
		var={}
		with codecs.open(self.config_file,'w',encoding="utf-8") as f:
			json.dump(var,f,ensure_ascii=False)
			f.close()

		return {"status":True,"msg":"Configuration file created successfuly"}

	#def create_conf		
	

	def read_conf(self):
		
		if not os.path.exists(self.config_file):
			self._create_conf()
		
		f=open(self.config_file)
		
		try:
			self.bells_config=json.load(f)
		except Exception as e:

			self.bells_config={}
			return {"status":False,"msg":"Unabled to read configuration file :" +str(e),"code":25,"data":self.bells_config}


		f.close()	

		return {"status":True,"msg":"Configuration file readed successfuly","code":26,"data":self.bells_config}

	#def read_conf	

	def _get_tasks_from_cron(self):

		cron_tasks={}
		tmp_tasks={}
		tasks=self.n4d.get_local_tasks(self.n4dkey,'SchedulerServer')
		
		if tasks["status"]:

			for item in tasks["data"]:
				if item=="BellScheduler":
					tmp_tasks=tasks["data"][item]

			if len(tmp_tasks)>0:
				for	item in tmp_tasks:
					key=str(tmp_tasks[item]["BellId"])
					cron_tasks[key]={}
					cron_tasks[key]["CronId"]=item
		
		return cron_tasks

	#def _get_tasks_from_cron	
		
	
	def sync_with_cron(self):
	
		bell_tasks=self.read_conf()["data"]
		keys_bells=bell_tasks.keys()

		bells_incron=self._get_tasks_from_cron()
		keys_cron=bells_incron.keys()
		changes=0

		if len(keys_cron)>0:
			for item in bell_tasks:
				if item in keys_cron:
					if bell_tasks[item]["active"]:
						pass
					else:
						changes+=1
						bell_tasks[item]["active"]=True
				else:
					if bell_tasks[item]["active"]:
						changes+=1
						bell_tasks[item]["active"]=False
					else:
						pass

			for item in keys_cron:
				if item not in keys_bells:
					result=self._delete_from_cron(item)
					if not result["status"]:
						return {"status":False,"msg":"Unable to clear alarm from cron file","code":37}
		else:
			for item in bell_tasks:
				if bell_tasks[item]["active"]:
					changes+=1
					bell_tasks[item]["active"]=False
					

		if changes>0:
			self._write_conf(bell_tasks,"BellList")

		return {"status":True,"msg":"Sync with cron sucessfully","data":bell_tasks}	
					

	#def sync_with_cron	

	def _write_conf(self,info,type_list):
		
		if type_list=="BellList":
			self.bells_config=info
			file_to_write=self.config_file
			msg="Bell list saved successfuly"
		else:
			file_to_write=self.cron_file
			msg="Cron list saved successfuly"

		
		with codecs.open(file_to_write,'w',encoding="utf-8") as f:
			json.dump(info,f,ensure_ascii=False)
			f.close()	

		return {"status":True,"msg":msg}	


	#def _write_conf	

	def save_changes(self,info,last_change,action):
		
		turn_on=False
		if action !="remove":
			if info[last_change]["active"]:
				turn_on=True
				tasks_for_cron=self._format_to_cron(info,last_change,action)
				result=self.n4d.write_tasks(self.n4dkey,'SchedulerServer','local',tasks_for_cron)

			else:
				result=self._delete_from_cron(last_change)
		else:
			result=self._delete_from_cron(last_change)


		if result['status']:	
			return self._write_conf(info,"BellList")
		else:
			if action=="edit":
				return {"status":False,"action":action,"msg":result['data'],"code":19}	
			elif action=="add":
				return {"status":False,"action":action,"msg":result['data'],"code":20}
			elif action=="remove":
				return {"status":False,"action":action,"msg":result['data'],"code":21}	
			elif action=="active":	
				if turn_on:
					return {"status":False,"action":action,"msg":result['data'],"code":22}
				else:
					return {"status":False,"action":action,"msg":result['data'],"code":23}
		
	#def save_changes				

	def _get_cron_id(self,last_change):

		cron_tasks=self._get_tasks_from_cron()
		if len(cron_tasks)>0:
			if last_change in cron_tasks.keys():
				return {"status":True, "id":cron_tasks[last_change]}
		
		return {"status":False,"id":{"CronId":0}}

	# def _get_cron_id	
	
	def _delete_from_cron(self,last_change):

		id_to_remove=self._get_cron_id(last_change)
		cron_id=id_to_remove["id"]["CronId"]
		delete={"status":True,"data":"0"}

		if id_to_remove["status"]:
			delete=self.n4d.remove_task(self.n4dkey,'SchedulerServer','local','BellScheduler',cron_id,'cmd')
			
		return delete

	#def _delete_from_cron	
	
	def _format_to_cron(self,info,item,action):

		info_to_cron={}
		
	
		if action=="edit" or action=="active":
			cron_tasks=self._get_tasks_from_cron()
			try:
				key=cron_tasks[item]["CronId"]
			except:
				key="0"	
		else:
			key="0"
			
		info_to_cron["BellScheduler"]={}
		info_to_cron["BellScheduler"][key]={}
		info_to_cron["BellScheduler"][key]["name"]=info[item]["name"]
		info_to_cron["BellScheduler"][key]["dom"]="*"
		info_to_cron["BellScheduler"][key]["mon"]="*" 
		info_to_cron["BellScheduler"][key]["h"]=str(info[item]["hour"])
		info_to_cron["BellScheduler"][key]["m"]=str(info[item]["minute"])
		info_to_cron["BellScheduler"][key]["protected"]=True

		weekdays=info[item]["weekdays"]
		days=""
		if weekdays["0"]:
			days=days+"1,"
		if weekdays["1"]:
			days=days+"2,"
		if weekdays["2"]:
			days=days+"3,"
		if weekdays["3"]:
			days=days+"4,"
		if weekdays["4"]:
			days=days+"5,"

		if days!="":
			days=days[:-1]

		else:
			days='*'

		info_to_cron["BellScheduler"][key]["dow"]=days
		info_to_cron["BellScheduler"][key]["BellId"]=item				

		
		sound_option=info[item]["sound"]["option"]
		sound_path=info[item]["sound"]["path"]
		duration=info[item]["play"]["duration"]


		if duration>0:
			fade_out=int(duration)-2
			fade_effects='-af aformat=channel_layouts=mono -af afade=in:st=0:d=6,afade=out:st='+str(fade_out)+":d=2"
			cmd="ffplay -nodisp -autoexit -t "+str(duration)
		else:
			fade_effects='-af aformat=channel_layouts=mono '
			cmd="ffplay -nodisp -autoexit "

		if sound_option !="url":
			if sound_option =="file":
				cmd=cmd+' "'+ sound_path +'" '+fade_effects
			else:
				#random_file="$(find"+ " '"+sound_path+"' -type f -print0 | xargs -0 file -i | awk -F ':' '{ if ($2 ~ /audio/ || $2 ~ /video/ ) print $1 }'| shuf -n 1)"
				random_file="$(randomaudiofile" + " '"+sound_path+"')"
				cmd=cmd+' "'+ random_file + '" '+fade_effects
				#cmd=cmd+" $(find"+ " '"+sound_path+"' -type f | shuf -n 1) "+fade_effects		
		else:
			cmd=cmd+ " $(youtube-dl -g "+sound_path+ " | sed -n 2p) "+fade_effects 
			
		info_to_cron["BellScheduler"][key]["cmd"]=cmd

		if os.path.exists(self.holiday_token):
			info_to_cron["BellScheduler"][key]["holidays"]=True
		else:
			info_to_cron["BellScheduler"][key]["holidays"]=False
	
			
		return info_to_cron

	#def _format_to_cron	

	def copy_media_files(self,image,sound):


		if image!="":
			image_file=os.path.basename(image)
			image_dest=os.path.join(self.images_folder,image_file)

		if sound!="":
			sound_file=os.path.basename(sound)
			sound_dest=os.path.join(self.sounds_folder,sound_file)

		try:
			if image!="":
				if not os.path.exists(image_dest):
					shutil.copy2(image,image_dest)

			if sound!="":
				if not os.path.exists(sound_dest):
					shutil.copy2(sound,sound_dest)

			result={"status":True,"msg":"Files copied successfully"}
		except Exception as e:
				result={"status":False,"msg":str(e),"code":24}		

		return result
	
	#def copy_media_files

	def export_bells_conf(self,dest_file,user,arg=None):

		tmp_export=tempfile.mkdtemp("_bell_export")
		
		try:
			shutil.copy2(self.config_file,os.path.join(tmp_export,os.path.basename(self.config_file)))
			if os.path.exists(self.cron_file):
				shutil.copy2(self.cron_file,os.path.join(tmp_export,os.path.basename(self.cron_file)))
			if os.path.exists(self.holiday_token):
				shutil.copy2(self.holiday_token,os.path.join(tmp_export,os.path.basename(self.holiday_token)))

			if os.path.exists(self.media_files_folder):
				shutil.copytree(self.media_files_folder,os.path.join(tmp_export,"media"))
			
			shutil.make_archive(dest_file, 'zip', tmp_export)
			if arg!=True:
				shutil.rmtree(tmp_export)

			cmd='chown -R '+user+':'+user +" " + dest_file+'.zip'
			os.system(cmd)	
			result={"status":True,"msg":"Bells exported successfullly","code":11}
						
		except Exception as e:
			result={"status":False,"msg":str(e),"code":12}		

		return result 	

	#def export_bells_conf	

	def import_bells_conf(self,orig_file,user,backup):

		backup_file=["",""]
		unzip_tmp=tempfile.mkdtemp("_import_bells")
		result={"status":True}
		action="disable"

		if backup:
			backup_file=tempfile.mkstemp("_bells_backup")
			result=self.export_bells_conf(backup_file[1],user,True)

		try:	
			if result['status']:	
				tmp_zip=zipfile.ZipFile(orig_file)
				tmp_zip.extractall(unzip_tmp)
				tmp_zip.close	

				config_file=os.path.join(unzip_tmp,os.path.basename(self.config_file))	
				if os.path.exists(config_file):
					try:
						f=open(config_file)
						read=json.load(f)
						shutil.copy2(config_file,self.config_dir)
						f.close()
					except Exception as e:
						result={"status":False,"msg":str(e),"code":9,"data":backup_file[1]}	
						return result		
							
				cron_file=os.path.join(unzip_tmp,os.path.basename(self.cron_file))
				if os.path.exists(cron_file):
					try:
						f=open(cron_file)
						read=json.load(f)
						shutil.copy2(cron_file,self.cron_dir)
						f.close()
						#self.n4d.process_tasks(self.n4dkey,'SchedulerClient')
					except Exception as e:
						result={"status":False,"msg":str(e),"code":9,"data":backup_file[1]}	
						return result	

				holiday_token=os.path.join(unzip_tmp,os.path.basename(self.holiday_token))	
				if os.path.exists(holiday_token):
					action="enable"
					shutil.copyfile(holiday_token,self.holiday_token)	
				else:
					if os.path.exists(self.holiday_token):
						os.remove(self.holiday_token)

				if os.path.exists(self.images_folder):
					shutil.rmtree(self.images_folder)
					shutil.copytree(os.path.join(unzip_tmp,"media/images"),self.images_folder)

				if os.path.exists(self.sounds_folder):
					shutil.rmtree(self.sounds_folder)
					shutil.copytree(os.path.join(unzip_tmp,"media/sounds"),self.sounds_folder)
		
				update_holiday=self.enable_holiday_control(action)	
				
				if update_holiday["status"]:	
					result={"status":True,"msg":"Bells imported successfullly","code":10,"data":backup_file[1]}
				else:
					result={"status":False,"msg":update_holiday["msg"],"code":9}				
		except Exception as e:
			result={"status":False,"msg":str(e),"code":9,"data":backup_file[1]}	

		
		return result		

	#def import_bells_conf

	def enable_holiday_control(self,action):

		result=self._update_holiday_control(action)
		if result['status']:
			if action=="disable":
				if os.path.exists(self.holiday_token):
					os.remove(self.holiday_token)	
					result={"status":True,"msg":"Holiday token removed","code":34}
			else:
				if not os.path.exists(self.holiday_token):
					if not os.path.exists(self.config_dir):
						os.makedirs(self.config_dir)
					f=open(self.holiday_token,'w')
					f.close()
					result={"status":True,"msg":"Holiday token created","code":35}		
		
		return result		

	#def enable_holiday

	def _update_holiday_control(self,action):

		
		if os.path.exists(self.cron_file):
			f=open(self.cron_file)
			try:
				tasks_cron=json.load(f)
			except Exception as e:
				result={"status":False,"msg":str(e),"code":36}
				return result

			
			for item in	tasks_cron["BellScheduler"]:
				if action=="enable":
					tasks_cron["BellScheduler"][item]["holidays"]=True
				
				else:
					tasks_cron["BellScheduler"][item]["holidays"]=False

			
			self._write_conf(tasks_cron,"CronList")
			self.n4d.process_tasks(self.n4dkey,'SchedulerClient')
			result={"status":True,"msg":"Cron file updated","code":37}
		else:
			result={"status":True,"msg":"Cron file dosn't exists","code":37}			

		return result

	#def _update_holiday_control		
		
			

