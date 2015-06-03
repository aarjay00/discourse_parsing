#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from extract_relations import *
from ssf_api import *

fullStop='\xe0\xa5\xa4'


class discourseUnit():
	def __init__(self,unit,span1,span2):
		self.unit=unit
		self.spanStart=span1
		self.spanEnd=span2
		self.wordList=re.split(' ',unit)
class discourseFile():
	def __init__(self,sentenceList):
		self.sentenceList=sentenceList
	def addDiscourseRelationInfo(self,relationInfo):
		pass
#	def addUnit(self,discourseUnit):
#		self.discourseUnitList.append(discourseUnit)
#	def addDiscourseRelationList(self,discourseRelationList):
#		self.discourseRelationList=discourseRelationList
#	def addSSFData(self,ssf):
#		self.SSFData=ssf


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
	return discourseFileInst


if len(sys.argv)<2:
	print "Please give folder location"
	exit()
dataLocation=sys.argv[1]
rawFileList=folderWalk(dataLocation+"/raw")
annFileList=folderWalk(dataLocation+"/ann")
connList=loadConnList("connectives/compConnectiveList.list")
connSplitList=loadConnList("connectives/splitConnectiveList.list",True)
discourseFileCollection=[]
for rawFile in rawFileList:
#	fd=codecs.open(rawFile,"r",encoding="utf-8")
#	discourseFileInst=processRawFile(fd.read(),connList,connSplitList,[])
	sentenceList=extractSSFannotations(rawFile)
	discourseFileInst=discourseFile(sentenceList)
	discourseFileInst.addDiscourseRelationInfo(extractRelation(rawFile))
	discourseFileCollection.append(discourseFileInst)
#	fd.close()
