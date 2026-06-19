#!/usr/bin/python3
import os
import sys
from PySide6 import QtCore, QtGui, QtQml

class BellsModel(QtCore.QAbstractListModel):

	IdRole= QtCore.Qt.UserRole + 1000
	CronRole=QtCore.Qt.UserRole+1001
	WeekDaysRole=QtCore.Qt.UserRole+1003
	ValidityRole=QtCore.Qt.UserRole+1004
	ValidityActivatedRole=QtCore.Qt.UserRole+1008
	ImgRole=QtCore.Qt.UserRole+1009
	NameRole= QtCore.Qt.UserRole + 1010
	SoundRole=QtCore.Qt.UserRole+1011
	BellActivatedRole=QtCore.Qt.UserRole+1012
	MetaInfoRole=QtCore.Qt.UserRole+1014
	IsSoundErrorRole=QtCore.Qt.UserRole+1015
	IsImgErrorRole=QtCore.Qt.UserRole+1016
	
	def __init__(self,parent=None):
		
		super(BellsModel, self).__init__(parent)
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
			if role == BellsModel.IdRole:
				return item["id"]
			elif role == BellsModel.CronRole:
				return item["cron"]
			elif role == BellsModel.WeekDaysRole:
				return item["weekDays"]
			elif role == BellsModel.ValidityRole:
				return item["validity"]
			elif role == BellsModel.ValidityActivatedRole:
				return item["validityActivated"]
			elif role == BellsModel.ImgRole:
				return item["img"]
			elif role == BellsModel.NameRole:
				return item["name"]
			elif role == BellsModel.SoundRole:
				return item["sound"]
			elif role == BellsModel.BellActivatedRole:
				return item["bellActivated"]
			elif role == BellsModel.MetaInfoRole:
				return item["metaInfo"]
			elif role == BellsModel.IsSoundErrorRole:
				return item["isSoundError"]
			elif role == BellsModel.IsImgErrorRole:
				return item["isImgError"]

	#def data

	def roleNames(self):
		
		roles = dict()
		roles[BellsModel.IdRole] = b"id"
		roles[BellsModel.CronRole] = b"cron"
		roles[BellsModel.WeekDaysRole] = b"weekDays"
		roles[BellsModel.ValidityRole] = b"validity"
		roles[BellsModel.ValidityActivatedRole] = b"validityActivated"
		roles[BellsModel.ImgRole]= b"img"
		roles[BellsModel.NameRole] = b"name"
		roles[BellsModel.SoundRole] = b"sound"
		roles[BellsModel.BellActivatedRole] = b"bellActivated"
		roles[BellsModel.MetaInfoRole]=b"metaInfo"
		roles[BellsModel.IsSoundErrorRole]=b"isSoundError"
		roles[BellsModel.IsImgErrorRole]=b"isImgError"
		
		return roles

	#def roleNames

	def appendRow(self,bellId,cron,weekdays,validity,validityActivated,image,name,sound,bellActivated,metaInfo,isSoundError,isImageError):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["id"])
		tmpN=name.strip()
		if bellId not in tmpId and name !="" and len(tmpN)>0:
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(id=bellId,cron=cron,weekDays=weekdays,validity=validity,validityActivated=validityActivated,img=image,name=name,sound=sound,bellActivated=bellActivated,metaInfo=metaInfo,isSoundError=isSoundError,isImgError=isImageError))
			self.endInsertRows()

	#def appendRow

	def removeRow(self,index):

		self.beginRemoveRows(QtCore.QModelIndex(),index,index)
		self._entries.pop(index)
		self.endRemoveRows()
	
	#def removeRow

	def setData(self, index, param, valueToUpdate, role=QtCore.Qt.EditRole):

		if role != QtCore.Qt.EditRole or not index.isValid():
			return

		row = index.row()
		validParams=["bellActivated"]
		changesMade=False

		if param in validParams:
			if self._entries[row][param]!=valueToUpdate:
				self._entries[row][param]=valueToUpdate
				changesMade=True
		
		if changesMade:
			self.dataChanged.emit(index,index)
	
	#def setData

	def clear(self):
		
		count=self.rowCount()
		self.beginRemoveRows(QtCore.QModelIndex(), 0, count)
		self._entries.clear()
		self.endRemoveRows()
	
	#def clear
	
#class BellsModel
