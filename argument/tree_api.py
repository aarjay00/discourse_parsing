#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
from util import *
from ssf_api import *
from letter import *
from merge_annotations import *
from annotated_data import *

def traverseNode(level,nodeName,nodeDict):
	print "\t"*level,"Node-",nodeName
	nodeDict[nodeName].nodeLevel=level
	for child in nodeDict[nodeName].childList:
		traverseNode(level+1,child,nodeDict)


def getLCA(argSpan,discourseFileInst):
	wordList=discourseFileInst.globalWordList
	sentenceList=discourseFileInst.sentenceList

def findRelation(nodeRelation, node , nodeDict , level , maxLevel):
	if(level==maxLevel):
		return False
	for child in nodeDict[node].childList:
		if nodeRelation in nodeDict[child].nodeRelation:
			return True
		if(findRelation(nodeRelation,child,nodeDict,level+1,maxLevel)):
			return True
	return False
def findChild(childTarget, node , nodeDict , level , maxLevel):
	if(level==maxLevel):
		return False
	for child in nodeDict[node].childList:
		if childTarget in nodeDict[child].getChunkName(child):
			return True
		if(findRelation(childTarget,child,nodeDict,level+1,maxLevel)):
			return True
	return False
def hasChild(nodeName, nodeDict,childTarget,unique=True):
	node=nodeDict[nodeName]
	num=0
	for child in node.childList:
		if(unique):
			if(node.getChunkName(child)==childTarget):
				num+=1
		else:
		  	if(childTarget in node.getChunkName(child)):
				num+=1
	return num
def hasChildRelation(nodeName, nodeDict,childRelationTarget):
	node=nodeDict[nodeName]
	num=0
	for child in node.childList:
		if(nodeDict[child].nodeRelation==childRelationTarget):
			return True
	return False
def getPathToRoot(node,nodeDict):
	path=[]
	while(1):
		path.append(node.nodeName)
		parent=node.nodeParent
		if(parent=="None"):
			break
		node=nodeDict[parent]
	return path
def getCommonParent(node1,node2,nodeDict):
	path1=getPathToRoot(node1,nodeDict)
	path2=getPathToRoot(node2,nodeDict)
	i=len(path1)-1
	j=len(path2)-1
	if(i==0):
		print "commonparent-node1"
		return node1.nodeName
	elif(j==0):
		print "commonparent-node2"
		return node2.nodeName
	commonParent="None"
	while(i>=0 and j>=0):
		if(path1[i]==path2[j]):
			commonParent=path1[i]
		else:
			break
		i-=1
		j-=1
	print "commonparent",commonParent
	return commonParent
def isParent(node1,node2,nodeDict):
	
	p=hasChild(node1.nodeName,nodeDict,node2.nodeName)

	return p
