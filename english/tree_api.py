#!/usr/bin/env python
# -*- coding: utf-8 -*-



from nltk import tree



def getNodeFromTreePostion(treePosition,parseTree):
	if(len(treePosition)==0):
		return parseTree
	nextParseTree=parseTree[treePosition[0]]
	if(not isinstance(nextParseTree,unicode)):
		parseTree=nextParseTree
	return getNodeFromTreePostion(treePosition[1:],parseTree)
