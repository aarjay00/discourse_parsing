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

	def first3WordArg1(self,parseFile,discourseRelation):
		self.featureVector["first3WordsArg1"]="_".join(discourseRelation["Arg1"]["RawText"].split()[:3])

	def first3WordArg2(self,parseFile,discourseRelation):
		self.featureVector["first3WordsArg2"]="_".join(discourseRelation["Arg2"]["RawText"].split()[:3])
	def first2WordArg1(self,parseFile,discourseRelation):
		self.featureVector["first3WordsArg1"]="_".join(discourseRelation["Arg1"]["RawText"].split()[:2])

	def first2WordArg2(self,parseFile,discourseRelation):
		self.featureVector["first3WordsArg2"]="_".join(discourseRelation["Arg2"]["RawText"].split()[:2])
	

	def initializeBrownCluster(self,brownCluster):
		
		cluster=brownCluster.keys()
		for c1 in cluster:
			for c2 in cluster:
				self.featureVector[c1+"__"+c2]=0

	def brownCluster(self,parseFile,discourseRelation,brownCluster):

		for token1 in discourseRelation["Arg1"]["TokenList"]:
			sentenceNum1=token1[3]
			wordNum1=token1[4]
			word1=parseFile["sentences"][sentenceNum1]["words"][wordNum1][0].lower()
			if(word1 not in brownCluster):
				continue
			for token2 in discourseRelation["Arg2"]["TokenList"]:
				sentenceNum2=token2[3]
				wordNum2=token2[4]
				word2=parseFile["sentences"][sentenceNum2]["words"][wordNum2][0].lower()
				if(word2 not in brownCluster):
					continue
				self.featureVector[brownCluster[word1]+"__"+brownCluster[word2]]=True
	def modalWords(self,parseFile,discourseRelation):
		
		modalWordList=["can","could","may","might","will","shall","would","should","must","dare","need","ought to","used to","have got to","to be going to","to be able to"]

		
		arg1=discourseRelation["Arg1"]["RawText"].lower()
		arg2=discourseRelation["Arg2"]["RawText"].lower()

		arg1Modals=[]
		arg2Modals=[]
		for modal in modalWordList:
			if(modal in arg1 or modal in arg2):
				self.featureVector["SimpleModalPresence_"+modal]=True
			if(modal in arg1):
				self.featureVector["arg1ModalPresence_"+modal]=True
				arg1Modals.append(modal)
			if(modal in arg2):
				self.featureVector["arg2ModalPresence_"+modal]=True
				arg2Modals.append(modal)
		for modal1 in arg1Modals:
			for modal2 in arg2Modals:
				self.featureVector["arg1-arg2ModalPresence"]=True
