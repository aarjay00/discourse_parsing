#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nltk import tree
from tree_api import *


class Feature():
	def __init__(self):
		self.featureVector={}
		self.classLabel=""
	def setClassLabel(self,classLabel):
		self.classLabel=classLabel

	def connectiveString(self,discourseRelation):
		
		connString=discourseRelation["Connective"]["RawText"]
		self.featureVector["connectiveString"]=connString
		
		return

	def connectivePOS(self,parseFile,discourseRelation):

		sentenceNum=int(discourseRelation["Connective"]["TokenList"][0][3])
		
		posTag=[]
		for token in discourseRelation["Connective"]["TokenList"]:
			
			wordNum=int(token[4])
			posTag.append(parseFile["sentences"][sentenceNum]["words"][wordNum][1]["PartOfSpeech"])
		posTag=" ".join(posTag)
		
		self.featureVector["connectivePOS"]=posTag

	def previousWordandConnective(self,parseFile,discourseRelation):

		sentenceNum=discourseRelation["Connective"]["TokenList"][0][3]

		connString=[]
		prevWord=""
		for token in discourseRelation["Connective"]["TokenList"]:
			wordNum=token[4]
			connString.append(parseFile["sentences"][sentenceNum]["words"][wordNum][0])
		wordNum=discourseRelation["Connective"]["TokenList"][0][4]
		if(wordNum!=0):
			prevWord=parseFile["sentences"][sentenceNum]["words"][wordNum-1][0]
		else:
		 	prevWord="X-Start-X"
		
		word=prevWord+"+"+" ".join(connString)

		self.featureVector["previousWordandConnective"]=word

	def connectiveSelfCategory(self,parseFile,discourseRelation):

		sentenceNum=discourseRelation["Connective"]["TokenList"][0][3]
		parseTree=parseFile["sentences"][sentenceNum]["parsetree"]
		parseTree=tree.ParentedTree.fromstring(parseTree)

		connectiveIndices=[]

		for token in discourseRelation["Connective"]["TokenList"]:
			connectiveIndices.append(token[4])
		try:
			connectiveTreePosition=parseTree.treeposition_spanning_leaves(connectiveIndices[0],connectiveIndices[-1]+1)
		except:
			print "self category issues"
			self.featureVector["connectiveSelfCategory"]="Bug"
			return

		connectiveTree=getNodeFromTreePostion(connectiveTreePosition,parseTree)

		self.featureVector["connectiveSelfCategory"]=connectiveTree.label()

	def connectiveLeftSiblingSelfCategory(self,parseFile,discourseRelation):

		sentenceNum=discourseRelation["Connective"]["TokenList"][0][3]
		parseTree=parseFile["sentences"][sentenceNum]["parsetree"]
		parseTree=tree.ParentedTree.fromstring(parseTree)

		connectiveIndices=[]

		for token in discourseRelation["Connective"]["TokenList"]:
			connectiveIndices.append(token[4])

		try:
			connectiveTreePosition=parseTree.treeposition_spanning_leaves(connectiveIndices[0],connectiveIndices[-1]+1)
		except:
			print "left category issues"
			self.featureVector["connectiveSelfCategory"]="Bug"
			return

		connectiveTree=getNodeFromTreePostion(connectiveTreePosition,parseTree)

		try:
			self.featureVector["connectiveLeftSiblingSelfCategory"]=connectiveTree.left_sibling().label()
		except:
			self.featureVector["connectiveLeftSiblingSelfCategory"]="None"
	def connectiveRightSiblingSelfCategory(self,parseFile,discourseRelation):

		sentenceNum=discourseRelation["Connective"]["TokenList"][0][3]
		parseTree=parseFile["sentences"][sentenceNum]["parsetree"]
		parseTree=tree.ParentedTree.fromstring(parseTree)

		connectiveIndices=[]

		for token in discourseRelation["Connective"]["TokenList"]:
			connectiveIndices.append(token[4])

		try:
			connectiveTreePosition=parseTree.treeposition_spanning_leaves(connectiveIndices[0],connectiveIndices[-1]+1)
		except:
			print "right category issues"
			self.featureVector["connectiveSelfCategory"]="Bug"
			return
		
		connectiveTree=getNodeFromTreePostion(connectiveTreePosition,parseTree)

		try:
			self.featureVector["connectiveRightSiblingSelfCategory"]=connectiveTree.right_sibling().label()
		except:
			self.featureVector["connectiveRightSiblingSelfCategory"]="None"
	def connectiveSyntaxInteraction(self):
			
		features=self.featureVector.keys()

		features=filter(lambda x: "__" not in x and x!="connectiveString", features)

		for feature in features:
			self.featureVector[feature+"__connectiveString"]=feature+"__"+self.featureVector["connectiveString"]
	def syntaxSyntaxInteraction(self):

		syntaxFeatures=self.featureVector.keys()
		
		syntaxFeatures=filter(lambda x: "__" not in x and x!="connectiveString", syntaxFeatures)
		
		for feature_1 in syntaxFeatures:
			for feature_2 in syntaxFeatures:
				if(feature_1==feature_2):
					continue
				self.featureVector[feature_1+"__"+feature_2]=self.featureVector[feature_1]+"__"+self.featureVector[feature_2]
