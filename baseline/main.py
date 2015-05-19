#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from extract_relations import *
fullStop='\xe0\xa5\xa4'


class discourseUnit():
	def __init__(self,unit,span1,span2):
		self.unit=unit
		self.spanStart=span1
		self.spanEnd=span2
		self.wordList=re.split(unit," ")
class discourseFile():
	def __init__(self):
		self.discourseUnitList=[]
	def addUnit(self,discourseUnit):
		self.discourseUnitList.append(discourseUnit)

def processRawFile(data,connList,connSplitList,extraDelimiters):
	extraDelimiters.append(fullStop)
	discourseUnits=getDiscourseUnit(data,extraDelimiters)
	spans=findAllOccurences(extraDelimiters,data)
	spans.insert(0,0)
	spans.append(len(data))
	num=0
	discourseFileInst=discourseFile()
	for unit in discourseUnits :
		unit=discourseUnit(unit,spans[num],[num+1])
		discourseFileInst.addUnit(unit)
		num+=1


if len(sys.argv)<2:
	print "Please give folder location"
	exit()
dataLocation=sys.argv[1]
rawFileList=folderWalk(dataLocation+"/raw")
annFileList=folderWalk(dataLocation+"/ann")
connList=loadConnList("connectives/compConnectiveList.list")
connSplitList=loadConnList("connectives/splitConnectiveList.list",True)
for rawFile in rawFileList:
	fd=open(rawFile,"r")
	processRawFile(fd.read(),connList,connSplitList,[])
	fd.close()
