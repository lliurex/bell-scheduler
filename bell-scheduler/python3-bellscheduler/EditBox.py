#!/usr/bin/env python3


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib,Gdk

from . import settings
import gettext
gettext.textdomain(settings.TEXT_DOMAIN)
_ = gettext.gettext

import os
import json
import codecs
import io
import glob
import threading

BANNERS_PATH="/usr/share/bell-scheduler/banners/"

class EditBox(Gtk.VBox):
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
	
	#def __init__	
		
	def init_form(self):

		try:
			self.editBox.remove(self.editBox.main_box)
		except:
			pass

	#def init_form		

	def render_form(self):	

		builder=Gtk.Builder()
		builder.set_translation_domain(settings.TEXT_DOMAIN)

		ui_path=self.core.ui_path
		builder.add_from_file(ui_path)

		self.css_file=self.core.rsrc_dir+"bell-scheduler.css"
		self.main_box=builder.get_object("bell_edit_box")
		self.cron_frame=builder.get_object("cron_frame")
		self.hour_spinbutton=builder.get_object("hour_spinbutton")
		self.minute_spinbutton=builder.get_object("minute_spinbutton")
		self.monday_tb=builder.get_object("monday_togglebutton")
		self.tuesday_tb=builder.get_object("tuesday_togglebutton")
		self.wednesday_tb=builder.get_object("wednesday_togglebutton")
		self.thursday_tb=builder.get_object("thursday_togglebutton")
		self.friday_tb=builder.get_object("friday_togglebutton")

		self.data_frame=builder.get_object("data_frame")
		self.name_label=builder.get_object("name_label")
		self.name_entry=builder.get_object("name_entry")
		self.image_label=builder.get_object("image_label")
		self.stock_rb=builder.get_object("stock_radiobutton")
		self.custom_rb=builder.get_object("custom_radiobutton")
		self.image_fc=builder.get_object("image_filechosser")
		self.sound_label=builder.get_object("sound_label")
		self.directory_rb=builder.get_object("directory_radiobutton")
		self.file_rb=builder.get_object("file_radiobutton")
		self.url_rb=builder.get_object("url_radiobutton")
		self.urlslist_rb=builder.get_object("urlslist_radiobutton")
		self.sound_dc=builder.get_object("sound_folderchosser")
		self.sound_fc=builder.get_object("sound_filechosser")
		self.sound_url=builder.get_object("url_entry")
		self.sound_urlslist=builder.get_object("urlslist_filechosser")

		self.play_label=builder.get_object("play_label")
		self.start_time_label=builder.get_object("start_time_label")
		self.start_time_entry=builder.get_object("start_time_entry")
		self.duration_label=builder.get_object("duration_label")
		self.duration_entry=builder.get_object("duration_entry")
		self.note_label=builder.get_object("note_label")
	
		self.weekdays=[]
		self.weekdays.append(self.monday_tb)
		self.weekdays.append(self.tuesday_tb)
		self.weekdays.append(self.wednesday_tb)
		self.weekdays.append(self.thursday_tb)
		self.weekdays.append(self.friday_tb)

		self.image_cb=builder.get_object("image_combobox")
		self.image_store=Gtk.ListStore(GdkPixbuf.Pixbuf,str)
		
		for x in sorted(glob.glob(BANNERS_PATH+"*.png")):
			f_name=x.replace(BANNERS_PATH,"").split(".png")[0]
			image=Gtk.Image()
			image.set_from_file(x)
			pixbuf=image.get_pixbuf()
			pixbuf=pixbuf.scale_simple(64,64,GdkPixbuf.InterpType.BILINEAR)
			self.image_store.append([pixbuf,f_name])
			
			
		self.image_cb.set_model(self.image_store)
		pixbuf_renderer=Gtk.CellRendererPixbuf()
		
		self.image_cb.pack_start(pixbuf_renderer,True)
		self.image_cb.add_attribute(pixbuf_renderer,"pixbuf",0)
	
		self.edit=False
		self.bell_to_edit=""
		self.pack_start(self.main_box,True,True,0)
		self.set_css_info()
		self.connect_signals()
		self.init_data_form()
				
	#def render_form_

	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()

		f=Gio.File.new_for_path(self.css_file)
		self.style_provider.load_from_file(f)

		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.name_label.set_name("EDIT_LABEL")
		self.image_label.set_name("EDIT_LABEL")
		self.sound_label.set_name("EDIT_LABEL")
		self.play_label.set_name("EDIT_LABEL")
		self.note_label.set_name("NOTE_LABEL")
	
	#def set-css_info

	def connect_signals(self):

		self.stock_rb.connect("toggled",self.image_toggled_button,"stock")
		self.custom_rb.connect("toggled",self.image_toggled_button,"custom")
		self.directory_rb.connect("toggled",self.sound_toggled_button,"directory")
		self.file_rb.connect("toggled",self.sound_toggled_button,"file")
		self.url_rb.connect("toggled",self.sound_toggled_button,"url")
		self.urlslist_rb.connect("toggled",self.sound_toggled_button,"urlslist")
		self.image_fc.connect("file-set",self.check_mimetype_image)
		self.sound_fc.connect("file-set",self.check_mimetype_sound)

	#def connect_signals	

	def init_threads(self):

		self.checking_data_t=threading.Thread(target=self.checking_data)
		self.checking_data_t.daemon=True
		GObject.threads_init()
		
	#def init_threads	

	def init_data_form(self):

		self.image_op="stock"
		self.image_cb.set_active(1)
		self.image_fc.set_sensitive(False)
		self.sound_op="file"
		self.sound_dc.set_sensitive(False)
		self.sound_url.set_sensitive(False)
		self.sound_urlslist.set_sensitive(False)
		self.start_time_entry.set_value(0)
		self.duration_entry.set_value(30)
		self.init_threads()

	#def init_data_form	


	def image_toggled_button(self,button,name):

		if button.get_active():
			if name=="stock":
				self.image_cb.set_sensitive(True)
				self.image_fc.set_sensitive(False)
				self.image_op="stock"

			else:
				self.image_cb.set_sensitive(False)
				self.image_fc.set_sensitive(True)	
				self.image_op="custom"

	#def image_toggled_button			

	
	def sound_toggled_button(self,button,name):

		if button.get_active():
			if name=="directory":
				self.sound_dc.set_sensitive(True)
				self.sound_fc.set_sensitive(False)
				self.sound_url.set_sensitive(False)
				self.sound_urlslist.set_sensitive(False)
				self.sound_op="directory"
			elif name=="file":
				self.sound_dc.set_sensitive(False)
				self.sound_fc.set_sensitive(True)
				self.sound_url.set_sensitive(False)
				self.sound_urlslist.set_sensitive(False)
				self.sound_op="file"
			elif name=="url":
				self.sound_dc.set_sensitive(False)
				self.sound_fc.set_sensitive(False)
				self.sound_url.set_sensitive(True)
				self.sound_urlslist.set_sensitive(False)	
				self.sound_op="url"
			elif name=="urlslist":
				self.sound_dc.set_sensitive(False)
				self.sound_fc.set_sensitive(False)
				self.sound_url.set_sensitive(False)
				self.sound_urlslist.set_sensitive(True)	
				self.sound_op="urlslist"		

	#def sound_toggled_button 					
	
	
	def load_values(self,bell):
	
		bell_to_edit=self.core.mainWindow.bells_info[bell]

		self.hour_spinbutton.set_value(bell_to_edit["hour"])	
		self.minute_spinbutton.set_value(bell_to_edit["minute"])
		self.name_entry.set_text(bell_to_edit["name"])	
		
		weekdays=bell_to_edit["weekdays"]
		if weekdays["0"]:
			self.monday_tb.set_active(True)
		if weekdays["1"]:
			self.tuesday_tb.set_active(True)	
		if weekdays["2"]:
			self.wednesday_tb.set_active(True)	
		if weekdays["3"]:
			self.thursday_tb.set_active(True)	
		if weekdays["4"]:
			self.friday_tb.set_active(True)	

		image_op=bell_to_edit["image"]["option"]

		if image_op=="stock":
			self.stock_rb.set_active(True)
			if os.path.exists(bell_to_edit["image"]["path"]):
				c=0
				for i in self.image_store:
					if os.path.basename(bell_to_edit["image"]["path"]).split(".")[0]==i[1]:
						break
					c+=1
				self.image_cb.set_active(c)				
		else:
			self.custom_rb.set_active(True)
			if os.path.exists(bell_to_edit["image"]["path"]):
				self.image_fc.set_filename(bell_to_edit["image"]["path"])

		sound_op=bell_to_edit["sound"]["option"]

		if sound_op=="directory":
			self.directory_rb.set_active(True)
			if os.path.exists(bell_to_edit["sound"]["path"]):
				self.sound_dc.set_filename(bell_to_edit["sound"]["path"])
		elif sound_op=="file":
			self.file_rb.set_active(True)
			if os.path.exists(bell_to_edit["sound"]["path"]):
				self.sound_fc.set_filename(bell_to_edit["sound"]["path"])	
		elif sound_op=="url":
			self.url_rb.set_active(True)
			self.sound_url.set_text(bell_to_edit["sound"]["path"])
		elif sound_op=="urlslist":
			self.urlslist_rb.set_active(True)
			if os.path.exists(bell_to_edit["sound"]["path"]):
				self.sound_urlslist.set_filename(bell_to_edit["sound"]["path"])		

		self.duration_entry.set_value(bell_to_edit["play"]["duration"])
		try:
			self.start_time_entry.set_value(bell_to_edit["play"]["start"])
		except:
			pass	
		
		self.edit=True
		self.bell_to_edit=bell
		self.active_bell=bell_to_edit["active"]

	#def load_values	
	
	def gather_values(self,widget):

		self.core.mainWindow.msg_label.set_text("")
		self.data_tocheck={}
		self.data_tocheck["name"]=self.name_entry.get_text()
		self.data_tocheck["image"]={}
		self.data_tocheck["image"]["option"]=self.image_op
		self.data_tocheck["sound"]={}
		self.data_tocheck["sound"]["option"]=self.sound_op

		self.core.mainWindow.save_button.set_sensitive(False)
		self.core.mainWindow.cancel_button.set_sensitive(False)
		self.manage_form_control(False)

		
		if self.image_op=="stock":
			self.image_path=BANNERS_PATH+self.image_store[self.image_cb.get_active()][1]+".png"
		else:
			self.image_path=self.image_fc.get_filename()
			self.data_tocheck["image"]["file"]=self.image_path

		if self.sound_op=="directory":
			self.sound_path=self.sound_dc.get_filename()
			self.data_tocheck["sound"]["file"]=self.sound_path
		elif self.sound_op=="file":
			self.sound_path=self.sound_fc.get_filename()
			self.data_tocheck["sound"]["file"]=self.sound_path
		elif self.sound_op=="url":	
			self.sound_path=self.sound_url.get_text().split('\n')[0]
			self.data_tocheck["sound"]["file"]=self.sound_path
		elif self.sound_op=="urlslist":
			self.sound_path=self.sound_urlslist.get_filename()
			self.data_tocheck["sound"]["file"]=self.sound_path	
			
		self.duration=self.duration_entry.get_value_as_int()
		self.start_time=self.start_time_entry.get_value_as_int()
		
		self.core.mainWindow.waiting_label.set_text(self.core.mainWindow.get_msg(30))			
		self.core.mainWindow.waiting_window.show_all()
		self.init_threads()
		self.checking_data_t.start()
		GLib.timeout_add(100,self.pulsate_checking_data)
		
	#def gather_values	

	def pulsate_checking_data(self):
		
		if self.checking_data_t.is_alive():
			self.core.mainWindow.waiting_pbar.pulse()
			return True
			
		else:
			self.core.mainWindow.waiting_window.hide()
			
			if not self.check["result"]:
				self.core.mainWindow.save_button.set_sensitive(True)
				self.core.mainWindow.cancel_button.set_sensitive(True)
				self.manage_form_control(True)
				self.core.mainWindow.manage_message(True,self.check["code"],self.check["data"])
			else:	
				self.save_values()
		
		return False
		
	#def pulsate_checking_data	
		
	def checking_data(self):
		
		self.check=self.core.bellmanager.check_data(self.data_tocheck)
	
	#def checking_data
		
	def save_values(self):		
		
		'''
		Result code:
			-15: edited successfully
			-18: created successfully
		'''

		bell=self.core.mainWindow.bells_info.copy()
		order_keys=[]
	
		if self.edit:
			order=self.bell_to_edit
			action="edit"
		else:		
			if len(bell)>0:
				keys=bell.keys()
				for item in  keys:
					order_keys.append(int(item))

				order=str(int(max(order_keys))+1)
			else:
				order="1"
			action="add"	
			
		minute=self.minute_spinbutton.get_value_as_int()
		hour=self.hour_spinbutton.get_value_as_int()
				

		bell[order]={}		
		bell[order]["hour"]=hour
		bell[order]["minute"]=minute
		bell[order]["weekdays"]={}			
		bell[order]["weekdays"]["0"]=self.monday_tb.get_active()
		bell[order]["weekdays"]["1"]=self.tuesday_tb.get_active()
		bell[order]["weekdays"]["2"]=self.wednesday_tb.get_active()
		bell[order]["weekdays"]["3"]=self.thursday_tb.get_active()
		bell[order]["weekdays"]["4"]=self.friday_tb.get_active()

		count=0
		if self.monday_tb.get_active():
			count=count+1
		if self.tuesday_tb.get_active():
			count+=count+1
		if self.wednesday_tb.get_active():
			count+=count+1		
		if self.thursday_tb.get_active():
			count+=count+1
		if self.friday_tb.get_active():
			count+=count+1	


		if count>0:
			if self.edit:
				active_bell=self.active_bell
			else:
				active_bell=True	
		else:
			active_bell=False	

				
		bell[order]["name"]=self.name_entry.get_text()

		bell[order]["image"]={}
		bell[order]["image"]["option"]=self.image_op
		if self.image_op=="custom":
			orig_image_path=self.image_path
			dest_image_path=os.path.join(self.core.images_path,os.path.basename(orig_image_path))
		else:
			orig_image_path=""
			dest_image_path=self.image_path

		bell[order]["image"]["path"]=dest_image_path

		bell[order]["sound"]={}
		bell[order]["sound"]["option"]=self.sound_op
		if self.sound_op=="file":
			orig_sound_path=self.sound_path
			dest_sound_path=os.path.join(self.core.sounds_path,os.path.basename(orig_sound_path))
		else:
			orig_sound_path=""
			dest_sound_path=self.sound_path

		bell[order]["sound"]["path"]=dest_sound_path	


		bell[order]["play"]={}
		bell[order]["play"]["duration"]=self.duration
		bell[order]["play"]["start"]=self.start_time


		bell[order]["active"]=active_bell
		

		result_copy=self.core.bellmanager.copy_media_files(orig_image_path,orig_sound_path)
		if result_copy['status']:
			result=self.core.bellmanager.save_conf(bell,order,action)
			if result['status']:
				self.core.mainWindow.load_info()
				self.core.bellBox.draw_bell(False,order)

			else:
				self.core.bellBox.draw_bell(False)


		self.core.mainWindow.search_entry.set_text("")
		self.core.mainWindow.manage_menubar(True)	
		self.core.mainWindow.manage_down_buttons(False)
		self.core.mainWindow.stack_opt.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
		self.core.mainWindow.stack_opt.set_visible_child_name("bellBox")
		self.core.editBox.remove(self.core.editBox.main_box)

		if result_copy['status']:
			if result['status']:
				if self.edit:
					self.core.mainWindow.manage_message(False,15)
				else:
					self.core.mainWindow.manage_message(False,18)	
			else:
				self.core.mainWindow.manage_message(True,result['code'])	
		else:
			self.core.mainWindow.manage_message(True,result_copy['code'])		


	#def save_values		
	
	
	def check_mimetype_image(self,widget):
	
		check=self.core.bellmanager.check_mimetypes(self.image_fc.get_filename(),"image")
		if check !=None:
			self.core.mainWindow.manage_message(True,check["code"])
		else:
			self.core.mainWindow.msg_label.set_text("")

	#def check_mimetype_image		
	
	def check_mimetype_sound(self,widget):
	
		check=self.core.bellmanager.check_mimetypes(self.sound_fc.get_filename(),"audio")
		if check !=None:
			self.core.mainWindow.manage_message(True,check["code"])
		else:
			self.core.mainWindow.msg_label.set_text("")

	#def check_mimetype_sound		


	def manage_form_control(self,sensitive):

		self.hour_spinbutton.set_sensitive(sensitive)
		self.minute_spinbutton.set_sensitive(sensitive)
		
		for item in self.weekdays:
			item.set_sensitive(sensitive)

		self.name_entry.set_sensitive(sensitive)	

		self.stock_rb.set_sensitive(sensitive)
		self.custom_rb.set_sensitive(sensitive)

		self.file_rb.set_sensitive(sensitive)
		self.directory_rb.set_sensitive(sensitive)
		self.url_rb.set_sensitive(sensitive)
		self.urlslist_rb.set_sensitive(sensitive)

		if self.image_op=="stock":
			self.image_cb.set_sensitive(sensitive)
		else:
			self.image_fc.set_sensitive(sensitive)

		if self.sound_op=="file":
			self.sound_fc.set_sensitive(sensitive)
		elif self.sound_op=="directory":
			self.sound_dc.set_sensitive(sensitive)
		elif self.sound_op=="url":
			self.sound_url.set_sensitive(sensitive)			
		elif self.sound_op=="urlslist":
			self.sound_urlslist.set_sensitive(sensitive)		

		self.duration_entry.set_sensitive(sensitive)
		self.start_time_entry.set_sensitive(sensitive)

	#def manage_form_control	
	
#class EditBox

from . import Core
