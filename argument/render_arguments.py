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

from tree_api import *

from argument_match_accuracy import *


if len(sys.argv)<2:
	print "Please give location of proccessed data"
	exit()

dataLocation = sys.argv[1]

from os import listdir
from os.path import isfile, join
discourseFileCollection= [ dataLocation+str(f) for f in listdir(dataLocation) if isfile(join(dataLocation,f)) ]
discourseFileCollection=folderWalk(dataLocation)



def findConnectives(wordList):
	connList=[]
	conn=[]
	wordNum=-1
	for word in wordList:
		wordNum+=1
		if not word.conn:
			continue
		if(len(conn)!=0 and conn[-1]!=wordNum-1):
			connList.append(conn)
			conn=[]
		conn.append(wordNum)
	if(len(conn)!=0):
		connList.append(conn)
	return connList
	

createDirectory


for discourseFileLocation in discourseFileCollection:
	discourseFile=loadModel(discourseFileLocation)
	print discourseFile.rawFileName
	rawFileName=discourseFile.rawFileName.split("/")
	filePath=""
	for part in rawFileName:
		if(part.startswith("Section") or filePath!="" ):
			filePath=filePath+part+"/"
	filePath="dependencyTreeGraph/"+filePath
	createDirectory(filePath)
	
	
	wordList=discourseFile.globalWordList
	connList=findConnectives(wordList)
	relationNum=0
	for conn in connList:
		arg1Span=wordList[conn[0]].arg1Span
		arg2Span=wordList[conn[0]].arg2Span
		wordNum=0
		FD=open(filePath+"relation"+str(relationNum),"w")
		for word in wordList:
			if(wordNum==arg1Span[0]):
				FD.write(" <ARG1 START>")
			if(wordNum==arg2Span[0]):
				FD.write(" <ARG2 START>")
			if(wordNum==conn[0]):
				FD.write(" <CONN START>")
		
			FD.write(" "+word.word)
		
			if(wordNum==arg1Span[-1]):
				FD.write(" <ARG1 END>")
			if(wordNum==arg2Span[-1]):
				FD.write(" <ARG2 END>")
			if(wordNum==conn[-1]):
				FD.write(" <CONN END>")
			wordNum+=1
		FD.close()
		relationNum+=1
