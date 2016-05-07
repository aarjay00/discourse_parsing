#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nltk import tree
from tree_api import *
from nltk.corpus import verbnet

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


	def firstAndLastArg1(self,parseFile,discourseRelation):
		l=discourseRelation["Arg1"]["RawText"].split()
		self.featureVector["firstAndLastArg1"]=l[0]+"__"+l[-1]


	def firstAndLastArg2(self,parseFile,discourseRelation):
		l=discourseRelation["Arg2"]["RawText"].split()
		self.featureVector["firstAndLastArg"]=l[0]+"__"+l[-1]

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
#				self.featureVector[word1+"__"+word2]=word1+"__"+word2
				if(word2 not in brownCluster):
					continue
				self.featureVector[brownCluster[word1]+"__"+brownCluster[word2]]=True
	def modalWords(self,parseFile,discourseRelation):
		
		modalWordList=["can","could","may","might","will","shall","would","should","must","dare","need","ought to","used to","have got to","to be going to","to be able to"]

		
		arg1=[]
		arg2=[]
		for token in discourseRelation["Arg1"]["TokenList"]:
			arg1.append(parseFile["sentences"][token[3]]["words"][token[4]][0])
		for token in discourseRelation["Arg1"]["TokenList"]:
			arg2.append(parseFile["sentences"][token[3]]["words"][token[4]][0])

		arg1Modals=[]
		arg2Modals=[]
		for modal in modalWordList:
			if(modal in arg1 or modal in arg2):
				self.featureVector["SimpleModalPresence_"+modal]=True
			else:
				self.featureVector["SimpleModalPresence_"+modal]=False
			if(modal in arg1):
				self.featureVector["arg1ModalPresence_"+modal]=True
				arg1Modals.append(modal)
			else:
				self.featureVector["arg1ModalPresence_"+modal]=False
			if(modal in arg2):
				self.featureVector["arg2ModalPresence_"+modal]=True
				arg2Modals.append(modal)
			else:
				self.featureVector["arg2ModalPresence_"+modal]=False
		for m1 in modalWordList:
		  for m2 in modalWordList:
		  	self.featureVector[m1+"__"+m2]=False
		for modal1 in arg1Modals:
			for modal2 in arg2Modals:
				self.featureVector[modal1+"__"+modal2]=True
	def numberPresence(self,parseFile,discourseRelation):

		arg1=[]
		arg2=[]

		for token in discourseRelation["Arg1"]["TokenList"]:
			sentenceNum=token[3]
			wordNum=token[4]
			arg1.append(parseFile["sentences"][sentenceNum]["words"][wordNum][0])
		for token in discourseRelation["Arg2"]["TokenList"]:
			sentenceNum=token[3]
			wordNum=token[4]
			arg2.append(parseFile["sentences"][sentenceNum]["words"][wordNum][0])


		arg1N=[]
		arg1P=[]
		arg1D=[]
		dollar=False
		prevWord=""
		for  word in arg1:
			if(word=="%"):
				arg1P.append(prevWord)
			elif(word=="$"):
				dollar=True
			elif(word.isdigit() and dollar):
				arg1D.append(word)
				dollar=False
			elif(word.isdigit() and not dollar):
				arg1N.append(word)
			prevWord=word

		arg2N=[]
		arg2P=[]
		arg2D=[]
		dollar=False
		prevWord=""
		for  word in arg2:
			if(word=="%"):
				arg2P.append(prevWord)
			elif(word=="$"):
				dollar=True
			elif(word.isdigit() and dollar):
				arg2D.append(word)
				dollar=False
			elif(word.isdigit() and not dollar):
				arg2N.append(word)
			prevWord=word


		if(len(arg1N)>0 and len(arg2N)>0):
			self.featureVector["NumberMention"]=True
		else:
			self.featureVector["NumberMention"]=False
		if(len(arg1P)>0 and len(arg2P)>0):
			self.featureVector["PercentageMention"]=True
		else:
			self.featureVector["PercentageMention"]=False
		if(len(arg1D)>0 and len(arg2D)>0):
			self.featureVector["DollarMention"]=True
		else:
			self.featureVector["DollarMention"]=False

