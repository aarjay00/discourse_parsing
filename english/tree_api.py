#!/usr/bin/env python
# -*- coding: utf-8 -*-



from nltk import tree



def getNodeFromTreePostion(treePosition,parseTree):
	if(len(treePosition)==0):
		return parseTree
	try:
		nextParseTree=parseTree[treePosition[0]]
	except:
	 	print treePosition
	 	print "aaaa"
	 	return parseTree
	if(not isinstance(nextParseTree,unicode)):
		parseTree=nextParseTree
	return getNodeFromTreePostion(treePosition[1:],parseTree)

def getProductionRulesFromTree(treeNode):

	productionRules=[]
	if(isinstance(treeNode,unicode)):
		return productionRules
	rule=treeNode.label()+"->"
	for child in treeNode:
		if(not isinstance(child,unicode)):
			rule+=child.label()+"_"
	if(len(treeNode)>1):
		productionRules.append(rule[:-1])
	for child in treeNode:
		productionRules.extend(getProductionRulesFromTree(child))
	return productionRules
	
