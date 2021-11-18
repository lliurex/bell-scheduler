#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, GdkPixbuf, Gdk, Gio, GObject,GLib

import sys
import os


from . import settings
import gettext
gettext.textdomain(settings.TEXT_DOMAIN)
_ = gettext.gettext


class BellBox(Gtk.VBox):
	
	def __init__(self):
		
		Gtk.VBox.__init__(self)
		
		self.core=Core.Core.get_core()
		
		builder=Gtk.Builder()
		builder.set_translation_domain(settings.TEXT_DOMAIN)
		ui_path=self.core.ui_path
		builder.add_from_file(ui_path)

		self.css_file=self.core.rsrc_dir+"bell-scheduler.css"
		self.edit_image=self.core.rsrc_dir+"edit.svg"
		self.manage_bell_image=self.core.rsrc_dir+"manage_bell.svg"
		self.delete_image=self.core.rsrc_dir+"trash.svg"
		self.main_box=builder.get_object("bell_data_box")
		self.bell_box=builder.get_object("bell_box")
		self.scrolledwindow=builder.get_object("scrolledwindow")
		self.bell_list_box=builder.get_object("bell_list_box")
		self.bell_list_vp=builder.get_object("bell_list_viewport")
		self.image_nodisp=self.core.rsrc_dir+"image_nodisp.svg"
		self.pack_start(self.main_box,True,True,0)
		self.set_css_info()
				
	#def __init__

	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()

		f=Gio.File.new_for_path(self.css_file)
		self.style_provider.load_from_file(f)

		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.bell_list_box.set_name("BELL_LIST")			
	#def set_css_info			
			
	def init_bell_list(self):
	
		self.alarms_error=0
		tmp=self.core.bellBox.bell_list_box.get_children()
		for item in tmp:
			self.bell_list_box.remove(item)

	#def init_bell_list
			

	def draw_bell(self,search,args=None):

		self.init_bell_list()
		self.search_box=search
		if not self.search_box:
			self.bells_list=self.core.mainWindow.bells_info
			order=self.core.mainWindow.order_bells		
		else:
			self.bells_list=self.core.mainWindow.search_list
			order=self.core.mainWindow.search_order

		last_change=args
		count=len(self.bells_list)
		for item in order:
			self.new_bell_box(item,count,last_change)
			count-=1		
		
		if self.alarms_error>0:
			self.core.mainWindow.manage_message(True,-31)	

	#def draw_bell		

	def new_bell_box(self,id_bell,count,args=None):

		self.days_on=0
		self.error_sound=False
		self.error_image=False

		bell_vbox=Gtk.VBox()
		hbox=Gtk.HBox()
		hbox_cron=Gtk.VBox()
		hour_info=self.core.bellmanager.format_time(id_bell)[2]
		bell_hour=Gtk.Label()
		bell_hour.set_text(hour_info)
		bell_hour.set_name("TIME_LABEL")
		bell_hour.set_margin_left(15)
		bell_hour.set_margin_right(15)
		bell_hour.set_margin_top(5)
		bell_hour.set_margin_bottom(0)
		bell_hour.id=id_bell
		
		hbox_week=Gtk.HBox()
		monday_inf=Gtk.Label()
		monday_inf.set_text(_("M"))
		monday_inf.set_margin_left(10)
		monday_inf.set_margin_bottom(12)
		monday_inf.set_width_chars(2)
		monday_inf.set_max_width_chars(2)
		monday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],0)
		monday_inf.set_name(day_css)

		thuesday_inf=Gtk.Label()
		thuesday_inf.set_text(_("T"))
		thuesday_inf.set_margin_left(1)
		thuesday_inf.set_margin_bottom(12)
		thuesday_inf.set_width_chars(2)
		thuesday_inf.set_max_width_chars(2)
		thuesday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],1)
		thuesday_inf.set_name(day_css)

		wednesday_inf=Gtk.Label()
		wednesday_inf.set_text(_("W"))
		wednesday_inf.set_margin_left(1)
		wednesday_inf.set_margin_bottom(12)
		wednesday_inf.set_width_chars(2)
		wednesday_inf.set_max_width_chars(2)
		wednesday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],2)
		wednesday_inf.set_name(day_css)

		thursday_inf=Gtk.Label()
		thursday_inf.set_text(_("R"))
		thursday_inf.set_margin_left(1)
		thursday_inf.set_margin_bottom(12)
		thursday_inf.set_width_chars(2)
		thursday_inf.set_max_width_chars(2)
		thursday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],3)
		thursday_inf.set_name(day_css)

		friday_inf=Gtk.Label()
		friday_inf.set_text(_("F"))
		friday_inf.set_margin_left(1)
		friday_inf.set_margin_bottom(12)
		friday_inf.set_width_chars(2)
		friday_inf.set_max_width_chars(2)
		friday_inf.id=id_bell
		day_css=self.format_weekdays(self.bells_list[id_bell],4)
		friday_inf.set_name(day_css)

		hbox_week.pack_start(monday_inf,False,False,2)
		hbox_week.pack_start(thuesday_inf,False,False,2)
		hbox_week.pack_start(wednesday_inf,False,False,2)
		hbox_week.pack_start(thursday_inf,False,False,2)
		hbox_week.pack_start(friday_inf,False,False,2)

		image=Gtk.Image()
		pixbuf=self.format_image_size(id_bell)
		image=Gtk.Image.new_from_pixbuf(pixbuf)
		image.set_margin_left(30)
		image.set_halign(Gtk.Align.CENTER)
		image.set_valign(Gtk.Align.CENTER)
		image_id=id_bell

		hbox_description=Gtk.VBox()
		description=Gtk.Label()
		description.set_text(self.bells_list[id_bell]["name"])
		description.set_margin_left(10)
		description.set_margin_right(5)
		description.set_margin_top(20)
		description.set_margin_bottom(1)
		description.set_width_chars(20)
		description.set_max_width_chars(20)
		description.set_xalign(-1)
		description.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
		description.set_name("BELL_DESCRIPTION")
		description.set_valign(Gtk.Align.START)

		sound=Gtk.Label()
		sound_path=self.load_sound_path(id_bell)
		sound.set_text(sound_path)
		sound.set_margin_left(10)
		sound.set_margin_right(5)
		sound.set_margin_bottom(15)
		sound.set_width_chars(40)
		sound.set_max_width_chars(40)
		sound.set_xalign(-1)
		sound.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
		
		sound.set_valign(Gtk.Align.START)
		hbox_description.pack_start(description,False,False,15)
		hbox_description.pack_start(sound,False,False,1)

		manage_bell=Gtk.Button()
		manage_bell_image=Gtk.Image.new_from_file(self.manage_bell_image)
		manage_bell.add(manage_bell_image)
		manage_bell.set_margin_right(15)
		manage_bell.set_halign(Gtk.Align.CENTER)
		manage_bell.set_valign(Gtk.Align.CENTER)
		manage_bell.set_name("EDIT_ITEM_BUTTON")
		manage_bell.connect("clicked",self.manage_bell_options,hbox)
		manage_bell.set_tooltip_text(_("Manage bell"))

		popover = Gtk.Popover()
		manage_bell.popover=popover
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		edit_box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		edit_box.set_margin_left(10)
		edit_box.set_margin_right(10)
		edit_eb=Gtk.EventBox()
		edit_eb.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
		edit_eb.connect("button-press-event", self.edit_bell_clicked,hbox)
		edit_eb.connect("motion-notify-event", self.mouse_over_popover)
		edit_eb.connect("leave-notify-event", self.mouse_exit_popover)
		edit_label=Gtk.Label()
		edit_label.set_text(_("Edit bell"))
		edit_eb.add(edit_label)
		edit_eb.set_name("POPOVER_OFF")
		edit_box.add(edit_eb)
		
		delete_box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		delete_box.set_margin_left(10)
		delete_box.set_margin_right(10)
		delete_eb=Gtk.EventBox()
		delete_eb.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
		delete_eb.connect("button-press-event", self.delete_bell_clicked,hbox,bell_vbox)
		delete_eb.connect("motion-notify-event", self.mouse_over_popover)
		delete_eb.connect("leave-notify-event", self.mouse_exit_popover)
		delete_label=Gtk.Label()
		delete_label.set_text(_("Delete bell"))
		delete_eb.add(delete_label)
		delete_eb.set_name("POPOVER_OFF")
		delete_box.add(delete_eb)

		vbox.pack_start(edit_box, True, True,8)
		vbox.pack_start(delete_box, True, True,8)
		
		vbox.show_all()
		popover.add(vbox)
		popover.set_position(Gtk.PositionType.BOTTOM)
		popover.set_relative_to(manage_bell)


		switch_button=Gtk.Switch()
		switch_button.set_halign(Gtk.Align.CENTER)
		switch_button.set_valign(Gtk.Align.CENTER)
		switch_button.set_tooltip_text(_("Activate or deactivate bell"))
		
		if not self.error_sound:
			sound.set_name("BELL_SOUND")
			if self.days_on>0:	
				if self.bells_list[id_bell]["active"]:
					switch_button.set_active(True)
			else:
				switch_button.set_sensitive(False)
		else:
			sound.set_name("BELL_ERROR_SOUND")
			switch_button.set_sensitive(False)
			switch_button.set_active(False)
			
			if self.bells_list[id_bell]["active"]:
				try:
					self.core.mainWindow.bells_info[id_bell]["active"]=False
					self.core.bellmanager.save_conf(self.core.mainWindow.bells_info,id_bell,"active")
				except:
					pass
		switch_button.connect("notify::active",self.on_switch_activaded,hbox)

		hbox_cron.pack_start(bell_hour,False,False,5)
		hbox_cron.pack_end(hbox_week,False,False,5)
		hbox.pack_start(hbox_cron,False,False,5)
		hbox.pack_start(image,False,False,5)
		hbox.pack_start(hbox_description,False,False,5)
		hbox.pack_end(manage_bell,False,False,5)
		
		hbox.pack_end(switch_button,False,False,5)
		hbox.show_all()

		list_separator=Gtk.Separator()
		list_separator.set_margin_top(5)
		list_separator.set_margin_left(20)
		list_separator.set_margin_right(20)

		if count!=1:
			list_separator.set_name("SEPARATOR")
		else:
			list_separator.set_name("WHITE_SEPARATOR")	


		bell_vbox.pack_start(hbox,False,False,0)
		bell_vbox.pack_end(list_separator,False,False,0)
		bell_vbox.show_all()

		if str(id_bell)==str(args):
			bell_vbox.set_name("CHANGE_BOX")
		else:
			if not self.error_sound and not self.error_image:
				bell_vbox.set_name("APP_BOX")
			else:
				self.alarms_error+=1
				bell_vbox.set_name("APP_ERROR_BOX")	
		self.bell_list_box.pack_start(bell_vbox,False,False,0)
		self.bell_list_box.queue_draw()
		bell_vbox.queue_draw()	

	#def new_bell_box	
		
	def format_weekdays(self,bell,day):
		
		weekdays=bell["weekdays"]
		day_f=weekdays[str(day)]
		if day_f:
			self.days_on+=1
			return("DAY_LABEL_ON")
		else:
			return("DAY_LABEL_OFF")	

	#def format_weekdays		


	def load_sound_path(self,bell):
		
		path=self.bells_list[bell]["sound"]["path"]
		option=self.bells_list[bell]["sound"]["option"]

		
		if option!="url":
			if os.path.exists(path):
				if option=="file":
					file=os.path.basename(path)
					return file
				else:
					return path	
			else:
				self.error_sound=True
				msg=self.core.mainWindow.get_msg(29)
				self.core.mainWindow.loading_errors=True
				return msg	
		else:
				return path

	#def load_sound_path			
		
	def format_image_size(self,bell):

		image_path=self.bells_list[bell]["image"]["path"]
		image=Gtk.Image()
		if os.path.exists(image_path):
			image.set_from_file(image_path)
		else:
			self.error_image=True
			image.set_from_file(self.image_nodisp)
			self.core.mainWindow.loading_errors=True

		pixbuf=image.get_pixbuf()
		pixbuf=pixbuf.scale_simple(80,80,GdkPixbuf.InterpType.BILINEAR)
		
		return pixbuf

	#def format_image_size	


	def delete_bell_clicked(self,widget,event,hbox,bell_box):

		popover=hbox.get_children()[4].popover.hide()
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING, Gtk.ButtonsType.YES_NO, "BELL SCHEDULER")
		dialog.format_secondary_text(_("Do you want delete the bell?"))
		response=dialog.run()
		dialog.destroy()
		
		if response==Gtk.ResponseType.YES:
			bell_to_remove=hbox.get_children()[0].get_children()[0].id
			self.core.mainWindow.bells_info.pop(bell_to_remove)
			result=self.core.bellmanager.save_conf(self.core.mainWindow.bells_info,bell_to_remove,"remove")
			if result['status']:
				self.bell_list_box.remove(bell_box)
				self.core.mainWindow.manage_message(False,14)
			else:
				self.core.mainWindow.manage_message(True,result['code'])

	#def delete_bell_clicked		
			
		
	def edit_bell_clicked(self,widget,event,hbox):

		popover=hbox.get_children()[4].popover.hide()
		bell_to_edit=hbox		
		bell_to_edit=bell_to_edit.get_children()[0].get_children()[0].id
		self.core.editBox.init_form()
		self.core.editBox.render_form()
		self.core.editBox.load_values(bell_to_edit)
		self.core.mainWindow.manage_menubar(False)
		self.core.mainWindow.manage_down_buttons(True)
		self.core.mainWindow.stack_opt.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
		self.core.mainWindow.stack_opt.set_visible_child_name("editBox")		

	#def edit_bell_clicked		

	def on_switch_activaded (self,switch,gparam,hbox):
		
		self.core.mainWindow.hide_message_items()
		bell_to_edit=hbox		
		bell_to_edit=bell_to_edit.get_children()[0].get_children()[0].id
		turn_on=False

		if switch.get_active():
			self.core.mainWindow.bells_info[bell_to_edit]["active"]=True
			turn_on=True
			
		else:
			self.core.mainWindow.bells_info[bell_to_edit]["active"]=False

		result=self.core.bellmanager.save_conf(self.core.mainWindow.bells_info,bell_to_edit,"active")
		if result['status']:
			if turn_on:
				self.core.mainWindow.manage_message(False,16)
			else:
				self.core.mainWindow.manage_message(False,17)
		else:
			self.core.mainWindow.manage_message(True,result['code'])			

	#def on_switch_activaded	

	def manage_bells_buttons(self,sensitive):
	
		for item in self.bell_list_box:
			item.get_children()[0].get_children()[3].set_sensitive(sensitive)
			item.get_children()[0].get_children()[4].set_sensitive(sensitive)

	#def manage_bells_buttons
	
	def manage_bell_options(self,button,hbox,event=None):
		
		self.core.mainWindow.hide_message_items()
		button.popover.show()

	#def manage_bell_options	

	def mouse_over_popover(self,widget,event=None):

		widget.set_name("POPOVER_ON")

	#def mouser_over_popover	

	def mouse_exit_popover(self,widget,event=None):

		widget.set_name("POPOVER_OFF")		
	

#class BellBox

from . import Core
