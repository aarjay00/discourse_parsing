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
"""
pydot example 1
@author: Federico Cáceres
@url: http://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot
"""
import pydot # import pydot or you're not going to get anywhere my friend :D

# first you create a new graph, you do that with pydot.Dot()
graph = pydot.Dot(graph_type='graph')

# the idea here is not to cover how to represent the hierarchical data
# but rather how to graph it, so I'm not going to work on some fancy
# recursive function to traverse a multidimensional array...
# I'm going to hardcode stuff... sorry if that offends you

if len(sys.argv)<2:
	print "Please give location of proccessed data"
	exit()

dataLocation = sys.argv[1]

discourseFileCollection=loadModel(dataLocation)


def create_graph(currNode , nodeDict , graph):
#	print "\t"*nodeDict[currNode].nodeLevel,currNode
	for child in nodeDict[currNode].childList:
		edge = pydot.Edge(currNode,child , label=" "+nodeDict[child].nodeRelation+" ")
		graph.add_edge(edge)
	for child in nodeDict[currNode].childList:
		graph=create_graph(child,nodeDict,graph)
	return graph


for discourseFileInst in discourseFileCollection:
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
	for sentence in sentenceList:
		graph = pydot.Dot(graph_type='graph')
		rootNode=sentence.rootNode
		nodeDict=sentence.nodeDict
#		print rootNode
		for node in rootNode:
			graph=create_graph(node,nodeDict,graph)
			graph.write_png(filePath+str(sentence.sentenceNum)+".png")
