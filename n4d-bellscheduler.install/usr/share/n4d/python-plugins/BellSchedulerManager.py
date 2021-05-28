 
import os
import subprocess
import json
import codecs
import shutil
import tempfile
import zipfile
import n4d.server.core as n4dcore
import n4d.responses


class BellSchedulerManager:

	READ_CONF_FILE_ERROR=-25
	CRON_SYNC_PROBLEMS_ERROR=-37
	BELL_EDIT_ERROR=-19
	BELL_CREATE_ERROR=-20
	BELL_DELETE_ERROR=-21
	BELL_ACTIVATE_ERROR=-22
	BELL_DEACTIVATE_ERROR=-23
	COPY_MEDIA_FILES_ERROR=-24
	BELL_EXPORT_ERROR=-12
	BELL_IMPORT_ERROR=-9
	APPLY_CHANGES_DUETOCRON_ERROR=-36
	BELL_LIST_LOADED_DUETOCRON_ERROR=-37
	CHANGE_ACTIVATION_STATUS_ERROR=-48
	CHANGE_DEACTIVATION_STATUS_ERROR=-49
	REMOVE_ALL_BELLS_ERROR=-52

	READ_CONF_FILE_SUCCESSFUL=0
	BELL_EXPORT_SUCCESSFUL=11
	BELL_IMPORT_SUCCESSFUL=10
	HOLIDAY_DEACTIVATE_SUCCESSFUL=34
	HOLIDAY_ACTIVATE_SUCCESSFUL=35
	CHANGE_ACTIVATION_STATUS_SUCCESSFUL=46
	CHANGE_DEACTIVATION_STATUS_SUCCESSFUL=47
	REMOVE_ALL_BELLS_SUCCESSFUL=51

	def __init__(self):

		self.config_dir=os.path.expanduser("/etc/bellScheduler/")
		self.config_file=self.config_dir+"bell_list"
		self.holiday_token=self.config_dir+"enabled_holiday_token"
		self.cron_dir="/etc/scheduler/tasks.d/"
		self.cron_file=os.path.join(self.cron_dir,"BellScheduler")

		self.images_folder="/usr/local/share/bellScheduler/images"
		self.sounds_folder="/usr/local/share/bellScheduler/sounds"
		self.media_files_folder="/usr/local/share/bellScheduler/"
		
		self.indicator_token_folder="/tmp/.BellScheduler"
		self.indicator_token_path=os.path.join(self.indicator_token_folder,"bellscheduler-token")
		self.cmd_create_token='bellscheduler-token-management create_token '
		self.cmd_remove_token='bellscheduler-token-management remove_token '

		'''
		server='localhost'
		context=ssl._create_unverified_context()
		self.n4d = n4dclient.ServerProxy("https://"+server+":9779",context=context,allow_none=True)
		'''
		self._get_n4d_key()
		
		self.core=n4dcore.Core.get_core()


	#def __init__	

	
	def _get_n4d_key(self):

		self.n4dkey=''
		with open('/etc/n4d/key') as file_data:
			self.n4dkey = file_data.readlines()[0].strip()
	
	#def _get_n4d_key

	def _create_dirs(self):

		if not os.path.exists(self.images_folder):
			os.makedirs(self.images_folder)

		if not os.path.exists(self.sounds_folder):
			os.makedirs(self.sounds_folder)	

	#def _create_dirs			
	
	def _create_conf(self):

		var={}

		if not os.path.exists(self.config_dir):
			os.makedirs(self.config_dir)

		with codecs.open(self.config_file,'w',encoding="utf-8") as f:
			json.dump(var,f,ensure_ascii=False)
			f.close()

		
		return {"status":True,"msg":"Configuration file created successfuly","code":"","data":""}

	#def create_conf		
	

	def read_conf(self):
		
		self._create_dirs()	
		
		if not os.path.exists(self.config_file):
			self._create_conf()
		
		f=open(self.config_file)
		
		try:
			self.bells_config=json.load(f)
			result={"status":True,"msg":"Configuration file readed successfuly","code":BellSchedulerManager.READ_CONF_FILE_SUCCESSFUL,"data":self.bells_config}

		except Exception as e:

			self.bells_config={}
			#Old n4d: return {"status":False,"msg":"Unabled to read configuration file :" +str(e),"code":25,"data":self.bells_config}
			result={"status":False,"msg":"Unabled to read configuration file :" +str(e),"code":BellSchedulerManager.READ_CONF_FILE_ERROR,"data":self.bells_config}

		f.close()	

		#Old n4d:return {"status":True,"msg":"Configuration file readed successfuly","code":BellSchedulerManager.READ_CONF_FILE_SUCCESSFUL,"data":self.bells_config}
		return n4d.responses.build_successful_call_response(result)

	#def read_conf	

	def _get_tasks_from_cron(self):

		cron_tasks={}
		tmp_tasks={}
		#Old n4d: tasks=self.n4d.get_local_tasks(self.n4dkey,'SchedulerServer')
		
		try:
			tasks=self.core.get_plugin('SchedulerServer').get_local_tasks()
			if tasks.get("status",None)==0:

				for item in tasks.get('return',None):
					if item=="BellScheduler":
						tmp_tasks=tasks.get('return',None)[item]

				if len(tmp_tasks)>0:
					for	item in tmp_tasks:
						key=str(tmp_tasks[item]["BellId"])
						cron_tasks[key]={}
						cron_tasks[key]["CronId"]=item
		except Exception as e:
			print("BellSchedulerManager-SchedulerServer:_get_tasks_from_cron.Error: "+str(e))
			pass
		
		return cron_tasks

	#def _get_tasks_from_cron	
		
	
	def sync_with_cron(self):
	
		bell_tasks=self.read_conf().get('return',None).get('data',None)
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
					if result.get('status',None)!=0:
						#Old n4d:return {"status":False,"msg":"Unable to clear alarm from cron file","code":37,"data":""}
						tmp_result={"status":False,"msg":"Unable to clear alarm from cron file","code":BellSchedulerManager.CRON_SYNC_PROBLEMS_ERROR,"data":""}
						return n4d.responses.build_successful_call_response(tmp_result)
	
		else:
			for item in bell_tasks:
				if bell_tasks[item]["active"]:
					changes+=1
					bell_tasks[item]["active"]=False
					

		if changes>0:
			self._write_conf(bell_tasks,"BellList")

		#Old n4d: return {"status":True,"msg":"Sync with cron sucessfully","code":"","data":bell_tasks}	
		tmp_result={"status":True,"msg":"Sync with cron sucessfully","code":"","data":bell_tasks}	
		return n4d.responses.build_successful_call_response(tmp_result)
				

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

		#Ol N4D:eturn {"status":True,"msg":msg}	
		result={"status":True,"msg":msg}
		return n4d.responses.build_successful_call_response(result)


	#def _write_conf	

	def save_changes(self,info,last_change,action):

		turn_on=False
		if action !="remove":
			if info[last_change]["active"]:
				turn_on=True
				tasks_for_cron=self._format_to_cron(info,last_change,action)
				#Old n4d:result=self.n4d.write_tasks(self.n4dkey,'SchedulerServer','local',tasks_for_cron)
				try:
					result=self.core.get_plugin('SchedulerServer').write_tasks('local',tasks_for_cron)
				except Exception as e:
					print("BellSchedulerManager-SchedulerServer:save_changes.Error: "+str(e))
					result={"status":-1}	
			else:
				result=self._delete_from_cron(last_change)
		else:
			result=self._delete_from_cron(last_change)


		if result.get('status',None)==0:	
			return self._write_conf(info,"BellList")
		else:
			if action=="edit":
				tmp_result={"status":False,"action":action,"msg":result.get('return',None),"code":BellSchedulerManager.BELL_EDIT_ERROR,"data":""}	
			elif action=="add":
				tmp_result={"status":False,"action":action,"msg":result.get('return',None),"code":BellSchedulerManager.BELL_CREATE_ERROR,"data":""}
			elif action=="remove":
				tmp_result={"status":False,"action":action,"msg":result.get('return',None),"code":BellSchedulerManager.BELL_DELETE_ERROR,"data":""}	
			elif action=="active":	
				if turn_on:
					tmp_result={"status":False,"action":action,"msg":result.get('return',None),"code":BellSchedulerManager.BELL_ACTIVATE_ERROR,"data":""}
				else:
					tmp_result={"status":False,"action":action,"msg":result.get('return',None),"code":BellSchedulerManager.BELL_DEACTIVATE_ERROR,"data":""}
			
			return n4d.responses.build_successful_call_response(tmp_result)	
	#def save_changes				

	def _get_cron_id(self,last_change):

		try:
			cron_tasks=self._get_tasks_from_cron()
			if len(cron_tasks)>0:
				if last_change in cron_tasks.keys():
					return {"status":True, "id":cron_tasks[last_change]}
		except Exception as e:
			print("BellSchedulerManager:_get_cron_id.Error:"+str(e))
			return {"status":False,"id":{}}
		
		
		return {"status":False,"id":{"CronId":0}}

	# def _get_cron_id	
	
	def _delete_from_cron(self,last_change):

		id_to_remove=self._get_cron_id(last_change)
		if len(id_to_remove["id"])>0:
			cron_id=id_to_remove["id"]["CronId"]
			delete={"status":0,"data":"0"}
			
			if id_to_remove["status"]:
				#OLd n4d:delete=self.n4d.remove_task(self.n4dkey,'SchedulerServer','local','BellScheduler',cron_id,'cmd')
				try:
					delete=self.core.get_plugin('SchedulerServer').remove_task('local','BellScheduler',cron_id,'cmd')
				except Exception as e:
					print("BellSchedulerManager-SchedulerServer:_delete_from_cron.Error:"+str(e))
					delete={"status":-1,"data":"0"}
					pass
		
		else:
			delete={"status":-1,"data":"0"}

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
			

		#write_token_command=" && echo "+item+" >>"+self.indicator_token_path+" && "	
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

		
			info_to_cron["BellScheduler"][key]["dow"]=days
			info_to_cron["BellScheduler"][key]["BellId"]=item				

			
			sound_option=info[item]["sound"]["option"]
			sound_path=info[item]["sound"]["path"]
			duration=info[item]["play"]["duration"]
			try:
				start_time=info[item]["play"]["start"]
			except:
				start_time=0	
			

			if duration>0:
				fade_out=int(duration)+int(start_time)-2
				fade_effects='-af aformat=channel_layouts=mono -af afade=in:st='+str(start_time)+':d=3,afade=out:st='+str(fade_out)+":d=2"
				cmd=self.cmd_create_token+item+" && ffplay -nodisp -autoexit " + "-ss "+ str(start_time) +" -t "+str(duration)
			else:
				fade_effects='-af aformat=channel_layouts=mono '
				cmd=self.cmd_create_token+item+" && ffplay -nodisp -autoexit -ss "+str(start_time)

			if sound_option=="file":
				cmd=cmd+' "'+ sound_path +'" '+fade_effects+';'+self.cmd_remove_token+item
			elif sound_option=="url":
				sound_path=sound_path.replace("%","\%")
				cmd=cmd+ ' $(youtube-dl -g "'+sound_path+'" | sed -n 2p) '+fade_effects+';'+self.cmd_remove_token+item	
			else:
				random_file="$(randomaudiofile" + " '"+sound_path+"')"
				if sound_option=="directory":
					cmd=cmd+' "'+ random_file + '" '+fade_effects+';'+self.cmd_remove_token+item
				elif sound_option=="urlslist":
					cmd=cmd+ ' $(youtube-dl -g "'+random_file+'" | sed -n 2p) '+fade_effects+';'+self.cmd_remove_token+item
				
			info_to_cron["BellScheduler"][key]["cmd"]=cmd

			if os.path.exists(self.holiday_token):
				info_to_cron["BellScheduler"][key]["holidays"]=True
			else:
				info_to_cron["BellScheduler"][key]["holidays"]=False
	
			
		return info_to_cron

	#def _format_to_cron	

	def copy_media_files(self,image,sound):

		self._create_dirs()
		
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

			result={"status":True,"msg":"Files copied successfully","code":"","data":""}
		except Exception as e:
				result={"status":False,"msg":str(e),"code":BellSchedulerManager.COPY_MEDIA_FILES_ERROR,"data":""}		

		return n4d.responses.build_successful_call_response(result)
	
	#def copy_media_files

	def export_bells_conf(self,dest_file,user,arg=None):

		tmp_export=tempfile.mkdtemp("_bell_export")
		self._create_dirs()
		
		try:
			shutil.copy2(self.config_file,os.path.join(tmp_export,os.path.basename(self.config_file)))
			if os.path.exists(self.cron_file):
				shutil.copy2(self.cron_file,os.path.join(tmp_export,os.path.basename(self.cron_file)))
			if os.path.exists(self.holiday_token):
				shutil.copy2(self.holiday_token,os.path.join(tmp_export,os.path.basename(self.holiday_token)))

			if os.path.exists(self.media_files_folder):
				shutil.copytree(self.media_files_folder,os.path.join(tmp_export,"media"))
			
			dest_file=os.path.splitext(dest_file)[0]
			shutil.make_archive(dest_file, 'zip', tmp_export)
			if arg!=True:
				shutil.rmtree(tmp_export)

			cmd='chown -R '+user+':'+user +" " + dest_file+'.zip'
			os.system(cmd)	
			result={"status":True,"msg":"Bells exported successfully","code":BellSchedulerManager.BELL_EXPORT_SUCCESSFUL,"data":""}
						
		except Exception as e:
			result={"status":False,"msg":str(e),"code":BellSchedulerManager.BELL_EXPORT_ERROR,"data":""}		

		return n4d.responses.build_successful_call_response(result) 	

	#def export_bells_conf	

	def import_bells_conf(self,orig_file,user,backup):


		backup_file=["",""]
		unzip_tmp=tempfile.mkdtemp("_import_bells")
		result={"status":True}
		action="disable"

		if backup:
			backup_file=tempfile.mkstemp("_bells_backup")
			result=self.export_bells_conf(backup_file[1],user,True)['return']

		try:
			if result['status']:	
				tmp_zip=zipfile.ZipFile(orig_file)
				tmp_zip.extractall(unzip_tmp)
				tmp_zip.close	

				try:
					config_file=os.path.join(unzip_tmp,os.path.basename(self.config_file))	
					f_config=open(config_file)
					read=json.load(f_config)
					self.update_config_file(config_file)
					shutil.copy2(config_file,self.config_dir)
					f_config.close()
					cron_file=os.path.join(unzip_tmp,os.path.basename(self.cron_file))
					if os.path.exists(cron_file):
						f_cron=open(cron_file)
						read=json.load(f_cron)
						shutil.copy2(cron_file,self.cron_dir)
						f_cron.close()
					
				except Exception as e:
					result={"status":False,"msg":str(e),"code":BellSchedulerManager.BELL_IMPORT_ERROR,"data":backup_file[1]}	
					return n4d.responses.build_successful_call_response(result)		
		

				holiday_token=os.path.join(unzip_tmp,os.path.basename(self.holiday_token))	

				if os.path.exists(holiday_token):
					action="enable"
					shutil.copyfile(holiday_token,self.holiday_token)	
				else:
					if os.path.exists(self.holiday_token):
						os.remove(self.holiday_token)

				if os.path.exists(os.path.join(unzip_tmp,"media/images")):
					if os.path.exists(self.images_folder):
						shutil.rmtree(self.images_folder)
					shutil.copytree(os.path.join(unzip_tmp,"media/images"),self.images_folder)

				if os.path.exists(os.path.join(unzip_tmp,"media/sounds")):
					if os.path.exists(self.sounds_folder):
						shutil.rmtree(self.sounds_folder)
					shutil.copytree(os.path.join(unzip_tmp,"media/sounds"),self.sounds_folder)
		
				update_holiday=self.enable_holiday_control(action).get('return',None)	
				if update_holiday["status"]:
					update_indicator=self.update_indicator_token().get('return',None)

					if update_indicator["status"]:
						result={"status":True,"msg":"Bells imported successfully","code":BellSchedulerManager.BELL_IMPORT_SUCCESSFUL,"data":backup_file[1]}
					else:
						result={"status":False,"msg":update_indicator["msg"],"code":BellSchedulerManager.BELL_IMPORT_ERROR,"data":backup_file[1]}	
				else:
					result={"status":False,"msg":update_holiday["msg"],"code":BellSchedulerManager.BELL_IMPORT_ERROR,"data":backup_file[1]}				
				
				return n4d.responses.build_successful_call_response(result)		
	
		except Exception as e:
			result={"status":False,"msg":str(e),"code":BellSchedulerManager.BELL_IMPORT_ERROR,"data":backup_file[1]}	
			return n4d.responses.build_successful_call_response(result)		

	#def import_bells_conf

	def enable_holiday_control(self,action):

		result=self._update_holiday_control(action)
		if result['status']:
			if action=="disable":
				if os.path.exists(self.holiday_token):
					os.remove(self.holiday_token)	
					result={"status":True,"msg":"Holiday token removed","code":BellSchedulerManager.HOLIDAY_DEACTIVATE_SUCCESSFUL,"data":""}
			else:
				if not os.path.exists(self.holiday_token):
					if not os.path.exists(self.config_dir):
						os.makedirs(self.config_dir)
					f=open(self.holiday_token,'w')
					f.close()
					result={"status":True,"msg":"Holiday token created","code":BellSchedulerManager.HOLIDAY_ACTIVATE_SUCCESSFUL,"data":""}		
		
		return n4d.responses.build_successful_call_response(result)		

	#def enable_holiday_control

	def _update_holiday_control(self,action):

		if os.path.exists(self.cron_file):
			f=open(self.cron_file)
			try:
				tasks_cron=json.load(f)
			except Exception as e:
				result={"status":False,"msg":str(e),"code":BellSchedulerManager.APPLY_CHANGES_DUETOCRON_ERROR,"data":""}
				return n4d.responses.build_successful_call_response(result)

			
			for item in	tasks_cron["BellScheduler"]:
				if action=="enable":
					tasks_cron["BellScheduler"][item]["holidays"]=True
				
				else:
					tasks_cron["BellScheduler"][item]["holidays"]=False

			
			self._write_conf(tasks_cron,"CronList")
			try:
				self.core.get_plugin('SchedulerClient').process_tasks(self.n4dkey)
				result={"status":True,"msg":"Cron file updated to use holiday manager","code":"","data":""}
			except Exception as e:
				print("BellSchedulerManager-SchedulerServer:_update_holiday_control.Error: "+str(e))
				result={"status":False,"msg":"Cron file dosn't exists","code":BellSchedulerManager.APPLY_CHANGES_DUETOCRON_ERROR,"data":""}			
			
		else:
			result={"status":False,"msg":"Cron file dosn't exists","code":BellSchedulerManager.APPLY_CHANGES_DUETOCRON_ERROR,"data":""}			

		return result

	#def _update_holiday_control		


	def update_indicator_token(self):


		if os.path.exists(self.cron_file):
			f=open(self.cron_file)
		
			try:
				tasks_cron=json.load(f)
				f.close()
			except Exception as e:
				result={"status":False,"msg":str(e),"code":BellSchedulerManager.APPLY_CHANGES_DUETOCRON_ERROR,"data":""}
				return n4d.responses.build_successful_call_response(result)

			for item in tasks_cron["BellScheduler"]:
				if not 'bellscheduler-token-management' in tasks_cron["BellScheduler"][item]["cmd"]:
					if 'mkdir -p' in tasks_cron["BellScheduler"][item]["cmd"]:
						write_token_command=self.cmd_create_token+tasks_cron["BellScheduler"][item]["BellId"]+" && "	
						tmp_cmd=write_token_command+tasks_cron["BellScheduler"][item]["cmd"].split("token &&")[1].split("rm -f")[0]+self.cmd_remove_token+tasks_cron["BellScheduler"][item]["BellId"]
						tasks_cron["BellScheduler"][item]["cmd"]=tmp_cmd
					else:	
						write_token_command=self.cmd_create_token+tasks_cron["BellScheduler"][item]["BellId"]+" && "
						tmp_cmd=write_token_command+tasks_cron["BellScheduler"][item]["cmd"]+";"+self.cmd_remove_token+tasks_cron["BellScheduler"][item]["BellId"]
						tasks_cron["BellScheduler"][item]["cmd"]=tmp_cmd

				
			self._write_conf(tasks_cron,"CronList")
			try:
				self.core.get_plugin('SchedulerClient').process_tasks(self.n4dkey)
				result={"status":True,"msg":"Cron file updated to use indicator","code":"","data":""}
			except Exception as e:
				print("BellSchedulerManager-SchedulerServer:update_indicator_token.Error: "+str(e))
				result={"status":False,"msg":"Cron file dosn't exists","code":BellSchedulerManager.APPLY_CHANGES_DUETOCRON_ERROR,"data":""}			
				
		else:
			result={"status":False,"msg":"Cron file dosn't exists","code":BellSchedulerManager.APPLY_CHANGES_DUETOCRON_ERROR,"data":""}			

		return n4d.responses.build_successful_call_response(result)
	
	#def update_indicator_control
	
	def stop_bell(self):
		
		cmd_kill=""
		bells_kill=""

		bells_pid=self._get_bells_pid()["data"]

		if len(bells_pid)>0:

			for item in bells_pid:	
				bells_kill=bells_kill+item+" "
				cmd_kill=cmd_kill+'kill ' +str(item)+";"
			
			bells_kill=bells_kill.strip()	
			os.system(cmd_kill)
			result={"status":True,"msg":"Alarm stoppped: "+bells_kill,"code":"","data":""}
			return n4d.responses.build_successful_call_response(result)	

	#def stop_bell 
			
	def _get_bells_pid(self):
	
		bells_pid=[]

		cmd='ps -ef | grep "ffplay -nodisp -autoexit" | grep -v "grep"'
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		output=p.communicate()[0]
		
		if type(output) is bytes:
			output=output.decode()

		lst=output.split("\n")
		lst.pop(0)
		
		if len(lst)>0:
			for item in lst:
				processed_line=item.split(" ")
				tmp_list=[]
				
				if len(processed_line) >= 10:
					for object in processed_line:
						if object!="":
							tmp_list.append(object)
					processed_line=tmp_list
					
					if str(processed_line[7])!='/bin/bash':
						bells_pid.append(processed_line[1])

		result={"status":True,"msg":"","code":"","data":bells_pid}
		return result	

	#def get_bells_pid
			

	def update_config_file(self,file=None):

		if file!=None:
			file=file
		else:
			file=self.config_file

		if os.path.exists(file):
			f=open(file,'r')
			filedata=f.read()
			filedata=filedata.replace('"option": "random"','"option": "directory"')
			f=open(file,'w')
			f.write(filedata)
			f.close()
		

	#def update_confif_file	
		

	def change_activation_status(self,action):

	
		bell_list=self.bells_config.copy()
		errors=0
			
		if action=="activate":
			msg_code_ok=BellSchedulerManager.CHANGE_ACTIVATION_STATUS_SUCCESSFUL
			msg_code_error=BellSchedulerManager.CHANGE_ACTIVATION_STATUS_ERROR
			for item in	bell_list:
				cont_days=0
				if not bell_list[item]["active"]:
					for day in bell_list[item]["weekdays"]:
						if bell_list[item]["weekdays"][day]:
							cont_days+=1
					if cont_days>0:			
						tasks_for_cron=self._format_to_cron(bell_list,str(item),"active")
						#Old n4d:result=self.n4d.write_tasks(self.n4dkey,'SchedulerServer','local',tasks_for_cron)
						try:
							result=self.core.get_plugin('SchedulerServer').write_tasks('local',tasks_for_cron)
						except Exception as e:
							print("BellSchedulerManager-SchedulerServer: change_activation_status.Error: "+str(e))
							result={'status':-1}
								

						if result.get('status',None)==0:
							bell_list[item]["active"]=True
						else:
							errors+=1
							break
							
		else:
			msg_code_ok=BellSchedulerManager.CHANGE_DEACTIVATION_STATUS_SUCCESSFUL
			msg_code_error=BellSchedulerManager.CHANGE_DEACTIVATION_STATUS_ERROR
			for item in	bell_list:
				if bell_list[item]["active"]:
					result=self._delete_from_cron(item)
					if result.get('status',None)==0:
						bell_list[item]["active"]=False
					else:
						errors+=1
						break

		if errors==0:
			self._write_conf(bell_list,"BellList")
			result_change={"status":True,"msg":"Activation/Deactivation successfully","code":msg_code_ok,"data":""}

		else:
			result_change={"status":False,"msg":"Activation/Deactivation failled","code":msg_code_error,"data":result.get('return',None)}			

		return n4d.responses.build_successful_call_response(result_change)	

	#def change_activation_state
	

	def remove_all_bells(self):

		bell_list=self.bells_config.copy()

		errors=0

		for item in	self.bells_config:
			if self.bells_config[item]["active"]:
				result=self._delete_from_cron(item)
				if result.get('status',None)==0:
						bell_list.pop(item)
				else:
					errors+=1
					break
			else:
				bell_list.pop(item)		

		if errors==0:			
			self._write_conf(bell_list,"BellList")
			result_remove={"status":True,"msg":"Removed all bells","code":BellSchedulerManager.REMOVE_ALL_BELLS_SUCCESSFUL,"data":""}

		else:
			result_remove={"status":False,"msg":"Removed all bells_failed","code":BellSchedulerManager.REMOVE_ALL_BELLS_ERROR,"data":result}

		return n4d.responses.build_successful_call_response(result_remove)

	#def remove_all_bells	

#def BellSchedulerManager
	
