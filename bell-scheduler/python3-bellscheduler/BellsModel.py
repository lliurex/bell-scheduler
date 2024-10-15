#!/usr/bin/python3
import os
import sys
from PySide6 import QtCore, QtGui, QtQml

class BellsModel(QtCore.QAbstractListModel):

	IdRole= QtCore.Qt.UserRole + 1000
	CronRole=QtCore.Qt.UserRole+1001
	MoRole=QtCore.Qt.UserRole+1002
	TuRole=QtCore.Qt.UserRole+1003
	WeRole=QtCore.Qt.UserRole+1004
	ThRole=QtCore.Qt.UserRole+1005
	FrRole=QtCore.Qt.UserRole+1006
	ValidityRole=QtCore.Qt.UserRole+1007
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
			elif role == BellsModel.MoRole:
				return item["mo"]
			elif role == BellsModel.TuRole:
				return item["tu"]
			elif role == BellsModel.WeRole:
				return item["we"]
			elif role == BellsModel.ThRole:
				return item["th"]
			elif role == BellsModel.FrRole:
				return item["fr"]
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
		roles[BellsModel.MoRole] = b"mo"
		roles[BellsModel.TuRole] = b"tu"
		roles[BellsModel.WeRole] = b"we"
		roles[BellsModel.ThRole] = b"th"
		roles[BellsModel.FrRole] = b"fr"
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

	def appendRow(self,i,cr,mo,tu,we,th,fr,va,vs,im,na,so,bs,mi,ise,iie):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["id"])
		tmpN=na.strip()
		if i not in tmpId and na !="" and len(tmpN)>0:
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(id=i,cron=cr,mo=mo,tu=tu,we=we,th=th,fr=fr,validity=va,validityActivated=vs,img=im,name=na,sound=so,bellActivated=bs,metaInfo=mi,isSoundError=ise,isImgError=iie))
			self.endInsertRows()

	#def appendRow

	def removeRow(self,index):
		self.beginRemoveRows(QtCore.QModelIndex(),index,index)
		self._entries.pop(index)
		self.endRemoveRows()
	
	#def removeRow

	def setData(self, index, param, value, role=QtCore.Qt.EditRole):
		
		if role == QtCore.Qt.EditRole:
			row = index.row()
			if param in ["bellActivated"]:
				if self._entries[row][param]!=value:
					self._entries[row][param]=value
					self.dataChanged.emit(index,index)
					return True
				else:
					return False
			else:
				return False
	
	#def setData

	def clear(self):
		
		count=self.rowCount()
		self.beginRemoveRows(QtCore.QModelIndex(), 0, count)
		self._entries.clear()
		self.endRemoveRows()
	
	#def clear
	
#class BellsModel