#		if(len(arg1N)>0 and len(arg2D)>0):
#			self.featureVector["NumberDollarMention"]=True
#		else:
#			self.featureVector["NumberDollarMention"]=False
#		if(len(arg1N)>0 and len(arg2P)>0):
#			self.featureVector["NumberPercentageMention"]=True
#		else:
#			self.featureVector["NumberPercentageMention"]=False
#		if(len(arg1D)>0 and len(arg2P)>0):
#			self.featureVector["DollarPercentageMention"]=True
#		else:
#			self.featureVector["DollarPercentageMention"]=False

	def verbSimilarity(self,parseFile,discourseRelation,brownCluster):
		
		arg1=[]
		arg2=[]
		arg1Indices=[]
		arg2Indices=[]
		for token in discourseRelation["Arg1"]["TokenList"]:
			arg1.append(parseFile["sentences"][token[3]]["words"][token[4]])
			arg1Indices.append(token[4])
		for token in discourseRelation["Arg2"]["TokenList"]:
			arg2.append(parseFile["sentences"][token[3]]["words"][token[4]])
			arg2Indices.append(token[4])

		#DO LATER , get different trees for arg1 since arg1 spans more than 1 sentence -----------------------
		arg1=[x for x in filter(lambda x: "VB" in x[1]["PartOfSpeech"],arg1)]
		arg2=[x for x in filter(lambda x: "VB" in x[1]["PartOfSpeech"],arg2)]

#		for word in arg1:
#			print word[0],word[1]["PartOfSpeech"],verbnet.classids(lemma=word[0])
#		print ""
#		for word in arg2:
#			print word[0],word[1]["PartOfSpeech"],verbnet.classids(lemma=word[0])
#		print ""

		simmilarity=False
		for word1 in arg1:
			for word2 in arg2:
				try:
					if(brownCluster[word1[0].lower()]==brownCluster[word2[0].lower()]):
						simmilarity=True
				except:
				  	pass
