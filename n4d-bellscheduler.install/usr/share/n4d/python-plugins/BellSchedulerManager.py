import os
import subprocess
import json
import shutil
import tempfile
import zipfile
import syslog
import n4d.server.core as n4dcore
import n4d.responses

class BellSchedulerManager:

    READ_CONF_FILE_ERROR = -25
    CRON_SYNC_PROBLEMS_ERROR = -37
    BELL_EDIT_ERROR = -19
    BELL_CREATE_ERROR = -20
    BELL_DELETE_ERROR = -21
    BELL_ACTIVATE_ERROR = -22
    BELL_DEACTIVATE_ERROR = -23
    COPY_MEDIA_FILES_ERROR = -24
    BELL_EXPORT_ERROR = -12
    BELL_IMPORT_ERROR = -9
    APPLY_CHANGES_DUETOCRON_ERROR = -36
    BELL_LIST_LOADED_DUETOCRON_ERROR = -37
    CHANGE_ACTIVATION_STATUS_ERROR = -48
    CHANGE_DEACTIVATION_STATUS_ERROR = -49
    REMOVE_ALL_BELLS_ERROR = -52
    AUDIO_DEVICE_CONFIG_CHANGED_ERROR = -53

    READ_CONF_FILE_SUCCESSFUL = 0
    BELL_EXPORT_SUCCESSFUL = 11
    BELL_IMPORT_SUCCESSFUL = 10
    HOLIDAY_DEACTIVATE_SUCCESSFUL = 34
    HOLIDAY_ACTIVATE_SUCCESSFUL = 35
    CHANGE_ACTIVATION_STATUS_SUCCESSFUL = 46
    CHANGE_DEACTIVATION_STATUS_SUCCESSFUL = 47
    REMOVE_ALL_BELLS_SUCCESSFUL = 51
    AUDIO_DEVICE_CONFIG_READED = 52
    AUDIO_DEVICE_CONFIG_CHANGED_SUCCCESS = 58

    def __init__(self):

        self.config_dir = os.path.expanduser("/etc/bellScheduler/")
        self.config_file = os.path.join(self.config_dir, "bell_list")
        self.holiday_token = os.path.join(self.config_dir, "enabled_holiday_token")
        self.images_folder = "/usr/local/share/bellScheduler/images"
        self.sounds_folder = "/usr/local/share/bellScheduler/sounds"
        self.media_files_folder = "/usr/local/share/bellScheduler/"
        self.bell_scheduler_player_log = "/var/log/BELL-SCHEDULER-PLAYER.log"
        self.n4d_bell_scheduler_manager_log = "/var/log/N4D-BELLSCHEDULER-MANAGER.log"
        self.indicator_token_folder = "/tmp/.BellScheduler"
        self.indicator_token_path = os.path.join(self.indicator_token_folder, "bellscheduler-token")
        self.cmd_create_token = 'bellscheduler-token-management create_token '
        self.cmd_remove_token = 'bellscheduler-token-management remove_token '
        self.audiodevice_config_file = os.path.join(self.config_dir, "audio_device")
        self.cron_file = "/etc/cron.d/localBellScheduler"

        self._get_n4d_key()
        self.core = n4dcore.Core.get_core()

    #def __init__

    def _log_error(self, method_name, exception):

        error_msg = f"BellSchedulerManager:{method_name}.Error: {str(exception)}"
        syslog.openlog("N4D-BELLSCHEDULER-MANAGER")
        syslog.syslog(syslog.LOG_ERR, error_msg)

    #def _log_error

    def _get_n4d_key(self):

        try:
            with open('/etc/n4d/key', 'r', encoding='utf-8') as file_data:
                self.n4dkey = file_data.readlines()[0].strip()
        except Exception as e:
            self._log_error("_get_n4d_key", e)
            self.n4dkey = ''

    #def _get_n4d_key

    def _create_dirs(self):

        os.makedirs(self.images_folder, exist_ok=True)
        os.makedirs(self.sounds_folder, exist_ok=True)

    #def _create_dirs

    def _create_conf(self):

        os.makedirs(self.config_dir, exist_ok=True)

        try:
            with open(self.config_file, 'w', encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False)
            
            return {"status": True, "msg": "Configuration file created successfully", "code": "", "data": ""}
        
        except Exception as e:
            self._log_error("_create_conf", e)
            return {"status": False, "msg": str(e), "code": "", "data": ""}

    #def _create_conf

    def read_conf(self):

        self._create_dirs()

        if not os.path.exists(self.config_file):
            self._create_conf()

        self.bells_config = {}

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.bells_config = json.load(f)
           
            result = {"status": True, "msg": "Configuration file read successfully", "code": self.READ_CONF_FILE_SUCCESSFUL, "data": self.bells_config}
        
        except Exception as e:
            self._log_error("read_conf", e)
            result = {"status": False, "msg": f"Unable to read configuration file: {str(e)}", "code": self.READ_CONF_FILE_ERROR, "data": self.bells_config}

        return n4d.responses.build_successful_call_response(result)

    #def read_conf

    def _get_tasks_from_cron(self):

        if not os.path.exists(self.cron_file):
            return []
        try:
            with open(self.cron_file, 'r', encoding='utf-8') as fd:
                return [line.strip().split()[-1] for line in fd if line.strip() and not line.strip().startswith("#")]
        except Exception as e:
            self._log_error("_get_tasks_from_cron", e)
            return []

    #def _get_tasks_from_cron

    def sync_with_cron(self):

        bell_tasks = self.read_conf().get('return', {}).get('data', {})

        if not bell_tasks:
            bell_tasks = {}

        bells_incron = set(self._get_tasks_from_cron())
        changes = 0

        for item, task_data in bell_tasks.items():
            in_cron = item in bells_incron
            if task_data.get("active") != in_cron:
                task_data["active"] = in_cron
                changes += 1

        for item in bells_incron:
            if item not in bell_tasks:
                result = self._delete_from_cron(item)
                if result.get('status') != 0:
                    return n4d.responses.build_successful_call_response({
                        "status": False, "msg": "Unable to clear alarm from cron file", "code": self.CRON_SYNC_PROBLEMS_ERROR, "data": ""
                    })

        if changes > 0:
            self._write_conf(bell_tasks, "BellList")

        return n4d.responses.build_successful_call_response({"status": True, "msg": "Sync with cron successfully", "code": "", "data": bell_tasks})

    #def sync_with_cron

    def _write_conf(self, info, type_list):

        if type_list == "BellList":
            self.bells_config = info

        try:
            with open(self.config_file, 'w', encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False)

            return n4d.responses.build_successful_call_response({"status": True, "msg": "Bell list saved successfully"})
       
        except Exception as e:
            self._log_error("_write_conf", e)
            return n4d.responses.build_successful_call_response({"status": False, "msg": str(e)})

    #def _write_conf

    def save_changes(self, info, last_change, action):

        turn_on = False

        if action != "remove" and info.get(last_change, {}).get("active"):
            turn_on = True
            tasks_for_cron = self._format_to_cron(info, last_change, action)
            result = self._add_to_cron(tasks_for_cron)
        else:
            result = self._delete_from_cron(last_change)

        if result.get('status') == 0:
            return self._write_conf(info, "BellList")

        error_mapping = {
            "edit": self.BELL_EDIT_ERROR,
            "add": self.BELL_CREATE_ERROR,
            "remove": self.BELL_DELETE_ERROR,
            "active": self.BELL_ACTIVATE_ERROR if turn_on else self.BELL_DEACTIVATE_ERROR
        }

        tmp_result = {
            "status": False,
            "action": action,
            "msg": result.get('msg', 'Error processing changes'),
            "code": error_mapping.get(action, -1),
            "data": ""
        }

        return n4d.responses.build_successful_call_response(tmp_result)

    #def save_changes

    def _get_cron_id(self, last_change):

        return {"status": True, "id": last_change} if last_change in self._get_tasks_from_cron() else {"status": True, "id": 0}

    #def _get_cron_id

    def _add_to_cron(self, task):

        try:
            new_task = f"{task['minute']} {task['hour']} {task['validity']['dom']} {task['validity']['mon']} {task['days']['dow']} {task['cmd']} {task['id']}\n"
            content = []
            if os.path.exists(self.cron_file):
                with open(self.cron_file, 'r', encoding='utf-8') as fd:
                    content = fd.readlines()

            match = False
            new_content = []

            for line in content:
                if line.strip() and line.strip().split()[-1] == task["id"]:
                    line = new_task
                    match = True
                new_content.append(line)

            if not match:
                new_content.append(new_task)

            with open(self.cron_file, 'w', encoding='utf-8') as fd:
                fd.writelines(new_content)

            return {"status": 0, "msg": ""}

        except Exception as e:
            self._log_error("_add_to_cron", e)
            return {"status": -1, "msg": str(e)}

    #def _add_to_cron

    def _delete_from_cron(self, last_change):

        if not os.path.exists(self.cron_file):
            return {"status": 0, "data": "0", "msg": ""}

        try:
            with open(self.cron_file, 'r', encoding='utf-8') as fd:
                content = fd.readlines()

            tmp_lines = [line for line in content if not line.strip() or line.strip().split()[-1] != last_change]

            with open(self.cron_file, 'w', encoding='utf-8') as fd:
                fd.writelines(tmp_lines)

            return {"status": 0, "data": "0", "msg": ""}

        except Exception as e:
            self._log_error("_delete_from_cron", e)
            return {"status": -1, "data": "0", "msg": str(e)}


    #def _delete_from_cron
   
    def _clean_date_padding(self, date_str):

        return str(int(date_str)) if date_str.isdigit() else date_str

    #def _clean_date_padding

    def _format_to_cron(self, info, item, action):

        info_to_cron = {"validity": {"dom": "*", "mon": "*"}}
        holiday_cmd = "/usr/bin/check_holidays.py"
        bell_cmd = "exec /usr/bin/BellSchedulerPlayer"

        try:
            bell_validity = info[item].get("validity", {}).get("value", "")

            if info[item].get("validity", {}).get("active") and bell_validity:
                if "-" in bell_validity:
                    start, end = bell_validity.split("-")
                    d1_parts = start.split("/")[:2]
                    d2_parts = end.split("/")[:2]

                    if len(d1_parts) == 2 and len(d2_parts) == 2:
                        d1_raw, m1_raw = d1_parts
                        d2_raw, m2_raw = d2_parts

                        d1 = self._clean_date_padding(d1_raw)
                        m1 = self._clean_date_padding(m1_raw)
                        d2 = self._clean_date_padding(d2_raw)
                        m2 = self._clean_date_padding(m2_raw)

                        if m1 == m2:
                            info_to_cron["validity"]["dom"] = f"{d1}-{d2}"
                            info_to_cron["validity"]["mon"] = m1
                        else:
                            info_to_cron["validity"]["dom"] = "*"
                            info_to_cron["validity"]["mon"] = f"{m1}-{m2}"

                else:
                    parts = bell_validity.split("/")[:2]
                    
                    if len(parts) == 2:
                        d_raw, m_raw = parts
                        d = self._clean_date_padding(d_raw)
                        m = self._clean_date_padding(m_raw)
                        info_to_cron["validity"]["dom"] = d
                        info_to_cron["validity"]["mon"] = m
        
        except Exception as e:
            self._log_error("_format_to_cron_validity_parse", e)
            info_to_cron["validity"] = {"dom": "*", "mon": "*"}

        info_to_cron["hour"] = str(info[item]["hour"])
        info_to_cron["minute"] = str(info[item]["minute"])

        weekdays = info[item].get("weekdays", {})
        active_days = [str(int(day_idx) + 1) for day_idx, is_active in weekdays.items() if is_active]
        info_to_cron["days"] = {"dow": ",".join(active_days)}
        info_to_cron["id"] = item

        info_to_cron["cmd"] = f"root {holiday_cmd} && {bell_cmd}" if os.path.exists(self.holiday_token) else f"root {bell_cmd}"

        return info_to_cron

    #def _format_to_cron

    def copy_media_files(self, image, sound):

        self._create_dirs()

        try:
            if image:
                imageToCopy=os.path.join(self.images_folder, os.path.basename(image))
                if not os.path.exists(imageToCopy):
                    shutil.copy2(image, imageToCopy)
            if sound:
                soundToCopy=os.path.join(self.sounds_folder, os.path.basename(sound))
                if not os.path.exists(soundToCopy):
                    shutil.copy2(sound, soundToCopy)
            
            return n4d.responses.build_successful_call_response({"status": True, "msg": "Files copied successfully", "code": "", "data": ""})
        
        except Exception as e:
            self._log_error("copy_media_files", e)
            return n4d.responses.build_successful_call_response({"status": False, "msg": str(e), "code": self.COPY_MEDIA_FILES_ERROR, "data": ""})

    #def copy_media_files

    def export_bells_conf(self, dest_file, user, arg=None):

        tmp_export = tempfile.mkdtemp("_bell_export")
        self._create_dirs()

        try:
            if os.path.exists(self.config_file):
                shutil.copy2(self.config_file, os.path.join(tmp_export, os.path.basename(self.config_file)))
            if os.path.exists(self.holiday_token):
                shutil.copy2(self.holiday_token, os.path.join(tmp_export, os.path.basename(self.holiday_token)))
            if os.path.exists(self.media_files_folder):
                shutil.copytree(self.media_files_folder, os.path.join(tmp_export, "media"), dirs_exist_ok=True)
            for log_file in [self.bell_scheduler_player_log, self.n4d_bell_scheduler_manager_log]:
                if os.path.exists(log_file):
                    shutil.copy2(log_file, os.path.join(tmp_export, os.path.basename(log_file)))

            dest_file_base = os.path.splitext(dest_file)[0]
            shutil.make_archive(dest_file_base, 'zip', tmp_export)

            if arg != True:
                shutil.rmtree(tmp_export)

            zip_full_path = f"{dest_file_base}.zip"
            subprocess.run(["chown", "-R", f"{user}:{user}", zip_full_path], check=True)

            return n4d.responses.build_successful_call_response({"status": True, "msg": "Bells exported successfully", "code": self.BELL_EXPORT_SUCCESSFUL, "data": ""})
        
        except Exception as e:
            self._log_error("export_bells_conf", e)
            return n4d.responses.build_successful_call_response({"status": False, "msg": str(e), "code": self.BELL_EXPORT_ERROR, "data": ""})

    #def export_bells_conf
    
    def import_bells_conf(self, orig_file, user, backup):

        backup_file_path = ""
        unzip_tmp = tempfile.mkdtemp("_import_bells")
        action = "disable"

        if backup:
            _, backup_file_path = tempfile.mkstemp("_bells_backup")
            export_res = self.export_bells_conf(backup_file_path, user, True).get('return', {})
            
            if not export_res.get('status'):
                return n4d.responses.build_successful_call_response(export_res)

        try:
            with zipfile.ZipFile(orig_file, 'r') as tmp_zip:
                tmp_zip.extractall(unzip_tmp)

            config_file_tmp = os.path.join(unzip_tmp, os.path.basename(self.config_file))
            try:
                with open(config_file_tmp, 'r', encoding='utf-8') as f_config:
                    json.load(f_config)
                self.update_config_file(config_file_tmp)
                shutil.copy2(config_file_tmp, self.config_dir)

            except Exception as e:
                self._log_error("import_bells_conf_json_parse", e)
                return n4d.responses.build_successful_call_response({"status": False, "msg": str(e), "code": self.BELL_IMPORT_ERROR, "data": backup_file_path})

            holiday_token_tmp = os.path.join(unzip_tmp, os.path.basename(self.holiday_token))
            if os.path.exists(holiday_token_tmp):
                action = "enable"
                shutil.copyfile(holiday_token_tmp, self.holiday_token)
            elif os.path.exists(self.holiday_token):
                os.remove(self.holiday_token)

            media_img_tmp = os.path.join(unzip_tmp, "media/images")
            if os.path.exists(media_img_tmp):
                shutil.rmtree(self.images_folder, ignore_errors=True)
                shutil.copytree(media_img_tmp, self.images_folder, dirs_exist_ok=True)

            media_snd_tmp = os.path.join(unzip_tmp, "media/sounds")
            if os.path.exists(media_snd_tmp):
                shutil.rmtree(self.sounds_folder, ignore_errors=True)
                shutil.copytree(media_snd_tmp, self.sounds_folder, dirs_exist_ok=True)

            if os.path.exists(self.cron_file):
                os.remove(self.cron_file)

            update_holiday = self.enable_holiday_control(action).get('return', {})
            if not update_holiday.get("status"):
                return n4d.responses.build_successful_call_response({"status": False, "msg": update_holiday.get("msg"), "code": self.BELL_IMPORT_ERROR, "data": backup_file_path})

            return n4d.responses.build_successful_call_response({"status": True, "msg": "Bells imported successfully", "code": self.BELL_IMPORT_SUCCESSFUL, "data": ""})
        
        except Exception as e:
            self._log_error("import_bells_conf", e)
            return n4d.responses.build_successful_call_response({"status": False, "msg": str(e), "code": self.BELL_IMPORT_ERROR, "data": backup_file_path})

    #def import_bells_conf

    def enable_holiday_control(self, action):

        if action == "disable":
            if os.path.exists(self.holiday_token):
                os.remove(self.holiday_token)
            result = {"status": True, "msg": "Holiday token removed", "code": self.HOLIDAY_DEACTIVATE_SUCCESSFUL, "data": ""}
        else:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.holiday_token, 'w', encoding='utf-8') as f:
                pass
            result = {"status": True, "msg": "Holiday token created", "code": self.HOLIDAY_ACTIVATE_SUCCESSFUL, "data": ""}

        result_cron = self._update_holiday_control(action)
        
        return n4d.responses.build_successful_call_response(result if result_cron["status"] else result_cron)

    #def enable_holiday_control

    def _update_holiday_control(self, action):

        bell_list = self.read_conf().get('return', {}).get('data', {}) or {}
        errors = 0

        for item in bell_list:
            if bell_list[item].get("active"):
                tasks_for_cron = self._format_to_cron(bell_list, str(item), "active")
                if self._add_to_cron(tasks_for_cron).get('status') == -1:
                    errors += 1
                    break
        
        if errors == 0:
            return {"status": True, "msg": "Cron file updated to use holiday manager", "code": "", "data": ""}
        
        return {"status": False, "msg": "Unable to update cron file to use holiday manager", "code": self.APPLY_CHANGES_DUETOCRON_ERROR, "data": ""}

    #def _update_holiday_control

    def stop_bell(self):

        try:
            subprocess.run(["pkill", "-f", "ffplay -nodisp -autoexit -loglevel error -ss"], check=True)
            result = {"status": True, "msg": "Alarm stopped", "code": "", "data": ""}
        
        except subprocess.CalledProcessError:
            result = {"status": True, "msg": "No active alarm process found to stop", "code": "", "data": ""}
        
        except Exception as e:
            self._log_error("stop_bell", e)
            result = {"status": False, "msg": str(e), "code": "", "data": ""}
        
        return n4d.responses.build_successful_call_response(result)

    #def stop_bell

    def update_config_file(self, file=None):

        target_file = file if file else self.config_file

        if os.path.exists(target_file):
            try:
                with open(target_file, 'r', encoding='utf-8') as f:
                    filedata = f.read()
                filedata = filedata.replace('"option": "random"', '"option": "directory"')
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(filedata)
            
            except Exception as e:
                self._log_error("update_config_file", e)

    #def update_config_file

    def change_activation_status(self, action):

        bell_list = self.bells_config.copy()
        errors = 0

        if action == "activate":
            msg_code_ok = self.CHANGE_ACTIVATION_STATUS_SUCCESSFUL
            msg_code_error = self.CHANGE_ACTIVATION_STATUS_ERROR
            for item in bell_list:
                if not bell_list[item].get("active"):
                    if any(bell_list[item].get("weekdays", {}).values()):
                        tasks_for_cron = self._format_to_cron(bell_list, str(item), "active")
                        if self._add_to_cron(tasks_for_cron).get('status') == 0:
                            bell_list[item]["active"] = True
                        else:
                            errors += 1
                            break
        else:
            msg_code_ok = self.CHANGE_DEACTIVATION_STATUS_SUCCESSFUL
            msg_code_error = self.CHANGE_DEACTIVATION_STATUS_ERROR
            for item in bell_list:
                if bell_list[item].get("active"):
                    if self._delete_from_cron(item).get('status') == 0:
                        bell_list[item]["active"] = False
                    else:
                        errors += 1
                        break

        if errors == 0:
            self._write_conf(bell_list, "BellList")
            result_change = {"status": True, "msg": "Activation/Deactivation processed successfully", "code": msg_code_ok, "data": ""}
        else:
            result_change = {"status": False, "msg": "Activation/Deactivation failed", "code": msg_code_error, "data": ""}
        
        return n4d.responses.build_successful_call_response(result_change)

    #def change_activation_status

    def remove_all_bells(self):

        bell_list = self.bells_config.copy()
        errors = 0
        
        for item in list(self.bells_config.keys()):
            if self.bells_config[item].get("active"):
                if self._delete_from_cron(item).get('status') == 0:
                    bell_list.pop(item, None)
                else:
                    errors += 1
                    break
            else:
                bell_list.pop(item, None)

        if errors == 0:
            self._write_conf(bell_list, "BellList")
            result_remove = {"status": True, "msg": "Removed all bells successfully", "code": self.REMOVE_ALL_BELLS_SUCCESSFUL, "data": ""}
        else:
            result_remove = {"status": False, "msg": "Removing all bells failed", "code": self.REMOVE_ALL_BELLS_ERROR, "data": ""}
        
        return n4d.responses.build_successful_call_response(result_remove)

    #def remove_all_bells

    def read_audio_device_config(self):

        audio_device_config = ""

        if os.path.exists(self.audiodevice_config_file):
            try:
                with open(self.audiodevice_config_file, 'r', encoding='utf-8') as fd:
                    audio_device_config = fd.readline().strip()
            except Exception as e:
                self._log_error("read_audio_device_config", e)

        result = {"status": True, "msg": "Current audio device config read successfully", "code": self.AUDIO_DEVICE_CONFIG_READED, "data": audio_device_config}
       
        return n4d.responses.build_successful_call_response(result)

    #def read_audio_device_config

    def write_audio_device_config(self, data):

        try:
            if data:
                with open(self.audiodevice_config_file, 'w', encoding='utf-8') as fd:
                    fd.write(f"{data}\n")
            elif os.path.exists(self.audiodevice_config_file):
                os.remove(self.audiodevice_config_file)
            
            result = {"status": True, "msg": "Audio device changed successfully", "code": self.AUDIO_DEVICE_CONFIG_CHANGED_SUCCCESS, "data": ""}
        
        except Exception as e:
            self._log_error("write_audio_device_config", e)
            result = {"status": False, "msg": "Audio device change error", "code": self.AUDIO_DEVICE_CONFIG_CHANGED_ERROR, "data": str(e)}
        
        return n4d.responses.build_successful_call_response(result)

    #def write_audio_device_config

#class BellSchedulerManager


