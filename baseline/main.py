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
	def __init__(self,sentenceList,globalWordList,rawData):
		self.rawData=rawData
		self.sentenceList=sentenceList
		self.globalWordList=globalWordList
	def addDiscourseRelationInfo(self,relationList):
		self.relationList=relationList
		for relation in self.relationList:
			if(relation.relationType != "Explicit"):
				continue
			print relation.relationType
			print "arg1",relation.arg1Span
			print "connective",relation.connSpan
			print "arg2",relation.arg2Span
			span=convertSpan(relation.arg2Span,self.rawData,self.globalWordList)
			printSpan(relation.arg2Span,self.rawData)
			printSpanWord(span,self.globalWordList)
		i=0
		for word in self.globalWordList:
			print word.word,i,
			i+=1
		i=0
		startString=self.globalWordList[0].word
		for i in range(1,5):
			startString=startString+" "+globalWordList[i].word
		data=self.rawData.replace(fullStop," "+fullStop+" ")
		startDoc=data.find(startString)
		data=data[startDoc:]
		data=re.split('\s+',data)
		print "-"*30
		i=0
		for word in data:
			print word,i,
			i+=1

#	def addUnit(self,discourseUnit):
#		self.discourseUnitList.append(discourseUnit)
#	def addDiscourseRelationList(self,discourseRelationList):
#		self.discourseRelationList=discourseRelationList
#	def addSSFData(self,ssf):
#		self.SSFData=ssf

def printSpan(spans,rawData):
	spans=re.split(';',spans)
	for span in spans:
		span=re.split("\.\.",span)
		print span
		print rawData[int(span[0]):int(span[1])],"-"
def printSpanWord(spans,wordList):
	for span in spans:
		print span[0],span[1]
		for word in wordList[span[0]:span[1]]:
			print word.word,
		print "-"

def convertSpan(spans,rawData,wordList):
	startString=wordList[0].word
	for i in range(1,5):
		startString=startString+" "+wordList[i].word
	startDoc=rawData.find(startString)
	spans=re.split(';',spans)
	returnSpan=[]
	for span in spans:
		span=re.split("\.\.",span)
#		print rawData[int(span[0]):int(span[1])]
		dataBefore=rawData[startDoc:int(span[0])]
		dataAfter=rawData[startDoc:int(span[1])]
		dataBefore=dataBefore.replace(fullStop," "+fullStop+" ")
		dataAfter=dataAfter.replace(fullStop," "+fullStop+" ")
#		print "dataBefore starts--",len(re.split('\s+',dataBefore))
#		i=0
#		for w in re.split(' ',dataBefore):
#			print w,i,
#			i+=1
#		print "dataBefore ends--"
		returnSpan.append((int(len(re.split('\s+',dataBefore)))-1,int(len(re.split('\s+',dataAfter)))))
	return returnSpan

		
def getSpan(span,data):
	finalSpan=[]
	spans=(span.split(";"))
	for span  in spans:
		span=span.split("..")
		finalSpan.append(re.split(' ',data[int(span[0]):int(span[1])]))
	return finalSpan
def findListinList(list1 , list2):
	for i in range(0,len(list1)):
		for j in range(0,len(list2)):
			if(list1[i+j].word!=list2[j]):
				break
		if(list1[i+j].word==list2[j]):
			return i
	return -1


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
	fd=codecs.open(rawFile,"r",encoding="utf-8")
#	discourseFileInst=processRawFile(fd.read(),connList,connSplitList,[])
	(sentenceList,globalWordList)=extractSSFannotations(rawFile)
	if(sentenceList==None or globalWordList==None):
		print "Continuing"
		continue
	discourseFileInst=discourseFile(sentenceList,globalWordList,fd.read())
	discourseFileInst.addDiscourseRelationInfo(extractRelation(rawFile))
	discourseFileCollection.append(discourseFileInst)
	fd.close()
	break
