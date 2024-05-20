 
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
	AUDIO_DEVICE_CONFIG_CHANGED_ERROR=-53

	READ_CONF_FILE_SUCCESSFUL=0
	BELL_EXPORT_SUCCESSFUL=11
	BELL_IMPORT_SUCCESSFUL=10
	HOLIDAY_DEACTIVATE_SUCCESSFUL=34
	HOLIDAY_ACTIVATE_SUCCESSFUL=35
	CHANGE_ACTIVATION_STATUS_SUCCESSFUL=46
	CHANGE_DEACTIVATION_STATUS_SUCCESSFUL=47
	REMOVE_ALL_BELLS_SUCCESSFUL=51
	AUDIO_DEVICE_CONFIG_READED=52
	AUDIO_DEVICE_CONFIG_CHANGED_SUCCCESS=53

	def __init__(self):

		self.config_dir=os.path.expanduser("/etc/bellScheduler/")
		self.config_file=self.config_dir+"bell_list"
		self.holiday_token=self.config_dir+"enabled_holiday_token"
		self.images_folder="/usr/local/share/bellScheduler/images"
		self.sounds_folder="/usr/local/share/bellScheduler/sounds"
		self.media_files_folder="/usr/local/share/bellScheduler/"
		self.bell_scheduler_player_log="/var/log/BELL-SCHEDULER-PLAYER.log"
	
		self.indicator_token_folder="/tmp/.BellScheduler"
		self.indicator_token_path=os.path.join(self.indicator_token_folder,"bellscheduler-token")
		self.cmd_create_token='bellscheduler-token-management create_token '
		self.cmd_remove_token='bellscheduler-token-management remove_token '
		self.audiodevice_config_file=self.config_dir+"audio_device"

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
			result={"status":False,"msg":"Unabled to read configuration file :" +str(e),"code":BellSchedulerManager.READ_CONF_FILE_ERROR,"data":self.bells_config}

		f.close()	

		return n4d.responses.build_successful_call_response(result)

	#def read_conf	

	def _get_tasks_from_cron(self):

		cron_tasks=[]
		
		try:
			if os.path.exists(self.cron_file):
				with open(self.cron_file,'r') as fd:
					content=fd.readlines()

				for line in content:
					if not line.startswith("#"):
						key=line.strip().split(" ")[-1]
						cron_tasks.append(key)

		except Exception as e:
			print("BellSchedulerManager:_get_tasks_from_cron.Error: "+str(e))
			pass
		
		return cron_tasks

	#def _get_tasks_from_cron	
		
	def sync_with_cron(self):
	
		bell_tasks=self.read_conf().get('return',None).get('data',None)
		keys_bells=bell_tasks.keys()
		bells_incron=[]
		keys_cron=[]
		try:
			bells_incron=self._get_tasks_from_cron()
		except:
			pass
		changes=0

		if len(bells_incron)>0:
			for item in bell_tasks:
				if item in bells_incron:
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

			for item in bells_incron:
				if item not in keys_bells:
					result=self._delete_from_cron(item)
					if result.get('status',None)!=0:
						tmp_result={"status":False,"msg":"Unable to clear alarm from cron file","code":BellSchedulerManager.CRON_SYNC_PROBLEMS_ERROR,"data":""}
						return n4d.responses.build_successful_call_response(tmp_result)
	
		else:
			for item in bell_tasks:
				if bell_tasks[item]["active"]:
					changes+=1
					bell_tasks[item]["active"]=False
					

		if changes>0:
			self._write_conf(bell_tasks,"BellList")

		tmp_result={"status":True,"msg":"Sync with cron sucessfully","code":"","data":bell_tasks}	
		return n4d.responses.build_successful_call_response(tmp_result)
				
	#def sync_with_cron	

	def _write_conf(self,info,type_list):
		
		if type_list=="BellList":
			self.bells_config=info
			file_to_write=self.config_file
			msg="Bell list saved successfuly"
		
		with codecs.open(file_to_write,'w',encoding="utf-8") as f:
			json.dump(info,f,ensure_ascii=False)
			f.close()	

		result={"status":True,"msg":msg}
		return n4d.responses.build_successful_call_response(result)


	#def _write_conf	

	def save_changes(self,info,last_change,action):

		turn_on=False
		if action !="remove":
			if info[last_change]["active"]:
				turn_on=True
				tasks_for_cron=self._format_to_cron(info,last_change,action)
				result=self._add_to_cron(tasks_for_cron)
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
				if last_change in cron_tasks:
					return {"status":True, "id":last_change}
		except Exception as e:
			print("BellSchedulerManager:_get_cron_id.Error:"+str(e))
			return {"status":False,"id":""}
		
		return {"status":False,"id":0}

	# def _get_cron_id

	def _add_to_cron(self,task):

		try:
			new_task="%s %s %s %s %s %s %s\n"%(task["minute"],task["hour"],task["validity"]["dom"],task["validity"]["mon"],task["days"]["dow"],task["cmd"],task["id"])

			if os.path.exists(self.cron_file):
				with open(self.cron_file,'r') as fd:
					content=fd.readlines()

				match=False
				new_content=[]
				for line in content:
					key=line.strip().split(" ")[-1]
					if key==task["id"]:
						line=new_task
						match=True
					new_content.append(line)
				if not match:
					new_content.append(new_task)

				with open(self.cron_file,'w') as fd:
					for line in new_content:
						fd.write(line)
			else:
				with open(self.cron_file,'a') as fd:
					fd.write(new_task)
			
			result={"status":0,"msg":""}
		except Exception as e:
			print("BellSchedulerManager:_add_to_cron.Error:"+str(e))
			result={"status":-1,"msg":str(e)}

		return result

	#def _add_to_cron	
	
	def _delete_from_cron(self,last_change):

		id_to_remove=self._get_cron_id(last_change)
		if id_to_remove["status"]:
			cron_id=id_to_remove["id"]
			delete={"status":0,"data":"0","msg":""}
			try:
				if os.path.exists(self.cron_file):
					with open(self.cron_file,'r') as fd:
						content=fd.readlines()
				tmpLines=[]
				for line in content:
					key=line.strip().split(" ")[-1]
					if key!=last_change:
						tmpLines.append(line)

				with open(self.cron_file,'w') as fd:
					for line in tmpLines:
						fd.write(line)

			except Exception as e:
				print("BellSchedulerManager:_delete_from_cron.Error:"+str(e))
				delete={"status":-1,"data":"0","msg":str(e)}
				pass
		
		else:
			delete={"status":-1,"data":"0","msg":""}

		return delete

	#def _delete_from_cron	
	
	def _format_to_cron(self,info,item,action):

		info_to_cron={}
		holiday_cmd="/usr/bin/check_holidays.py"
		bell_cmd="/usr/bin/BellSchedulerPlayer"

		try:
			info_to_cron["validity"]={}
			if info[item]["validity"]["active"]:
				bell_validity=info[item]["validity"]["value"]
				if bell_validity!="":
					if "-" in bell_validity:
						tmpRange=bell_validity.split("-")
						tmpday1=tmpRange[0].split("/")[0]
						if tmpday1.startswith("0"):
							tmpday1=tmpday1[1:]

						tmpmonth1=tmpRange[0].split("/")[1]
						if tmpmonth1.startswith("0"):
							tmpmonth1=tmpmonth1[1:]

						tmpday2=tmpRange[1].split("/")[0]
						if tmpday2.startswith("0"):
							tmpday2=tmpday2[1:]

						tmpmonth2=tmpRange[1].split("/")[1]
						if tmpmonth2.startswith("0"):
							tmpmonth2=tmpmonth2[1:]
						
						if tmpmonth1==tmpmonth2:
							info_to_cron["validity"]["dom"]="%s-%s"%(tmpday1,tmpday2)
							info_to_cron["validity"]["mon"]="%s"%(tmpmonth1) 
						else:
							info_to_cron["validity"]["dom"]="*"
							info_to_cron["validity"]["mon"]="%s-%s"%(tmpmonth1,tmpmonth2) 
						
					else:
						tmpday=bell_validity.split("/")[0]
						if tmpday.startswith("0"):
							tmpday=tmpday[1:]
						tmpmonth=bell_validity.split("/")[1]
						if tmpmonth.startswith("0"):
							tmpmonth=tmpmonth[1:]
						info_to_cron["validity"]["dom"]="%s"%tmpday
						info_to_cron["validity"]["mon"]="%s"%tmpmonth
				else:
					info_to_cron["validity"]["dom"]="*"
					info_to_cron["validity"]["mon"]="*" 
			else:
				info_to_cron["validity"]["dom"]="*"
				info_to_cron["validity"]["mon"]="*" 
		except:
			info_to_cron["validity"]["dom"]="*"
			info_to_cron["validity"]["mon"]="*" 

		info_to_cron["hour"]=str(info[item]["hour"])
		info_to_cron["minute"]=str(info[item]["minute"])

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
			info_to_cron["days"]={}
			info_to_cron["days"]["dow"]=days
			info_to_cron["id"]=item				

			if os.path.exists(self.holiday_token):
				cmd="root %s && %s"%(holiday_cmd,bell_cmd)
			else:
				cmd="root %s"%(bell_cmd)
			
			info_to_cron["cmd"]=cmd
		
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

			if os.path.exists(self.holiday_token):
				shutil.copy2(self.holiday_token,os.path.join(tmp_export,os.path.basename(self.holiday_token)))

			if os.path.exists(self.media_files_folder):
				shutil.copytree(self.media_files_folder,os.path.join(tmp_export,"media"))

			if os.path.exists(self.bell_scheduler_player_log):
				shutil.copy2(self.bell_scheduler_player_log,os.path.join(tmp_export,os.path.basename(self.bell_scheduler_player_log)))
		
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
				
				if not update_holiday["status"]:
					result={"status":False,"msg":update_holiday["msg"],"code":BellSchedulerManager.BELL_IMPORT_ERROR,"data":backup_file[1]}				

				else:
					result={"status":True,"msg":"Bells imported successfully","code":BellSchedulerManager.BELL_IMPORT_SUCCESSFUL,"data":""}
		
				return n4d.responses.build_successful_call_response(result)		
	
		except Exception as e:
			result={"status":False,"msg":str(e),"code":BellSchedulerManager.BELL_IMPORT_ERROR,"data":backup_file[1]}	
			return n4d.responses.build_successful_call_response(result)		

	#def import_bells_conf

	def enable_holiday_control(self,action):

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

		result_cron=self._update_holiday_control(action)
		if result_cron["status"]:
			return n4d.responses.build_successful_call_response(result)	
		else:
			return n4d.response.build_successfull_call_response(result_cron)			

	#def enable_holiday_control

	def _update_holiday_control(self,action):

		bell_list=self.read_conf().get('return',None).get('data',None)
		errors=0

		for item in bell_list:
			cont_days=0
			if bell_list[item]["active"]:
				tasks_for_cron=self._format_to_cron(bell_list,str(item),"active")
				result=self._add_to_cron(tasks_for_cron)
				if result.get('status',None)==-1:
					errors+=1
					break
		if errors==0:
			result={"status":True,"msg":"Cron file updated to use holiday manager","code":"","data":""}
		else:
			result={"status":False,"msg":" Unable to update cron file to user holiday manager","code":BellSchedulerManager.APPLY_CHANGES_DUETOCRON_ERROR,"data":""}			

		return result

	#def _update_holiday_control		

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

		cmd="ps -ef | grep 'ffplay -nodisp -autoexit' | grep -v '/bin/bash' |grep -v 'grep' |egrep ' ' | awk '{print $2}' "
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		output=p.communicate()[0]
		
		if type(output) is bytes:
			output=output.decode()

		lst=output.split("\n")
		lst=lst[:-1]
		
		if len(lst)>0:
			for item in lst:
				bells_pid.append(item)
	
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
						result=self._add_to_cron(tasks_for_cron)

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

	def read_audio_device_config(self):

		audio_device_config=""
		if os.path.exists(self.audiodevice_config_file):
			with open(self.audiodevice_config_file,'r') as fd:
				audio_device_config=fd.readline()

		result={"status":True,msg:"Current audio device config readed","code":BellSchedulerManager.AUDIO_DEVICE_CONFIG_READED,"data":audio_device_config}

		return n4d.responses.build_successful_call_response(result)

	#def read_audio_device_config

	def write_audio_device_config(self,data):

		try:
			if data!="":
				with open(self.audiodevice_config_file,'w') as fd:
					fd.write("%sdata\n"%(data))
			else:
				if os.path.exists(self.audiodevice_config_file):
					os.remove(self.audiodevice_config_file)
		
			result={"status":True,msg:"Audio device changed successfully","code":BellSchedulerManager.AUDIO_DEVICE_CONFIG_CHANGED_SUCCCESS,"data":""}

		except Exception as e:
			result={"status":False,msg:"Audio device changed error","code":BellSchedulerManager.AUDIO_DEVICE_CONFIG_CHANGED_ERROR,"data":str(e)}

		return n4d.responses.build_successful_call_response(result)

#def BellSchedulerManager
	
