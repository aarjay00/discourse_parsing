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
from models import *

discourseFileCollection=loadModel("processedData/annotatedData")


def traverseNode(level,nodeName,nodeDict):
	print "\t"*level,"Node-",nodeName
	nodeDict[nodeName].nodeLevel=level
	for child in nodeDict[nodeName].childList:
		traverseNode(level+1,child,nodeDict)



for discourseFileInst in discourseFileCollection:
	print "*"*60,"new file"
	for sentence in discourseFileInst.sentenceList:
		print "\t","sentence"	
		nodeDict=sentence.nodeDict
		for nodeName,nodeInst in nodeDict.items():
			if(nodeInst.nodeParent!="None"):
				nodeDict[nodeInst.nodeParent].addChild(nodeName)
		for nodeName,nodeInst in nodeDict.items():
			if(len(nodeInst.childList)!=0 and nodeInst.nodeParent=="None"):
				sentence.rootNode.append(nodeName)
				print "\t\there",nodeName,len(sentence.rootNode)
				for child in nodeInst.childList:
					print "\t\t\t",nodeDict[child].nodeName
print "-"*60,"traversing"
for discourseFileInst in discourseFileCollection:
	print "-"*30,"new file !!!",discourseFileInst.rawFileName
	for sentence in discourseFileInst.sentenceList:
	  print "-"	*30," new sentencce"
	  for root in sentence.rootNode:
	  	traverseNode(0,root,sentence.nodeDict)
	  for nodeName,nodeInst in sentence.nodeDict.items():
	  	if(nodeInst.nodeLevel==-1):
			print "problem here ", nodeName
exit()

exportModel("processedData/annotatedData",discourseFileCollection)	
discourseFileCollection=loadModel("processedData/annotatedData")



print "aloha hahahaha"

for discourseFileInst in discourseFileCollection:
	sentenceList=discourseFileInst.sentenceList
	print "*"*60,"new file"
	for sentence in sentenceList:
		print "\t","sentence"	
		for root in sentence.rootNode:
			print "\t\t",root
