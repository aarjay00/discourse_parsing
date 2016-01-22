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
#from identify_connectives import *
from annotated_data import *

if len(sys.argv)<2:
	print "Please give location of proccessed data"
	exit()

dataLocation = sys.argv[1]

from os import listdir
from os.path import isfile, join
discourseFileCollection= [ dataLocation+str(f) for f in listdir(dataLocation) if isfile(join(dataLocation,f)) ]
discourseFileCollection=folderWalk(dataLocation)




for discourseFileLocation in discourseFileCollection:
	discourseFileInst=loadModel(discourseFileLocation)
	print discourseFileInst.rawFileName
	rawFileName=discourseFileInst.rawFileName.split("/")
	filePath=""
	for part in rawFileName:
		if(part.startswith("Section") or filePath!="" ):
			filePath=filePath+part+"/"
	filePath="dependencyTreeGraph/"+filePath
	print filePath
	createDirectory(filePath)
	sentenceList=discourseFileInst.sentenceList
	wordList=discourseFileInst.globalWordList
	FD=codecs.open(filePath+"sentenceInfo","w")
	for sentence in sentenceList:
	  	FD.write("Sentence"+str(sentence.sentenceNum)+"-"*50+"\n")
	  	for pos in sentence.wordNumList:
	  		FD.write(" "+wordList[pos].word+"-"+wordList[pos].wordTag.replace("\n","")+"-"+str(wordList[pos].chunkNum))
	  		if(wordList[pos].conn):
				FD.write("-cn")
			elif(wordList[pos].splitConn):
				FD.write("-sn")
		FD.write("\n")
	FD.close()
