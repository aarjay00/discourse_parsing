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

class discourseUnit():
	def __init__(self,unit,span1,span2):
		self.unit=unit
		self.spanStart=span1
		self.spanEnd=span2
		self.wordList=re.split(' ',unit)
class discourseFile():
	def __init__(self,rawFileName,sentenceList,globalWordList,rawData):
		self.rawFileName=rawFileName
		self.rawData=rawData
		self.sentenceList=sentenceList
		self.globalWordList=globalWordList
		self.relationList=[]
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
			print arg1
			for pos in arg1:
				relation.arg1List.append(pos)
				self.globalWordList[pos].arg1=True
				self.globalWordList[pos].relationNum=relationNum
		
			print "arg2",relation.arg2Span
			printSpan(relation.arg2Span,self.rawData)
			arg2=getSpanFromAnn(relation.arg2Span,self.rawData,self.globalWordList,self.annToRawMapping,self.rawToAnnMapping)
			print arg2
			for pos in arg2:
				relation.arg2List.append(pos)
				self.globalWordList[pos].arg2=True
				self.globalWordList[pos].relationNum=relationNum
			print "connectivez",relation.connSpan
			isSplitConn=printSpan(relation.connSpan,self.rawData)
			conn=getSpanFromAnn(relation.connSpan,self.rawData,self.globalWordList,self.annToRawMapping,self.rawToAnnMapping)
			print conn
			print "---",
			connective=getSpan(conn,self.globalWordList)
			connList=connList=loadConnList("lists/compConnectiveList.list")
			if(connective not in connList and not isSplitConn):
				print "FIX THIS!!!!",connective
			for pos in conn:
			 	if(self.globalWordList[pos].word=="," or self.globalWordList[pos].word=="।"):
			 		print "gagaga",connective
					continue
				relation.connList.append(pos)
				if(isSplitConn):
					print "huihui"
					self.globalWordList[pos].splitConn=True
				else:
					self.globalWordList[pos].conn=True
				self.globalWordList[pos].sense=relation.sense
				self.globalWordList[pos].relationNum=relationNum
				self.globalWordList[pos].arg1Span=arg1
				self.globalWordList[pos].arg2Span=arg2
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
