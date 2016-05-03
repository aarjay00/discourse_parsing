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
		feature.previousWordandConnective(parseFile,explicitRelation)
		feature.connectiveSelfCategory(parseFile,explicitRelation)	
		feature.connectiveLeftSiblingSelfCategory(parseFile,explicitRelation)
		feature.connectiveRightSiblingSelfCategory(parseFile,explicitRelation)
		feature.connectiveSyntaxInteraction()
		feature.syntaxSyntaxInteraction()
		feature.setClassLabel(explicitRelation["Sense"][0])
		featureCollection.append(feature)

	createDirectory("featureCollection/explicitRelation/")
	for featureNum in range(0,len(featureCollection)):
		exportModel("featureCollection/explicitRelation/"+str(featureNum),featureCollection[featureNum])
		
	simpleModelRun(featureCollection,10,"explicitRelation/",False)

if __name__=='__main__':
	if(len(sys.argv)<2):
		print "Please input document parses and relation data folder location"
		exit()

	documentLocation=sys.argv[1]+"parses.json"
#	relationLocation=sys.argv[1]+"relations-no-senses.json"
	relationLocation=sys.argv[1]+"relations.json"

	documentList,relationList=readDocuments(documentLocation,relationLocation)

	print len(relationList)

	senses=[]
	for relation in relationList:
		senses.append(relation["Sense"][0])
	senses=sorted(set(senses))
	for s in senses:
		print s


	implicitRelationList,explicitRelationList=divideRelations(relationList)


	explicitConnectiveFeatureGeneration(documentList,explicitRelationList)


	print implicitRelationList[0]['Arg1']['RawText']

	doc_id=implicitRelationList[0]['DocID']
	
	for w in implicitRelationList[0]['Arg1']['TokenList']:
		print  documentList[doc_id]['sentences'][w[3]]['words'][w[4]][0],
	print ""

#	print documentList[doc_id]['sentences'][0]['parsetree']
#	print documentList[doc_id]['sentences'][0]['dependencies']
#	print documentList[doc_id]['sentences'][0]['words']


	print len(implicitRelationList),len(explicitRelationList)
