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
from datetime import datetime, date,timedelta


BANNERS_PATH="/usr/share/bell-scheduler/banners/"

class EditBox(Gtk.VBox):
	
	DATE_RANGE_INCONSISTENT_ERROR=-53
	DATE_RANGE_INCOMPLETE_ERROR=-54
	DATE_EMPTY_ERROR=-55

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
		
		self.cron_box=builder.get_object("cron_box")
		self.hour_eb=builder.get_object("hour_eb")
		self.hour_label=builder.get_object("hour_label")
		self.separator_label=builder.get_object("separator_label")
		self.minute_label=builder.get_object("minute_label")
		self.hour_popover=builder.get_object("hour_popover")
		self.hour_spinbutton=builder.get_object("hour_spinbutton")
		self.minute_spinbutton=builder.get_object("minute_spinbutton")
		self.hour_popover_apply_bt=builder.get_object("hour_popover_apply_bt")
		self.hour_popover_cancel_bt=builder.get_object("hour_popover_cancel_bt")
		self.monday_tb=builder.get_object("monday_togglebutton")
		self.tuesday_tb=builder.get_object("tuesday_togglebutton")
		self.wednesday_tb=builder.get_object("wednesday_togglebutton")
		self.thursday_tb=builder.get_object("thursday_togglebutton")
		self.friday_tb=builder.get_object("friday_togglebutton")
		self.validity_cb=builder.get_object("validity_cb")
		self.validity_entry=builder.get_object("validity_entry")
		self.validity_edit_bt=builder.get_object("validity_edit_bt")
		self.validity_popover=builder.get_object("validity_popover")
		self.calendar=builder.get_object("calendar")
		self.date_separator_label=builder.get_object("date_separaror_label")
		self.date_separator=builder.get_object("date_separator")
		self.single_day_rb=builder.get_object("single_day_rb")
		self.single_day_entry=builder.get_object("single_day_entry")
		self.range_day_rb=builder.get_object("range_day_rb")
		self.range_day1_entry=builder.get_object("range_day1_entry")
		self.range_day2_entry=builder.get_object("range_day2_entry")
		self.remove_day_button=builder.get_object("remove_day_button")
		self.remove_range_button=builder.get_object("remove_range_button")
		self.add_day_button=builder.get_object("add_day_button")
		self.calendar_message_box=builder.get_object("calendar_message_box")
		self.calendar_error_img=builder.get_object("calendar_error_img")
		self.calendar_message_label=builder.get_object("calendar_message_label")
		self.save_day_button=builder.get_object("save_day_button")
		self.cancel_day_button=builder.get_object("cancel_day_button")	
		self.data_box=builder.get_object("data_box")
		self.name_label=builder.get_object("name_label")
		self.name_entry=builder.get_object("name_entry")
		self.image_popover=builder.get_object("image_popover")
		self.image_popover_msg_box=builder.get_object("image_popover_msg_box")
		self.image_popover_error_img=builder.get_object("image_popover_error_img")
		self.image_popover_msg=builder.get_object("image_popover_msg")
		self.image_popover_cancel_bt=builder.get_object("image_popover_cancel_bt")
		self.image_popover_apply_bt=builder.get_object("image_popover_apply_bt")
		self.stock_rb=builder.get_object("stock_radiobutton")
		self.custom_rb=builder.get_object("custom_radiobutton")
		self.image_fc=builder.get_object("image_filechosser")
		label=self.image_fc.get_children()[0].get_children()[0].get_children()[1]
		label.set_max_width_chars(30)
		label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
		self.image_box=builder.get_object("image_box")
		self.image_eb=builder.get_object("image_eb")
		self.image_bell=builder.get_object("bell_image")
		
		self.sound_label=builder.get_object("sound_label")
		self.sound_op_label=builder.get_object("sound_op_label")
		self.sound_path_label=builder.get_object("sound_op_path")
		self.sound_path_label.set_width_chars(45)
		self.sound_path_label.set_max_width_chars(45)
		self.sound_path_label.set_xalign(1)
		self.sound_path_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
		self.sound_edit_button=builder.get_object("sound_edit_button")
		self.sound_popover=builder.get_object("sound_popover")
		self.sound_popover_msg_box=builder.get_object("sound_popover_msg_box")
		self.sound_popover_error_img=builder.get_object("sound_popover_error_img")
		self.sound_popover_msg=builder.get_object("sound_popover_msg")
		self.sound_popover_cancel_bt=builder.get_object("sound_popover_cancel_bt")
		self.sound_popover_apply_bt=builder.get_object("sound_popover_apply_bt")
		self.sound_options_box=builder.get_object("sound_options_box")
		self.sound_grid=builder.get_object("sound_grid")
		self.sound_grid.set_hexpand(False)
		self.directory_rb=builder.get_object("directory_radiobutton")
		self.file_rb=builder.get_object("file_radiobutton")
		self.url_rb=builder.get_object("url_radiobutton")
		self.urlslist_rb=builder.get_object("urlslist_radiobutton")
		self.sound_dc=builder.get_object("sound_folderchosser")
		label=self.sound_dc.get_children()[0].get_children()[0].get_children()[1]
		label.set_max_width_chars(30)
		label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
		self.sound_fc=builder.get_object("sound_filechosser")
		label=self.sound_fc.get_children()[0].get_children()[0].get_children()[1]
		label.set_max_width_chars(30)
		label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)

		self.sound_url=builder.get_object("url_entry")
		self.sound_urlslist=builder.get_object("urlslist_filechosser")
		label=self.sound_urlslist.get_children()[0].get_children()[0].get_children()[1]
		label.set_max_width_chars(30)
		label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)

		self.localpath_cb=builder.get_object("localpath_checkbutton")
		self.localpath_leyend=builder.get_object("localpath_leyend")
		
		self.play_label=builder.get_object("play_label")
		self.start_time_label=builder.get_object("start_time_label")
		self.start_entry_label=builder.get_object("start_entry_label")
		self.start_edit_bt=builder.get_object("start_edit_bt")
		self.start_popover=builder.get_object("start_popover")
		self.start_popover_cancel_bt=builder.get_object("start_popover_cancel_bt")
		self.start_popover_apply_bt=builder.get_object("start_popover_apply_bt")
		self.start_time_spinbutton=builder.get_object("start_time_spinbutton")
		self.duration_label=builder.get_object("duration_label")
		self.duration_entry_label=builder.get_object("duration_entry_label")
		self.duration_second_label=builder.get_object("duration_second_label")
		self.duration_edit_bt=builder.get_object("duration_edit_bt")
		self.duration_popover=builder.get_object("duration_popover")
		self.duration_popover_cancel_bt=builder.get_object("duration_popover_cancel_bt")
		self.duration_popover_apply_bt=builder.get_object("duration_popover_apply_bt")
		self.duration_spinbutton=builder.get_object("duration_spinbutton")
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
		self.cron_box.set_name("CARD-ITEM")
		self.hour_label.set_name("TIME_LABEL")
		self.separator_label.set_name("TIME_LABEL")
		self.minute_label.set_name("TIME_LABEL")
		self.data_box.set_name("CARD-ITEM")
		self.name_label.set_name("EDIT_LABEL")
		self.name_entry.set_name("CUSTOM-ENTRY")
		self.sound_label.set_name("EDIT_LABEL")
		self.sound_path_label.set_name("SOUND_PATH_LABEL")
		self.play_label.set_name("EDIT_LABEL")
		self.note_label.set_name("NOTE_LABEL")
		self.image_box.set_name("IMAGE_BOX")
		self.sound_url.set_name("CUSTOM-ENTRY")
		self.localpath_leyend.set_name("NOTE_LABEL")
		self.calendar.set_name("CALENDAR")
		self.single_day_entry.set_name("CUSTOM-ENTRY")
		self.range_day1_entry.set_name("CUSTOM-ENTRY")
		self.range_day2_entry.set_name("CUSTOM-ENTRY")
		self.date_separator_label.set_name("HEADER-LABEL")
		self.date_separator.set_name("HEADER_SEPARATOR")

	#def set-css_info

	def connect_signals(self):

		self.hour_eb.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
		self.hour_eb.connect("button-press-event", self.edit_hour_bell)
		self.hour_eb.connect("motion-notify-event", self.mouse_over_hour)
		self.hour_eb.connect("leave-notify-event", self.mouse_exit_hour)
		self.hour_popover.connect("closed",self.hour_popover_closed)
		self.hour_popover_apply_bt.connect("clicked",self.hour_popover_apply_bt_clicked)
		self.hour_popover_cancel_bt.connect("clicked",self.hour_popover_cancel_bt_clicked)
		self.monday_tb.connect("toggled",self.weekday_clicked,0)
		self.tuesday_tb.connect("toggled",self.weekday_clicked,1)
		self.wednesday_tb.connect("toggled",self.weekday_clicked,2)
		self.thursday_tb.connect("toggled",self.weekday_clicked,3)
		self.friday_tb.connect("toggled",self.weekday_clicked,4)
		self.validity_cb.connect("toggled",self.validity_cb_clicked)
		self.validity_edit_bt.connect("clicked",self.validity_edit_bt_clicked)
		self.single_day_rb.connect("toggled",self.day_toggled_button,"singleDay")
		self.range_day_rb.connect("toggled",self.day_toggled_button,"rangeDay")
		self.calendar.connect("month-changed",self.month_changed)
		self.calendar.connect("day_selected",self.day_selected)
		self.remove_day_button.connect("clicked",self.remove_range,"singleDay")
		self.remove_range_button.connect("clicked",self.remove_range,"rangeDay")
		self.save_day_button.connect("clicked",self.save_day_clicked)
		self.cancel_day_button.connect("clicked",self.cancel_day_clicked)
		self.validity_popover.connect("closed",self.validity_popover_closed)
		self.stock_rb.connect("toggled",self.image_toggled_button,"stock")
		self.custom_rb.connect("toggled",self.image_toggled_button,"custom")
		self.directory_rb.connect("toggled",self.sound_toggled_button,"directory")
		self.file_rb.connect("toggled",self.sound_toggled_button,"file")
		self.url_rb.connect("toggled",self.sound_toggled_button,"url")
		self.urlslist_rb.connect("toggled",self.sound_toggled_button,"urlslist")
		self.image_fc.connect("file-set",self.check_mimetype_image)
		self.sound_fc.connect("file-set",self.check_mimetype_sound)
		self.image_eb.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
		self.image_eb.connect("button-press-event", self.edit_image_clicked)
		self.image_eb.connect("motion-notify-event", self.mouse_over_image)
		self.image_eb.connect("leave-notify-event", self.mouse_exit_image)
		self.image_popover_cancel_bt.connect("clicked",self.image_popover_cancel_bt_clicked)
		self.image_popover_apply_bt.connect("clicked",self.image_popover_apply_bt_clicked)
		self.image_popover.connect("closed",self.image_popover_closed)
		self.sound_edit_button.connect("clicked",self.sound_edit_button_clicked)
		self.sound_popover.connect("closed",self.sound_popover_closed)
		self.sound_popover_cancel_bt.connect("clicked",self.sound_popover_cancel_bt_clicked)
		self.sound_popover_apply_bt.connect("clicked",self.sound_popover_apply_bt_clicked)
		self.start_edit_bt.connect("clicked",self.start_edit_bt_clicked)
		self.start_popover.connect("closed",self.start_popover_closed)
		self.start_popover_cancel_bt.connect("clicked",self.start_popover_cancel_bt_clicked)
		self.start_popover_apply_bt.connect("clicked",self.start_popover_apply_bt_clicked)
		self.duration_edit_bt.connect("clicked",self.duration_edit_bt_clicked)
		self.duration_popover.connect("closed",self.duration_popover_closed)
		self.duration_popover_cancel_bt.connect("clicked",self.duration_popover_cancel_bt_clicked)
		self.duration_popover_apply_bt.connect("clicked",self.duration_popover_apply_bt_clicked)
	
	#def connect_signals	

	def init_threads(self):

		self.checking_data_t=threading.Thread(target=self.checking_data)
		self.checking_data_t.daemon=True
		GObject.threads_init()
		
	#def init_threads	

	def init_data_form(self):

		self.image_op="stock"
		self.image_cb.set_active(1)
		path=BANNERS_PATH+self.image_store[self.image_cb.get_active()][1]+".png"
		self.render_bell_image(path)
		self.image_fc.set_sensitive(False)
		self.sound_op="file"
		self.sound_op_label.set_text(self.get_sound_option_label("file"))
		self.sound_dc.set_sensitive(False)
		self.sound_url.set_sensitive(False)
		self.sound_urlslist.set_sensitive(False)
		self.localpath_cb.set_active(False)
		self.localpath_cb.set_sensitive(False)
		self.start_time_spinbutton.set_value(0)
		self.duration_spinbutton.set_value(30)
		self.validity=""
		self.validity_cb.set_active(False)
		self.validity_cb.set_sensitive(False)
		self.validity_edit_bt.set_sensitive(False)
		self.active_weekdays=[False,False,False,False,False]
		self.there_are_active_days=False
		self.init_calendar()
		self.init_threads()

	#def init_data_form	

	def image_toggled_button(self,button,name):
		
		if button.get_active():
			if name=="stock":
				self.image_cb.set_sensitive(True)
				self.image_fc.set_sensitive(False)
				self.image_popover_apply_bt.set_sensitive(True)
				self.image_op="stock"
			else:
				self.image_cb.set_sensitive(False)
				self.image_fc.set_sensitive(True)	
				self.image_popover_apply_bt.set_sensitive(False)

				self.image_op="custom"

	#def image_toggled_button			

	def sound_toggled_button(self,button,name):

		if button.get_active():
			if name=="directory":
				self.sound_dc.set_sensitive(True)
				self.sound_fc.set_sensitive(False)
				self.sound_url.set_sensitive(False)
				self.sound_urlslist.set_sensitive(False)
				self.localpath_cb.set_sensitive(False)
				self.sound_op="directory"
				self.sound_popover_apply_bt.set_sensitive(True)
			elif name=="file":
				self.sound_dc.set_sensitive(False)
				self.sound_fc.set_sensitive(True)
				self.sound_url.set_sensitive(False)
				self.sound_urlslist.set_sensitive(False)
				self.sound_op="file"
				if self.sound_fc.get_filename() !=None:
					check=self.core.bellmanager.check_mimetypes(self.sound_fc.get_filename(),"audio")
					if check==None:
						self.sound_popover_apply_bt.set_sensitive(True)
						if self.core.sounds_path not in self.sound_fc.get_filename():
							self.localpath_cb.set_sensitive(True)
					else:
						self.sound_popover_apply_bt.set_sensitive(False)
						self.localpath_cb.set_sensitive(False)	
				else:	
					self.sound_popover_apply_bt.set_sensitive(False)
					self.localpath_cb.set_sensitive(False)	
			elif name=="url":
				self.sound_dc.set_sensitive(False)
				self.sound_fc.set_sensitive(False)
				self.sound_url.set_sensitive(True)
				self.sound_urlslist.set_sensitive(False)
				self.localpath_cb.set_sensitive(False)	
				self.sound_op="url"
				self.sound_popover_apply_bt.set_sensitive(True)
			elif name=="urlslist":
				self.sound_dc.set_sensitive(False)
				self.sound_fc.set_sensitive(False)
				self.sound_url.set_sensitive(False)
				self.sound_urlslist.set_sensitive(True)
				self.localpath_cb.set_sensitive(False)	
				self.sound_op="urlslist"	
				self.sound_popover_apply_bt.set_sensitive(True)

	#def sound_toggled_button 					
	
	def load_values(self,bell):
	
		self.localpath_cb.set_active(False)
		self.validity_cb.set_active(False)
		
		bell_to_edit=self.core.mainWindow.bells_info[bell]

		self.hour_spinbutton.set_value(bell_to_edit["hour"])	
		self.minute_spinbutton.set_value(bell_to_edit["minute"])
		format_time=self.format_hour_label(bell_to_edit["hour"],bell_to_edit["minute"])
		self.hour_label.set_text(format_time[0])
		self.minute_label.set_text(format_time[1])
		self.name_entry.set_text(bell_to_edit["name"])	
		
		weekdays=bell_to_edit["weekdays"]
		if weekdays["0"]:
			self.monday_tb.set_active(True)
			self.active_weekdays[0]=True
		if weekdays["1"]:
			self.tuesday_tb.set_active(True)
			self.active_weekdays[1]=True	
		if weekdays["2"]:
			self.wednesday_tb.set_active(True)
			self.active_weekdays[2]=True	
		if weekdays["3"]:
			self.thursday_tb.set_active(True)
			self.active_weekdays[3]=True	
		if weekdays["4"]:
			self.friday_tb.set_active(True)
			self.active_weekdays[4]=True	

		try:
			if True in self.active_weekdays:
				self.validity_cb.set_sensitive(True)
			if bell_to_edit["validity"]["active"]:
				self.validity_cb.set_active(True)
				if True in self.active_weekdays:
					self.validity_edit_bt.set_sensitive(True)
			self.validity=bell_to_edit["validity"]["value"]
			self.validity_entry.set_text(self.validity)

		except:
			self.validity=""
			self.validity_entry.set_text(self.validity)
		
		self.load_current_validity()

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
				
		try:
			self.render_bell_image(bell_to_edit["image"]["path"])
		except:
			self.render_bell_image(self.core.rsrc_dir+"image_nodisp.svg")
		
		sound_op=bell_to_edit["sound"]["option"]
		sound_error=True
		
		if sound_op=="directory":
			self.directory_rb.set_active(True)
			if os.path.exists(bell_to_edit["sound"]["path"]):
				self.sound_dc.set_filename(bell_to_edit["sound"]["path"])
				sound_error=False
		elif sound_op=="file":
			self.file_rb.set_active(True)
			if os.path.exists(bell_to_edit["sound"]["path"]):
				self.sound_fc.set_filename(bell_to_edit["sound"]["path"])
				sound_error=False

			if self.core.sounds_path in bell_to_edit["sound"]["path"]:
				self.localpath_cb.set_active(True)
			else:
				self.localpath_cb.set_sensitive(True)	
				
		elif sound_op=="url":
			self.url_rb.set_active(True)
			self.sound_url.set_text(bell_to_edit["sound"]["path"])
			sound_error=False
		elif sound_op=="urlslist":
			self.urlslist_rb.set_active(True)
			if os.path.exists(bell_to_edit["sound"]["path"]):
				self.sound_urlslist.set_filename(bell_to_edit["sound"]["path"])	
				sound_error=False

		self.sound_op_label.set_text(self.get_sound_option_label(sound_op))
		if sound_error:
			self.sound_path_label.set_text(self.core.mainWindow.get_msg(29))
			self.sound_path_label.set_name("MSG_ERROR_LABEL")
		else:
			self.sound_path_label.set_text(self.get_sound_path(sound_op,True))
			self.sound_path_label.set_name("SOUND_PATH_LABEL")
			
		self.duration_spinbutton.set_value(bell_to_edit["play"]["duration"])
		duration=bell_to_edit["play"]["duration"]
		self.manage_duration_entry_label(duration)

		try:
			self.start_time_spinbutton.set_value(bell_to_edit["play"]["start"])
			self.start_entry_label.set_text(str(bell_to_edit["play"]["start"]))
		except:
			pass	
		
		self.edit=True
		self.bell_to_edit=bell
		self.active_bell=bell_to_edit["active"]

	#def load_values	
	
	def gather_values(self,widget):

		self.core.mainWindow.hide_message_items()
		self.data_tocheck={}
		self.data_tocheck["name"]=self.name_entry.get_text()
		self.data_tocheck["image"]={}
		self.data_tocheck["image"]["option"]=self.image_op
		self.data_tocheck["sound"]={}
		self.data_tocheck["sound"]["option"]=self.sound_op
		self.data_tocheck["weekdays"]=self.active_weekdays
		self.data_tocheck["validity"]={}
		self.data_tocheck["validity"]["active"]=self.validity_cb.get_active()
		self.data_tocheck["validity"]["value"]=self.validity

		self.core.mainWindow.save_button.set_sensitive(False)
		self.core.mainWindow.cancel_button.set_sensitive(False)
		self.manage_form_control(False)

		if self.image_op=="stock":
			self.image_path=BANNERS_PATH+self.image_store[self.image_cb.get_active()][1]+".png"
		else:
			self.image_path=self.image_fc.get_filename()
			self.data_tocheck["image"]["file"]=self.image_path

		self.sound_path=self.get_sound_path(self.sound_op,False)
		self.data_tocheck["sound"]["file"]=self.sound_path	
			
		self.duration=self.duration_spinbutton.get_value_as_int()
		self.start_time=self.start_time_spinbutton.get_value_as_int()
		
		self.core.mainWindow.waiting_label.set_text(self.core.mainWindow.get_msg(30))			
		self.core.mainWindow.manage_waiting_stack(True,True)
		self.init_threads()
		self.checking_data_t.start()
		GLib.timeout_add(100,self.pulsate_checking_data)
		
	#def gather_values	

	def pulsate_checking_data(self):
		
		if self.checking_data_t.is_alive():
			return True
		else:
			if not self.check["result"]:
				self.core.mainWindow.manage_waiting_stack(False,True,True)
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
		bell[order]["weekdays"]["0"]=self.active_weekdays[0]
		bell[order]["weekdays"]["1"]=self.active_weekdays[1]
		bell[order]["weekdays"]["2"]=self.active_weekdays[2]
		bell[order]["weekdays"]["3"]=self.active_weekdays[3]
		bell[order]["weekdays"]["4"]=self.active_weekdays[4]

		count=0
		for item in self.active_weekdays:
			if item:
				count=count+1
	
		if count>0:
			if self.edit:
				active_bell=self.active_bell
			else:
				active_bell=True	
		else:
			active_bell=False	

		bell[order]["validity"]={}
		if self.validity!="":
			if self.validity_cb.get_active():
				bell[order]["validity"]["active"]=True
			else:
				bell[order]["validity"]["active"]=False
		else:
			bell[order]["validity"]["active"]=False

		bell[order]["validity"]["value"]=self.validity
		
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
		orig_sound_path=""
		
		if self.sound_op=="file":
			if self.localpath_cb.get_active():
				orig_sound_path=self.sound_path
				dest_sound_path=os.path.join(self.core.sounds_path,os.path.basename(orig_sound_path))
			else:
				dest_sound_path=self.sound_path
		else:
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
			msg=self.core.mainWindow.get_msg(check["code"])
			self.image_popover_msg.set_text(msg)
			self.image_popover_error_img.show()
			self.image_popover_msg_box.set_name("ERROR_BOX")
			self.image_popover_apply_bt.set_sensitive(False)
		else:
			self.image_popover_msg.set_text("")
			self.image_popover_error_img.hide()
			self.image_popover_msg_box.set_name("HIDE_BOX")
			self.image_popover_apply_bt.set_sensitive(True)

	#def check_mimetype_image		
	
	def check_mimetype_sound(self,widget):

		check=self.core.bellmanager.check_mimetypes(self.sound_fc.get_filename(),"audio")
		if check !=None:
			msg=self.core.mainWindow.get_msg(check["code"])
			self.sound_popover_msg.set_text(msg)
			self.sound_popover_error_img.show()
			self.sound_popover_msg_box.set_name("ERROR_BOX")
			self.sound_popover_apply_bt.set_sensitive(False)
			self.localpath_cb.set_sensitive(False)
		else:
			self.sound_popover_msg.set_text("")
			self.sound_popover_error_img.hide()
			self.sound_popover_msg_box.set_name("HIDE_BOX")
			self.localpath_cb.set_active(True)
			if self.core.sounds_path not in self.sound_fc.get_filename():
				self.localpath_cb.set_sensitive(True)
			else:
				self.localpath_cb.set_sensitive(False)
			self.sound_popover_apply_bt.set_sensitive(True)

	#def check_mimetype_sound		

	def manage_form_control(self,sensitive):

		self.hour_spinbutton.set_sensitive(sensitive)
		self.minute_spinbutton.set_sensitive(sensitive)
		
		for item in self.weekdays:
			item.set_sensitive(sensitive)

		self.validity_edit_bt.set_sensitive(sensitive)
		self.name_entry.set_sensitive(sensitive)	
		self.hour_eb.set_sensitive(sensitive)
		self.sound_edit_button.set_sensitive(sensitive)
		self.image_eb.set_sensitive(sensitive)
		self.duration_edit_bt.set_sensitive(sensitive)
		self.start_edit_bt.set_sensitive(sensitive)
	
	#def manage_form_control	

	def edit_hour_bell(self,widget,event=None):
		
		self.core.mainWindow.hide_message_items()
		self.previous_hour=self.hour_spinbutton.get_value_as_int()
		self.previous_minute=self.minute_spinbutton.get_value_as_int()
		self.restore_hour=True
		self.hour_popover.show_all()

	#def edit_hour_bell	

	def hour_popover_apply_bt_clicked(self,button):

		format_time=self.format_hour_label(self.hour_spinbutton.get_value_as_int(),self.minute_spinbutton.get_value_as_int())
		self.hour_label.set_text(format_time[0])	
		self.minute_label.set_text(format_time[1])
		self.restore_hour=False
		self.hour_popover.hide()

	#def hour_popover_apply_bt_clicked	

	def hour_popover_cancel_bt_clicked(self,button):
		
		self.restore_hour=True
		self.hour_popover.hide()

	#def hour_popover_cancel_bt_clicked		

	def hour_popover_closed(self,widget,event=None):
	
		self.restore_hour_info()

	#def hour_popover_closed

	def restore_hour_info(self):

		if self.restore_hour:
			self.hour_spinbutton.set_value(self.previous_hour)	
			self.minute_spinbutton.set_value(self.previous_minute)

	#def restore_hour_info		

	def format_hour_label(self,hour,minute):
	
		time=[]
		if hour<10:
			hour='0'+str(hour)

		if minute<10:
			minute='0'+str(minute)

		time=[str(hour),str(minute)]

		return time			

	#def format_hour_label	

	def mouse_over_hour(self,widget,event=None):

		self.hour_label.set_name("TIME_LABEL_ON")
		self.separator_label.set_name("TIME_LABEL_ON")
		self.minute_label.set_name("TIME_LABEL_ON")

	#def mouse_over_hour 	

	def mouse_exit_hour(self,widget,event=None):
	
		self.hour_label.set_name("TIME_LABEL")
		self.separator_label.set_name("TIME_LABEL")
		self.minute_label.set_name("TIME_LABEL")

	#def mouse_exit_hour

	def weekday_clicked(self,button,day):

		if button.get_active():
			self.active_weekdays[day]=True
		else:
			self.active_weekdays[day]=False

		if True in self.active_weekdays:
			self.validity_cb.set_sensitive(True)
			if self.validity_cb.get_active():
				self.validity_edit_bt.set_sensitive(True)
		else:
			self.validity_cb.set_sensitive(False)
			self.validity_edit_bt.set_sensitive(False)

	#def weekday_clicked

	def validity_cb_clicked(self,cb,name=None):

		if cb.get_active():
			self.validity_edit_bt.set_sensitive(True)
			self.validity_cb.set_tooltip_text(_("Click to deactive the alarm validity period"))
		else:
			self.validity_cb.set_tooltip_text(_("Click to active the alarm validiy period"))
			self.validity_edit_bt.set_sensitive(False)

	#def validity_cb_clicked

	def validity_edit_bt_clicked(self,widget,event=None):

		self.restore_validity=True
		self.validity_popover.show_all()
		self.hide_calendar_message_items()
	
	def init_calendar(self):

		self.range=True
		self.clear_days=False
		self.day=""
		self.days_inrange=[]
		current_date=date.today().strftime('%d/%m/%Y').split("/")
		current_month=int(current_date[1])-1
		current_year=int(current_date[2])

		self.calendar.select_day(0)
		self.calendar.select_month(current_month,current_year)
		self.single_day_rb.set_active(False)
		self.range_day_rb.set_active(True)
		self.remove_day_button.set_sensitive(False)
		self.single_day_entry.set_text("")
		self.range_day1_entry.set_text("")
		self.range_day2_entry.set_text("")
		self.edit_day=False
		self.hide_calendar_message_items()

	#def init_calendar

	def load_current_validity(self):

		self.init_calendar()
		self.calendar.clear_marks()
		if self.validity!="":
			if "-" in self.validity:
				self.range=True
				tmpDay=self.validity.split("-")
				self.range_day_rb.set_active(True)
				self.range_day1_entry.set_text(tmpDay[0])
				self.range_day2_entry.set_text(tmpDay[1])
			else:
				self.range=False
				self.single_day_rb.set_active(True)
				self.single_day_entry.set_text(self.validity)	

			self.marked_range_days(1,self.validity)
	
	#def load_current_validity

	def day_toggled_button (self,button,name):

		if button.get_active():
			self.calendar.clear_marks()

			if name=="singleDay":
				self.range=False
				self.range_day1_entry.set_text("")
				self.range_day2_entry.set_text("")
				self.remove_day_button.set_sensitive(True)
				self.remove_range_button.set_sensitive(False)
				self.hide_calendar_message_items()
			else:
				self.calendar.select_day(0)
				self.range=True
				self.remove_range_button.set_sensitive(True)
				self.remove_day_button.set_sensitive(False)
				self.single_day_entry.set_text("")
				self.hide_calendar_message_items()
	
	#def day_toggled_button

	def month_changed(self,widget):	

		self.calendar.select_day(0)
		self.calendar.clear_marks()

		if  self.clear_days:
			self.marked_range_days(0)
		else:
			date=self.range_day1_entry.get_text()
			if date!="":
				month_ref=self.calendar.get_date().month
				year_ref=self.calendar.get_date().year	

				split_date=self._splited_date(date)
				tmp_day=split_date[0]
				tmp_month=split_date[1]
				tmp_year=split_date[2]
	
				if tmp_month==month_ref and tmp_year==year_ref:
					self.calendar.mark_day(tmp_day)				
	
	#def month_changed							

	def day_selected(self,widget):
		
		date_selected=self.calendar.get_date()
		day_selected=date_selected.day
		
		if int(day_selected)!=0:
			if day_selected<10:
				day_selectedf="0"+str(day_selected)
			else:
				day_selectedf=day_selected	
			month_selected=date_selected.month+1
			if month_selected<10:
				month_selected="0"+str(month_selected)

			year_selected=date_selected.year
			date_format=str(day_selectedf)+"/"+str(month_selected)+"/"+str(year_selected)

			if not self.range:
				self.calendar.clear_marks()
				self.single_day_entry.set_text(date_format)
				self.range=False
				self.clear_days=True
			else:
				if self.range_day1_entry.get_text()=="":
					self.clear_days=False
					self.calendar.clear_marks()
					self.range_day1_entry.set_text(date_format)
					self.calendar.mark_day(day_selected)
					self.calendar.select_day(0)

				else:
					if self.range_day2_entry.get_text()=="":
						date1=datetime.strptime(self.range_day1_entry.get_text(),"%d/%m/%Y")
						date2=datetime.strptime(date_format,"%d/%m/%Y")
						if date2>date1:
							self.range=True
							self.clear_days=True
							self.range_day2_entry.set_text(date_format)	
							range_day=self.range_day1_entry.get_text()+"-"+self.range_day2_entry.get_text()
							self.marked_range_days(2,range_day)
							self.calendar.select_day(0)
							self.hide_calendar_message_items()
						else:
							self.calendar.select_day(0)
							self.manage_calendar_msg(self.core.mainWindow.get_msg(EditBox.DATE_RANGE_INCONSISTENT_ERROR))	
	#def day_selected						

	def marked_range_days(self,monthref,range_day=None):

		if range_day!=None:
			if self.range:
				self.days_inrange=self.core.bellmanager.get_days_inrange(range_day)

		if monthref==0:
			ref_month=self.calendar.get_date().month
			ref_year=self.calendar.get_date().year

		elif monthref==1:
			if self.range:
				ref_date=self.range_day1_entry.get_text()
			else:
				ref_date=self.single_day_entry.get_text()
				
			split_date=self._splited_date(ref_date)
			ref_month=split_date[1]
			ref_year=split_date[2]

			self.calendar.select_month(ref_month,ref_year)

		else:
			split_date=self._splited_date(self.range_day2_entry.get_text())
			ref_month=split_date[1]
			ref_year=split_date[2]

		if self.range:
			for i in self.days_inrange:
				split_date=self._splited_date(i)
				tmp_day=split_date[0]
				tmp_month=split_date[1]
				tmp_year=split_date[2]
				if tmp_month==ref_month and tmp_year==ref_year:
					self.calendar.mark_day(tmp_day)
			
		else:
			if self.single_day_entry.get_text()!="":
				split_date=self._splited_date(self.single_day_entry.get_text())
				tmp_day=split_date[0]
				tmp_month=split_date[1]
				tmp_year=split_date[2]
				
				if tmp_month==ref_month and tmp_year==ref_year:
					self.calendar.mark_day(tmp_day)		

	#def marked_range_days			

	def _splited_date(self,date):

		splited_date=[]
		tmp_date=date.split("/")
		tmp_day=int(tmp_date[0])
		tmp_month=int(tmp_date[1])-1
		tmp_year=int(tmp_date[2])

		splited_date=[tmp_day,tmp_month,tmp_year]
		
		return splited_date

	#def _splited_date	

	def remove_range(self,widget,typeDate):

		self.calendar.clear_marks()
		self.clear_days=False
		self.calendar.select_day(0)
		if typeDate=="singleDay":
			self.single_day_entry.set_text("")
		else:
			self.range_day1_entry.set_text("")
			self.range_day2_entry.set_text("")
		
		self.hide_calendar_message_items()

	#def remove_range

	def save_day_clicked(self,widget,event=None):

		error=False
		if self.range:
			if self.range_day1_entry.get_text()!="" and self.range_day2_entry.get_text()!="":
				self.validity_entry.set_text(self.range_day1_entry.get_text()+"-"+self.range_day2_entry.get_text())
			else:
				if self.range_day1_entry.get_text()!="" and self.range_day2_entry.get_text()=="":
					error=True
				else:
					self.validity_entry.set_text("")
		else:
			self.validity_entry.set_text(self.single_day_entry.get_text())		

		if not error:
			self.validity=self.validity_entry.get_text()
			self.restore_validity=False
			self.validity_popover.hide()
		else:
			self.manage_calendar_msg(self.core.mainWindow.get_msg(EditBox.DATE_RANGE_INCOMPLETE_ERROR))	

	#def save_day_clicked

	def cancel_day_clicked(self,widget,event=None):

		self.restore_validity=True
		self.validity_popover.hide()

	#def cancel_day_clicked	

	def validity_popover_closed(self,widget,event=None):

		self.restore_validity_popover()
			
	#def validity_popover_closed

	def restore_validity_popover(self):

		if self.restore_validity:
			self.load_current_validity()

	#def restore_validity_popover		

	def edit_image_clicked(self,widget,event=None):
		
		self.core.mainWindow.hide_message_items()
		self.previous_image_op=self.image_op
		self.restore_img=True
		
		if self.image_op=="stock":
			self.previous_image_path=BANNERS_PATH+self.image_store[self.image_cb.get_active()][1]+".png"
			c=0
			for i in self.image_store:
				if os.path.basename(self.previous_image_path).split(".")[0]==i[1]:
					break
				c+=1
				
			self.previous_image_cb=c		
		else:
			self.previous_image_path=self.image_fc.get_filename()
			self.image_cb.set_active(1)
			if self.previous_image_path==None:
				self.image_popover_apply_bt.set_sensitive(False)
		
		self.image_popover.show_all()
		self.image_popover_error_img.hide()	

	#def edit_image_clicked	
	
	def image_popover_cancel_bt_clicked(self,widget):

		self.restore_img=True
		self.image_popover.hide()

	#def image_popover_cancel_bt_clicked	
	
	def image_popover_apply_bt_clicked(self,widget):	

		self.restore_img=False
		
		if self.image_op=="stock":
			path=BANNERS_PATH+self.image_store[self.image_cb.get_active()][1]+".png"
		else:
			path=self.image_fc.get_filename()
		
		self.render_bell_image(path)
		
		self.image_popover.hide()

	#def image_popover_apply_bt_clicked(self,widget)		

	def render_bell_image(self,path):

		image=Gtk.Image()
		image.set_from_file(path)
		pixbuf=image.get_pixbuf()
		pixbuf=pixbuf.scale_simple(80,80,GdkPixbuf.InterpType.BILINEAR)
		self.image_bell.set_from_pixbuf(pixbuf)

	#def render_bell_image	

	def image_popover_closed(self,widget,event=None):

		self.restore_image_popover()
			
	#def image_popover_closed		

	def restore_image_popover(self):
	
		if self.restore_img:

			if self.previous_image_op=="stock":
				self.stock_rb.set_active(True)
				self.image_cb.set_active(self.previous_image_cb)
			else:
				self.custom_rb.set_active(True)
				self.image_fc.set_filename(self.previous_image_path)


			self.image_path=self.previous_image_path

	#def restore_image_popover		

	def mouse_over_image(self,widget,event=None):

		self.image_box.set_name("IMAGE_BOX_HOVER")

	#def mouse_over_image

	def mouse_exit_image(self,widget,event=None):

		self.image_box.set_name("IMAGE_BOX")

	#def mouse_exit_image		

	def sound_edit_button_clicked (self,widget):
		
		self.core.mainWindow.hide_message_items()
		self.restore_sound=True
		self.previous_sound_op=self.sound_op
		self.previous_sound_path=self.get_sound_path(self.sound_op,False)
		if self.sound_op=="file":
			if self.previous_sound_path==None:
				self.sound_popover_apply_bt.set_sensitive(False)
			else:
				self.sound_popover_apply_bt.set_sensitive(True)	
		self.sound_popover.show_all()
		self.sound_popover_error_img.hide()

	#def sound_edit_button_clicked	

	def sound_popover_apply_bt_clicked(self,widget):
	
		self.restore_sound=False
		self.previous_sound_op=self.sound_op
		self.previous_sound_path=self.get_sound_path(self.sound_op,False)

		self.sound_op_label.set_text(self.get_sound_option_label(self.sound_op))
		self.sound_path_label.set_name("SOUND_PATH_LABEL")
		try:
			self.sound_path_label.set_text(self.get_sound_path(self.sound_op,True))
		except:
			self.sound_path_label.set_text(_("<specify the file/url for the sound>"))


		self.sound_popover.hide()

	#def sound_popover_apply_bt_clicked	

	def sound_popover_cancel_bt_clicked(self,widget):

		self.restore_sound=True
		self.sound_popover.hide()

	#def image_popover_cancel_bt_clicked	

	def sound_popover_closed(self,widget,event=None):

		self.restore_sound_popover()

	#def sound_popover_closed		


	def restore_sound_popover(self):
	
		if self.restore_sound:

			self.localpath_cb.set_active(False)
			
			if self.previous_sound_op=="file":
				self.file_rb.set_active(True)
				self.localpath_cb.set_sensitive(True)
				
				try:
					self.sound_fc.set_filename(self.previous_sound_path)
				
					if self.core.sounds_path in self.previous_sound_path:
						self.localpath_cb.set_sensitive(False)
						self.localpath_cb.set_active(True)
				except:
					pass	
			elif self.previous_sound_op=="directory":
				self.localpath_cb.set_sensitive(False)
				self.directory_rb.set_active(True)
				try:
					self.sound_dc.set_filename(self.previous_sound_path)
				except:
					pass	
			elif self.previous_sound_op=="url":
				self.localpath_cb.set_sensitive(False)
				self.url_rb.set_active(True)
				self.sound_url.set_text(self.previous_sound_path)
			elif self.previous_sound_op=="urllist":
				self.localpath_cb.set_sensitive(False)
				self.urlslist_rb.set_active(True)
				try:
					self.sound_urllist.set_filenanme(self.previous_sound_path)
				except:
					pass	
					
	#def restore_sound_popover	

	def get_sound_option_label(self,option):

		if option=="file":
			text=(_("Sound file"))
		elif option=="directory":
			text=(_("Random from directory"))
		elif option=="url":
			text=(_("YouTube url"))	
		elif option=="urlslist":	
			text=(_("Random from urls list"))

		return text	

	#def get_sound_option_label	

	def get_sound_path(self,option,basename):
	
		if option=="file":
			path=self.sound_fc.get_filename()
			if basename:
				if path!=None:
					path=os.path.basename(path)
		elif option=="directory":
			path=self.sound_dc.get_filename()
		elif option=="url":
			path=self.sound_url.get_text().split('\n')[0]
		elif option=="urlslist":	
			path=self.sound_urlslist.get_filename()

		return path			

	#def get_sound_path

	def start_edit_bt_clicked(self,button):
		
		self.core.mainWindow.hide_message_items()
		self.restore_start_time=True
		self.previous_start_time=self.start_time_spinbutton.get_value_as_int()
		self.start_popover.show_all()
	
	#def start_edit_bt_clicked	

	def start_popover_apply_bt_clicked(self,button):

		self.start_entry_label.set_text(str(self.start_time_spinbutton.get_value_as_int()))
		self.restore_start_time=False
		self.start_popover.hide()

	#def start_popover_apply_bt	

	def start_popover_cancel_bt_clicked(self,button):

		self.restore_start_time=True
		self.start_popover.hide()

	#def start_popover_cancel_bt	
		
	def start_popover_closed(self,widget,event=None):

		self.restore_start_popover()

	#def start_popover_closed
	
	def restore_start_popover(self):

		if self.restore_start_time:
			self.start_time_spinbutton.set_value(self.previous_start_time)

	#def restore_start_time		

	def duration_edit_bt_clicked(self,button):

		self.core.mainWindow.hide_message_items()
		self.restore_duration=False
		self.previous_duration=self.duration_spinbutton.get_value_as_int()
		self.duration_popover.show_all()
	
	#def duration_edit_bt_clicked	

	def duration_popover_apply_bt_clicked(self,button):

		duration=self.duration_spinbutton.get_value_as_int()
		self.manage_duration_entry_label(duration)
		self.restore_duration=False
		self.duration_popover.hide()

	#def duration_popover_apply_bt	

	def duration_popover_cancel_bt_clicked(self,button):

		self.restore_duration=True
		self.duration_popover.hide()

	#def duration_popover_cancel_bt	
		
	def duration_popover_closed(self,widget,event=None):

		self.restore_duration_popover()

	#def duration_popover_closed
	
	def restore_duration_popover(self):

		if self.restore_duration:
			self.duration_spinbutton.set_value(self.previous_duration)

	#def restore_duration_time		

	def manage_duration_entry_label(self,duration):

		if duration==0:
			self.duration_entry_label.set_text(_("Full reproduction"))
			self.duration_second_label.hide()
		else:
			self.duration_entry_label.set_text(str(duration))
			self.duration_second_label.show()

	#def manage_duration_entry_label

	def manage_calendar_msg(self,msg):

		self.calendar_error_img.show()
		self.calendar_message_box.set_name("ERROR_BOX")
		self.calendar_message_label.set_text(msg)
		self.calendar_message_label.show()

	#def manage_calendar_msg

	def hide_calendar_message_items(self):

		self.calendar_message_box.set_name("HIDE_BOX")
		self.calendar_error_img.hide()
		self.calendar_message_label.set_text("")

	#def hide_calendar_message_items
		
#class EditBox

from . import Core
