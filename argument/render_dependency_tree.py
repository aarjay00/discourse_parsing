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
from render_dependency_tree_api import *

import pydot # import pydot or you're not going to get anywhere my friend :D

graph = pydot.Dot(graph_type='graph')


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
	createDirectory(filePath)
	sentenceList=discourseFileInst.sentenceList
	wordList=discourseFileInst.globalWordList
	for sentence in sentenceList:
		graph = pydot.Dot(graph_type='graph')
		rootNode=sentence.rootNode
		nodeDict=sentence.nodeDict
		print rootNode
		for node in rootNode:
			print "creating"
			graph=render_dependency_tree(node,nodeDict,graph,sentence,wordList,filePath+"/"+str(sentence.sentenceNum)+".png")
