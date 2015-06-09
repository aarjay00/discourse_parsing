#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from extract_relations import *
from ssf_api import *
from letter import *
from merge_annotations import *
from identify_connectives import *

class discourseUnit():
	def __init__(self,unit,span1,span2):
		self.unit=unit
		self.spanStart=span1
		self.spanEnd=span2
		self.wordList=re.split(' ',unit)
class discourseFile():
	def __init__(self,sentenceList,globalWordList,rawData):
		self.rawData=rawData
		self.sentenceList=sentenceList
		self.globalWordList=globalWordList
		self.rawToAnnMapping={}
		self.annToRawMapping={}
	def addDiscourseRelationInfo(self,relationList):
		self.relationList=relationList
		(self.rawToAnnMapping,self.annToRawMapping)=mappingBetweenFiles(self.globalWordList,self.rawData)
		relationNum=0
		for relation in self.relationList:
			if(relation.relationType != "Explicit" and relation.relationType!="AltLex"):
				continue
			print relation.relationType
			print "arg1",relation.arg1Span
			printSpan(relation.arg1Span,self.rawData)
			arg1=getSpanFromAnn(relation.arg1Span,self.rawData,self.globalWordList,self.annToRawMapping,self.rawToAnnMapping)
			for pos in arg1:
				self.globalWordList[pos].arg1=True
				self.globalWordList[pos].relationNum=relationNum
			print "connective",relation.connSpan
			isSplitConn=printSpan(relation.connSpan,self.rawData)
			conn=getSpanFromAnn(relation.connSpan,self.rawData,self.globalWordList,self.annToRawMapping,self.rawToAnnMapping)
			for pos in conn:
				if(isSplitConn):
					print "huihui"
					self.globalWordList[pos].splitConn=True
				else:
					self.globalWordList[pos].conn=True
				self.globalWordList[pos].relationNum=relationNum
			print "arg2",relation.arg2Span
			printSpan(relation.arg2Span,self.rawData)
			arg2=getSpanFromAnn(relation.arg2Span,self.rawData,self.globalWordList,self.annToRawMapping,self.rawToAnnMapping)
			for pos in arg2:
				self.globalWordList[pos].arg2=True
				self.globalWordList[pos].relationNum=relationNum
			relationNum+=1
		return
def printSpan(spans,rawData):
	split=False
	spans=re.split(';',spans)
	if(len(spans)>1):
		split=True
	for span in spans:
		span=re.split("\.\.",span)
#		print span
		print rawData[int(span[0]):int(span[1])],"-"
	return split

		
def getSpan(span,data):
	finalSpan=[]
	spans=(span.split(";"))
	for span  in spans:
		span=span.split("..")
		finalSpan.append(re.split(' ',data[int(span[0]):int(span[1])]))
	return finalSpan


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
fileNum=0
for rawFile in rawFileList:
	fd=codecs.open(rawFile,"r",encoding="utf-8")
#	discourseFileInst=processRawFile(fd.read(),connList,connSplitList,[])
	(sentenceList,globalWordList)=extractSSFannotations(rawFile)
	if(sentenceList==None or globalWordList==None):
		print "Continuing"
		continue
	discourseFileInst=discourseFile(sentenceList,globalWordList,fd.read())
	discourseFileInst.addDiscourseRelationInfo(extractRelation(rawFile))
	discourseFileCollection.append(discourseFileInst)
	identifyConnectives(discourseFileInst,connList,connSplitList)
	fd.close()
	fileNum+=1
	print "*"*90,fileNum,"files done"

print "processed %d files correctly"%(fileNum)
#for discourseFileInst in discourseFileCollection:
#	identifyConnectives(discourseFileInst,connList,connSplitList)
