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
import pydot # import pydot or you're not going to get anywhere my friend :D

graph = pydot.Dot(graph_type='graph')

def isNodeArg2(node,sentence,wordList):

	chunk=sentence.chunkList[node.chunkNum]
	for pos in chunk.wordNumList:
		if(wordList[pos].arg2):
			return True
	return False



def create_graph_highlighted(currNode , nodeDict , graph,sentence,wordList,nodeList):
#	print "\t"*nodeDict[currNode].nodeLevel,currNode

	for nodeName,node in nodeDict.iteritems():
		if(nodeName in nodeList):
			var=True
		else:
		 var=False
		graphNodeName=nodeName+"_"+get_full_node_label(node,sentence,wordList)
		if(var):
			graphNode=pydot.Node(graphNodeName,fillcolor="red",style="filled")
		else:
			graphNode=pydot.Node(graphNodeName)
		graph.add_node(graphNode)

	for child in nodeDict[currNode].childList:
		vertexA=currNode+"_"+get_full_node_label(nodeDict[currNode],sentence,wordList)
		vertexB=child+"_"+get_full_node_label(nodeDict[child],sentence,wordList)
		edge = pydot.Edge(vertexA,vertexB , label=" "+nodeDict[child].nodeRelation+" " , fillcolor="red")
#		print edge
		graph.add_edge(edge)
	for child in nodeDict[currNode].childList:
		graph=create_graph(child,nodeDict,graph,sentence,wordList)
	return graph
	

def create_graph(currNode , nodeDict , graph,sentence,wordList):
#	print "\t"*nodeDict[currNode].nodeLevel,currNode

	for child in nodeDict[currNode].childList:
		vertexA=currNode+"_"+get_full_node_label(nodeDict[currNode],sentence,wordList)
		vertexB=child+"_"+get_full_node_label(nodeDict[child],sentence,wordList)
		edge = pydot.Edge(vertexA,vertexB , label=" "+nodeDict[child].nodeRelation+" " , fillcolor="red")
#		print edge
		graph.add_edge(edge)
	for child in nodeDict[currNode].childList:
		graph=create_graph(child,nodeDict,graph,sentence,wordList)
	return graph

def get_full_node_label(node,sentence,wordList):
	chunkNum=node.chunkNum
	if(chunkNum==-1):
		return ""
	label=""
	chunk=sentence.chunkList[chunkNum]
	i=0
	for pos in chunk.wordNumList:
		label=label+"_"+wordList[pos].word
		i+=1
	label=label.replace(" ","")
	label=label.replace("/","")
	label=label.replace("?","")
	label=label.replace("'","")
	label=label.replace("\"","")
	label=label.replace(" ","")
	label=label.replace(":","")
	label=label.replace(";","")
	label=label.replace("(","")
	label=label.replace(")","")
	label=label.replace(",","")
	label=label.replace(".","")
	label=label.replace("-","")
	label=label.replace("\n","")
	label=label.replace("\r","")
#	print repr(label)
	return label

def render_dependency_tree_highlighted(node,nodeDict,graph,sentence,wordList,nodeList,filePath):
	graph=create_graph_highlighted(node,nodeDict,graph,sentence,wordList,nodeList)
	graph.write_png(filePath)
def render_dependency_tree(node,nodeDict,graph,sentence,wordList,filePath):
	graph=create_graph(node,nodeDict,graph,sentence,wordList)
	graph.write_png(filePath)