#				self.featureVector[word1[0]+"__"+word2[0]]=word1[0]+"__"+word2[0]
		self.featureVector["verbSimilarity"]=simmilarity

	def argumentSentiment(self,parseFile,discourseRelation,sentimentDict):
		
		arg1=[]
		arg2=[]
		sentimentArg1=[]
		sentimentArg2=[]

		for token in discourseRelation["Arg1"]["TokenList"]:
			arg1.append(parseFile["sentences"][token[3]]["words"][token[4]])
			try:
				sentimentArg1.append((sentimentDict[arg1[-1][0].upper()],token[3],token[4]))
			except KeyError:
				continue
		for token in discourseRelation["Arg2"]["TokenList"]:
			arg2.append(parseFile["sentences"][token[3]]["words"][token[4]])
			try:
				sentimentArg2.append((sentimentDict[arg2[-1][0].upper()],token[3],token[4]))
			except KeyError:
				continue

		sentiment_1=[]
		sentiment_2=[]
		prev=""
		currentSentiment="None"
		for i in sentimentArg1:
			if(prev!="" and i[1]==prev[1] and i[2]-1==prev[2]):
				if(currentSentiment=="None" or currentSentiment=="neutral"):
					if(i[0][0]=="positive"):
						currentSentiment="positive"
					elif(i[0][0]=="negative" or i[0][0]=="weakneg"):
						currentSentiment="negative"
				elif(i[0][0]=="weakneg" or i[0][0]=="negative"):
					currentSentiment="negative"
				elif(i[0][0]=="positive"):
					currentSentiment="positive"
			else:
			 	if(currentSentiment!="None"):
					sentiment_1.append(currentSentiment)
			 	if(i[0][0]=="weakneg" or i[0][0]=="negative"):
			 		currentSentiment="negative"
				elif(i[0]=="positive"):
					currentSentiment="positive"
				else:
					currentSentiment=i[0][0]
			prev=i
		if(currentSentiment!="None"):
			sentiment_1.append(currentSentiment)
		prev=""
		currentSentiment="None"
		for i in sentimentArg2:
			if(prev!="" and i[1]==prev[1] and i[2]-1==prev[2]):
				if(currentSentiment=="None" or currentSentiment=="neutral"):
					if(i[0]=="positive"):
						currentSentiment="positive"
					elif(i[0]=="negative" or i[0]=="weakneg"):
						currentSentiment="negative"
				elif(i[0][0]=="weakneg" or i[0][0]=="negative"):
					currentSentiment="negative"
				elif(i[0][0]=="positive"):
					currentSentiment="positive"
			else:
			 	if(currentSentiment!="None"):
					sentiment_2.append(currentSentiment)
			 	if(i[0][0]=="weakneg" or i[0][0]=="negative"):
			 		currentSentiment="negative"
				elif(i[0][0]=="positive"):
					currentSentiment="positive"
				else:
					currentSentiment=i[0][0]
			prev=i
		if(currentSentiment!="None"):
			sentiment_2.append(currentSentiment)

		arg1FinalSentiment=0
		arg2FinalSentiment=0
		for i in sentiment_1:
			if(i=="positive"):
				arg1FinalSentiment+=1
			elif(i=="negative"):
				arg1FinalSentiment-=1
		for i in sentiment_2:
			if(i=="positive"):
				arg2FinalSentiment+=1
			elif(i=="negative"):
				arg2FinalSentiment-=1
		if(arg1FinalSentiment==0 or arg2FinalSentiment==0):
			self.featureVector["arg1Sentiment"]="none"
			self.featureVector["arg2Sentiment"]="none"
			self.featureVector["arg1_arg2Sentiment"]="none"
			return

		if(arg1FinalSentiment<0 and arg2FinalSentiment>0):
			self.featureVector["NegToPos"]=True
		else:
		 	self.featureVector["NegToPos"]=False
		if(arg1FinalSentiment>0 and arg2FinalSentiment<0):
			self.featureVector["PosToNeg"]=True
		else:
		 	self.featureVector["PosToNeg"]=False
		
		return

		if(arg1FinalSentiment<0):
			self.featureVector["arg1Sentiment"]="negative"
		elif(arg1FinalSentiment>0):
			self.featureVector["arg1Sentiment"]="positive"
		else:
			self.featureVector["arg1Sentiment"]="nuetral"
		if(arg2FinalSentiment<0):
			self.featureVector["arg2Sentiment"]="negative"
		elif(arg2FinalSentiment>0):
			self.featureVector["arg2Sentiment"]="positive"
		else:
			self.featureVector["arg2Sentiment"]="nuetral"

		self.featureVector["arg1_arg2Sentiment"]=self.featureVector["arg1Sentiment"]+"__"+self.featureVector["arg2Sentiment"]

	def argumentPosition(self,parseFile,discourseRelation):

		arg1Sentence=[]
		arg1Word=[]
		arg2Sentence=[]
		arg2Word=[]

		for token in discourseRelation["Arg1"]["TokenList"]:
			arg1Sentence.append(token[3])
			arg1Word.append(token[4])
		for token in discourseRelation["Arg2"]["TokenList"]:
			arg2Sentence.append(token[3])
			arg2Word.append(token[4])
		arg1Sentence=list(set(arg1Sentence))
		arg2Sentence=list(set(arg2Sentence))
		if(len(arg1Sentence)==len(arg2Sentence)==1 and arg1Sentence[0]==arg2Sentence[0]):
			self.featureVector["bothArgInSameSentence"]=True
		else:
			self.featureVector["bothArgInSameSentence"]=False
