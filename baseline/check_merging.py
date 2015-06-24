#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from merge_annotations import *
from random import shuffle

discourseFileCollection=loadModel("processedData/annotatedData")

shuffle(discourseFileCollection)
collectionSize=len(discourseFileCollection)/7
for i in range(0,collectionSize):
	discourseFileInst=discourseFileCollection[i]
	print i,discourseFileCollection[i].rawFileName,"-"*60
	rawData=discourseFileInst.rawData
	wordList=discourseFileInst.globalWordList
	rawToAnn=discourseFileInst.rawToAnnMapping
	annToRaw=discourseFileInst.annToRawMapping
	rawData=addSpaces(rawData)
	rawData=rawData[getStartPos(rawData,wordList):]
	rawData=rawData.split()
	for rawPos in range(0,len(rawData)):
		try:
			if(rawData[rawPos]!=wordList[rawToAnn[rawPos][0]].word):
				print "herei"
			print rawData[rawPos],"--",
			for pos in rawToAnn[rawPos]:
				print wordList[pos].word,
			print ""
		except:
			print rawData[rawPos],"--",
			print "done here at",rawData[rawPos]
