#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import json

from util import *
from feature import *
from model_api import *

def readDocuments(documentLocation,relationLocation):
	
	documentData=codecs.open(documentLocation,encoding='utf-8')
	documentList=json.load(documentData)
	
	relationData=codecs.open(relationLocation,encoding='utf-8')
	relationList=[json.loads(x) for x in relationData]

	return documentList,relationList


def divideRelations(relationList):
	explicitRelationList=[]
	implicitRelationList=[]
	for relation in relationList:
		connective=relation['Connective']['CharacterSpanList']
		if(len(connective)==0):
			implicitRelationList.append(relation)
		else:
			if(relation['Type']=="Explicit"):
				explicitRelationList.append(relation)
			if(relation['Type']!="Explicit" and relation['Type']!="AltLex"):
				print "hmmma",relation['Type']
	return implicitRelationList,explicitRelationList


def explicitConnectiveFeatureGeneration(documentList,explicitRelationList):


	print "number of explicit relations",len(explicitRelationList)


	featureCollection=[]
	for explicitRelation in explicitRelationList :
		parseFile=documentList[explicitRelation["DocID"]]
		feature=Feature()

		feature.connectiveString(explicitRelation)
		feature.connectivePOS(parseFile,explicitRelation)
		feature.previousWord(parseFile,explicitRelation)
		feature.nextWord(parseFile,explicitRelation)
		feature.connectiveSelfCategory(parseFile,explicitRelation)	
		feature.connectiveParentSelfCategory(parseFile,explicitRelation)	
		feature.connectiveLeftSiblingSelfCategory(parseFile,explicitRelation)
		feature.connectiveRightSiblingSelfCategory(parseFile,explicitRelation)
		feature.connectiveSyntaxInteraction()
#		feature.connectiveParentLeftSiblingSelfCategory(parseFile,explicitRelation)
#		feature.connectiveParentRightSiblingSelfCategory(parseFile,explicitRelation)
		feature.parentLinkedContext(parseFile,explicitRelation)
#		feature.syntaxSyntaxInteraction()
		feature.setClassLabel(explicitRelation["Sense"][0])
		featureCollection.append(feature)


	for key in featureCollection[0].featureVector.keys():
		print key
	return featureCollection

if __name__=='__main__':
	if(len(sys.argv)<3):
		print "Please train and test document parses and relation data folder location"
		exit()

	trainDocumentLocation=sys.argv[1]+"parses.json"
#	trainRelationLocation=sys.argv[1]+"relations-no-senses.json"
	trainRelationLocation=sys.argv[1]+"relations.json"

	testDocumentLocation=sys.argv[2]+"parses.json"
#	testRelationLocation=sys.argv[2]+"relations-no-senses.json"
	testRelationLocation=sys.argv[2]+"relations.json"
	
	trainDocumentList,trainRelationList=readDocuments(trainDocumentLocation,trainRelationLocation)
	testDocumentList,testRelationList=readDocuments(testDocumentLocation,testRelationLocation)


	trainImplicitRelationList,trainExplicitRelationList=divideRelations(trainRelationList)
	testImplicitRelationList,testExplicitRelationList=divideRelations(testRelationList)


	trainExplicitFeatureCollection=explicitConnectiveFeatureGeneration(trainDocumentList,trainExplicitRelationList)

#	createDirectory("featureCollection/explicitRelation/")
#	for featureNum in range(0,len(trainExplicitFeatureCollection)):
#		exportModel("featureCollection/explicitRelation/"+str(featureNum),trainExplicitFeatureCollection[featureNum])

	trainModel(trainExplicitFeatureCollection,"explicitModel")

	testExplicitFeatureCollection=explicitConnectiveFeatureGeneration(testDocumentList,testExplicitRelationList)
	
	simpleTrainedModelRun(testExplicitFeatureCollection,"explicitModel","explicitRelation")

#	simpleModelRun(featureCollection,10,"explicitRelation/",False)
	
	#runFeatureCombination(featureCollection,"explictRelationCombo",False)    
