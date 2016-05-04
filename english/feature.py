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


#-----------------------------------------Explicit Features-------------------------------------------------------------

	def connectiveString(self,discourseRelation):
		
		connString=discourseRelation["Connective"]["RawText"]
		self.featureVector["connectiveString"]=connString
		connString=connString.split()

	def connectivePOS(self,parseFile,discourseRelation):

		sentenceNum=int(discourseRelation["Connective"]["TokenList"][0][3])
		
		posTag=[]
		for token in discourseRelation["Connective"]["TokenList"]:
			
			wordNum=int(token[4])
			posTag.append(parseFile["sentences"][sentenceNum]["words"][wordNum][1]["PartOfSpeech"])
		posTag=" ".join(posTag)
		
		self.featureVector["connectivePOS"]=posTag

	def previousWord(self,parseFile,discourseRelation):

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
		
		word=prevWord+"__"+" ".join(connString)

		self.featureVector["previousWord"]=prevWord

	def nextWord(self,parseFile,discourseRelation):

		sentenceNum=discourseRelation["Connective"]["TokenList"][0][3]

		connString=[]
		nextWord=""
		for token in discourseRelation["Connective"]["TokenList"]:
			wordNum=token[4]
			connString.append(parseFile["sentences"][sentenceNum]["words"][wordNum][0])
		wordNum=discourseRelation["Connective"]["TokenList"][0][4]
		try:
			nextWord=parseFile["sentences"][sentenceNum]["words"][wordNum+1][0]
		except:
		 	nextWord="X-End-X"
		
		word=nextWord+"__"+" ".join(connString)

		self.featureVector["nextWord"]=nextWord

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



	def connectiveParentSelfCategory(self,parseFile,discourseRelation):

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
			self.featureVector["connectiveParentSelfCategory"]="Bug"
			return

		connectiveTree=getNodeFromTreePostion(connectiveTreePosition,parseTree)


		self.featureVector["connectiveParentSelfCategory"]=connectiveTree.parent().label()
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
			self.featureVector["connectiveLeftSiblingSelfCategory"]="Bug"
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
			self.featureVector["connectiveRightSiblingSelfCategory"]="Bug"
			return
		
		connectiveTree=getNodeFromTreePostion(connectiveTreePosition,parseTree)

		try:
			self.featureVector["connectiveRightSiblingSelfCategory"]=connectiveTree.right_sibling().label()
		except:
			self.featureVector["connectiveRightSiblingSelfCategory"]="None"


	def connectiveParentLeftSiblingSelfCategory(self,parseFile,discourseRelation):

		sentenceNum=discourseRelation["Connective"]["TokenList"][0][3]
		parseTree=parseFile["sentences"][sentenceNum]["parsetree"]
		parseTree=tree.ParentedTree.fromstring(parseTree)

		connectiveIndices=[]

		for token in discourseRelation["Connective"]["TokenList"]:
			connectiveIndices.append(token[4])

		try:
			connectiveTreePosition=parseTree.treeposition_spanning_leaves(connectiveIndices[0],connectiveIndices[-1]+1)
		except:
			print "parent left category issues"
			self.featureVector["connectiveParentLeftSiblingSelfCategory"]="Bug"
			return

		connectiveTree=getNodeFromTreePostion(connectiveTreePosition,parseTree)

		try:
			self.featureVector["connectiveParentLeftSiblingSelfCategory"]=connectiveTree.parent.left_sibling().label()
		except:
			self.featureVector["connectiveParentLeftSiblingSelfCategory"]="None"

	def connectiveParentRightSiblingSelfCategory(self,parseFile,discourseRelation):

		sentenceNum=discourseRelation["Connective"]["TokenList"][0][3]
		parseTree=parseFile["sentences"][sentenceNum]["parsetree"]
		parseTree=tree.ParentedTree.fromstring(parseTree)

		connectiveIndices=[]

		for token in discourseRelation["Connective"]["TokenList"]:
			connectiveIndices.append(token[4])

		try:
			connectiveTreePosition=parseTree.treeposition_spanning_leaves(connectiveIndices[0],connectiveIndices[-1]+1)
		except:
			print "parent right category issues"
			self.featureVector["connectiveParentRightSiblingSelfCategory"]="Bug"
			return

		connectiveTree=getNodeFromTreePostion(connectiveTreePosition,parseTree)

		try:
			self.featureVector["connectiveParentRightSiblingSelfCategory"]=connectiveTree.parent.right_sibling().label()
		except:
			self.featureVector["connectiveParentRightSiblingSelfCategory"]="None"
	def connectiveSyntaxInteraction(self):
			
		features=self.featureVector.keys()

		features=filter(lambda x: "__" not in x and x!="connectiveString", features)

		for feature in features:
			self.featureVector[feature+"__connectiveString"]=self.featureVector[feature]+"__"+self.featureVector["connectiveString"]
	def syntaxSyntaxInteraction(self):

		syntaxFeatures=self.featureVector.keys()
		
		syntaxFeatures=filter(lambda x: "__" not in x and x!="connectiveString", syntaxFeatures)
		
		for feature_1 in syntaxFeatures:
			for feature_2 in syntaxFeatures:
				if(feature_1==feature_2):
					continue
				self.featureVector[feature_1+"__"+feature_2]=self.featureVector[feature_1]+"__"+self.featureVector[feature_2]

	def parentLinkedContext(self,parseFile,discourseRelation):

		sentenceNum=discourseRelation["Connective"]["TokenList"][0][3]
		parseTree=parseFile["sentences"][sentenceNum]["parsetree"]
		parseTree=tree.ParentedTree.fromstring(parseTree)
		connectiveIndices=[]
		

		for token in discourseRelation["Connective"]["TokenList"]:
			connectiveIndices.append(token[4])

		try:
			connectiveTreePosition=parseTree.treeposition_spanning_leaves(connectiveIndices[0],connectiveIndices[-1]+1)
		except:
			print "parent linked context issues"
			self.featureVector["parentLinkedContext__"]="Bug"
			return

		connectiveTree=getNodeFromTreePostion(connectiveTreePosition,parseTree).parent()
		linkedContext=""
		try:
			linkedContext=connectiveTree.parent().label()+"_"
		except:
			linkedContext="None_"
		linkedContext=linkedContext+connectiveTree.label()+"_"

		for child in connectiveTree:
			if(not isinstance(child,unicode)):
				linkedContext=linkedContext+child.label()+"_"
			else:
				linkedContext=linkedContext+child+"_"

		self.featureVector["parentLinkedContext__"]=linkedContext
	def connectiveToRootPath(self,parseFile,discourseRelation):
		sentenceNum=discourseRelation["Connective"]["TokenList"][0][3]
		parseTree=parseFile["sentences"][sentenceNum]["parsetree"]
		parseTree=tree.ParentedTree.fromstring(parseTree)
		connectiveIndices=[]
		for token in discourseRelation["Connective"]["TokenList"]:
			connectiveIndices.append(token[4])
		try:
			connectiveTreePosition=parseTree.treeposition_spanning_leaves(connectiveIndices[0],connectiveIndices[-1]+1)
		except:
			print "connective to root path issues"
			self.featureVector["connectiveToRootPath__"]="Bug"
			return

		connectiveTree=getNodeFromTreePostion(connectiveTreePosition,parseTree)

		path=""
		while(connectiveTree!=None):
			path+=connectiveTree.label()+"_"
			connectiveTree=connectiveTree.parent()
		self.featureVector["connectiveToRootPath__"]=path
#-----------------------------------------Implicit Features-------------------------------------------------------------

	def firstWordArg1(self,parseFile,discourseRelation):
		self.featureVector["firstWordArg1"]=discourseRelation["Arg1"]["RawText"].split()[0]

	def firstWordArg2(self,parseFile,discourseRelation):
		self.featureVector["firstWordArg2"]=discourseRelation["Arg2"]["RawText"].split()[0]

	def lastWordArg1(self,parseFile,discourseRelation):
		self.featureVector["firstWordArg1"]=discourseRelation["Arg1"]["RawText"].split()[-1]

	def lastWordArg2(self,parseFile,discourseRelation):
		self.featureVector["firstWordArg2"]=discourseRelation["Arg2"]["RawText"].split()[-1]
