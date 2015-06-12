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

def identifyConnectives(discourseFileInst,connList,connSplitList,positiveSet,negativeSet):
	wordList=discourseFileInst.globalWordList
	for conn in connList:
		posList=searchConn(conn,wordList)
		if(len(posList)>0):
			print "found ",conn,len(posList)
			for i in posList:
				if(wordList[i].conn):
					positiveSet.append((i,i+len(conn)-1))
					print "Yes",wordList[i].sense
				else:
					negativeSet.append((i,i+len(conn)-1))
				 	print "No"
	return (positiveSet,negativeSet)
	
connList=loadConnList("lists/compConnectiveList.list")
connSplitList=loadConnList("lists/splitConnectiveList.list",True)


discourseFileCollection=loadModel("processedData/annotatedData")
print len(discourseFileCollection)
positiveSet=[]
negativeSet=[]
for discourseFile in discourseFileCollection:
	positiveSet,negativeSet=identifyConnectives(discourseFile,connList,connSplitList,positiveSet,negativeSet)
print len(positiveSet),len(negativeSet)
