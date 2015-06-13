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
from annotated_data import *
from feature import *

def searchConn(conn,wordList):
	conn=conn.split()
	pos=0
	posList=[]
	while(pos<len(wordList)-len(conn)+1):
		found=True
		for j in range(0,len(conn)):
			if(conn[j]!=wordList[pos+j].word):
				found=False
				break
		if(found):
			posList.append(pos)
			pos+=len(conn)
		else:
			pos+=1
	return posList

def identifyConnectives(discourseFileInst,connList,connSplitList):
	positiveSet=[]
	negativeSet=[]
	wordList=discourseFileInst.globalWordList
	for conn in connList:
		posList=searchConn(conn,wordList)
		if(len(posList)>0):
			print "found ",conn,len(posList)
			for i in posList:
				for j in range(i,i+len(conn.split())):
					print wordList[j].chunkNum,
				print "\n"
				if(wordList[i].conn):
					connSpan=[]
					for i in range(i,i+len(conn.split())):
						connSpan.append(i)
					positiveSet.append(connSpan)
					print "Yes",wordList[i].sense
				else:
					connSpan=[]
					for i in range(i,i+len(conn.split())):
						connSpan.append(i)
					negativeSet.append(connSpan)
				 	print "No"
	return (positiveSet,negativeSet)
	
connList=loadConnList("lists/compConnectiveList.list")
connSplitList=loadConnList("lists/splitConnectiveList.list",True)


discourseFileCollection=loadModel("processedData/annotatedData")
print len(discourseFileCollection)
positiveSet=[]
negativeSet=[]
for discourseFile in discourseFileCollection:
	print discourseFile.rawData
	pSet,nSet=identifyConnectives(discourseFile,connList,connSplitList)
	for conn in pSet:
		print "conn","-"*30
		feature=Feature("lists/compConnectiveList.list","lists/tagSet.list","lists/chunkSet.list",discourseFile.globalWordList,discourseFile.sentenceList)
		feature.tagFeature(conn)
		feature.chunkFeature(conn)
		feature.chunkNeighbor(conn,1)
		feature.chunkNeighbor(conn,-1)
		print feature.featureVector
	positiveSet.extend(pSet)
	negativeSet.extend(nSet)
	break
print len(positiveSet),len(negativeSet)
