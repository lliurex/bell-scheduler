#!/usr/bin/python3
import os
import sys
from PySide6 import QtCore, QtGui, QtQml

class ImagesModel(QtCore.QAbstractListModel):

	ImageSourceRole= QtCore.Qt.UserRole + 1000
		
	def __init__(self,parent=None):
		
		super(ImagesModel, self).__init__(parent)
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
			if role == ImagesModel.ImageSourceRole:
				return item["imageSource"]
	#def data

	def roleNames(self):
		
		roles = dict()
		roles[ImagesModel.ImageSourceRole] = b"imageSource"
		return roles

	#def roleNames

	def appendRow(self,ims):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["imageSource"])
		if ims not in tmpId and ims !="":
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(imageSource=ims))
			self.endInsertRows()

	#def appendRow

	def clear(self):
		
		count=self.rowCount()
		self.beginRemoveRows(QtCore.QModelIndex(), 0, count)
		self._entries.clear()
		self.endRemoveRows()
	
	#def clear
	
#class ImagesModel
