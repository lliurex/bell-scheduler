#!/usr/bin/python3
import os
import sys
from PySide2 import QtCore, QtGui, QtQml

class AudioDevicesModel(QtCore.QAbstractListModel):

	IdAuidoDeviceRole= QtCore.Qt.UserRole + 1000
	NameAudioDeviceRole=QtCore.Qt.UserRole + 1001

	def __init__(self,parent=None):
		
		super(AudioDevicesModel, self).__init__(parent)
		self._entries =[]
	
	#def __init__

	def rowCount(self, parent=QtCore.QModelIndex()):
		
		if parent.isValid():
			return 0
		return len(self._entries)

	#def rowCount

	def data(self, index, role=QtCore.Qt.DisplayRole):
		
		if 0 <= index.row() < self.rowCount() and index.isValid():
			item = self._entries[index.row()]
			if role == AudioDevicesModel.IdAudioDeviceRole:
				return item["idAudioDevice"]
			if role == AudioDevicesModel.NameAudioDeviceRole:
				return item["nameAudioDevice"]
	#def data

	def roleNames(self):
		
		roles = dict()
		roles[AudioDevicesModel.IdAudioDeviceRole] = b"idAudioDevice"
		roles[AudioDevicesModel.NameAudioDeviceRole] = b"nameAudioDevice"
	

		return roles

	#def roleNames

	def appendRow(self,iad,nad):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["idAudioDevice"])
		if iad not in tmpId:
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(idAudioDevice=idAudioDevice,nameAudioDevice=nad))
			self.endInsertRows()

	#def appendRow

	def removeRow(self,index):
		self.beginRemoveRows(QtCore.QModelIndex(),index,index)
		self._entries.pop(index)
		self.endRemoveRows()
	
	#def removeRow

	def clear(self):
		
		count=self.rowCount()
		self.beginRemoveRows(QtCore.QModelIndex(), 0, count)
		self._entries.clear()
		self.endRemoveRows()
	
	#def clear
	
#class AudioDevicesModel
