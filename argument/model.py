import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
import  cPickle as pickle
import nltk
import numpy as np
import time
import itertools
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression as maxent
from sklearn.svm import SVC


from util import *
from feature import *
from annotated_data import *
from analysis import *




def genClassifer(corpus):
	classifier=SklearnClassifier(maxent()).train(corpus)
	return classifier


def convertFeatureCollection(featureCollection,chooseFeatures=False,chosenFeatures=[]):

	dataSet=[]
	for feature in featureCollection:
		featureList=feature.featureList
		d={}
		for f in featureList:
			if not chooseFeatures:
				d[f[0]]=f[1]
			elif f[0] in chosenFeatures:
				d[f[0]]=f[1]
		dataSet.append((d,feature.classLabel))
	return dataSet
def featureSelection(featureCollection):
	featureSet=[f[0] for f in featureCollection[0].featureList]
	chosenFeatureSet=[]
	print "Choose features to be used"
	for f  in featureSet:
		take=raw_input(f)
		if(take=="y" or take=="Y"):
			chosenFeatureSet.append(f)
	return chosenFeatureSet


def simpleClassify(dataSet,foldNum):

	averageAcc=0.0
	dataSize=len(dataSet)
	negativeSamples=[]
	for iteration in range(foldNum):
		start=iteration*(dataSize/foldNum)
		end=start+(dataSize/foldNum)
		testDataSet=dataSet[start:end]
		trainDataSet=dataSet[:start]+dataSet[end+1:]
		classifier=genClassifer(trainDataSet)


		positive=0
		negative=0
		sampleNum=0
		for sample in testDataSet:
			sampleLabel=sample[1]
			sampleFeature=sample[0]
			result=classifier.prob_classify(sampleFeature)
			if(result.prob(sampleLabel)>.5):
				positive+=1
			else:
			 	negative+=1
			 	negativeSamples.append(sampleNum+start)
			sampleNum+=1
		accuracy=1.0*positive/(positive+negative)
#		print "accuracy for round %d is %f"%(iteration,accuracy)
		averageAcc=(averageAcc*iteration+accuracy)/(iteration+1)
	print "avgAccuracy is ",averageAcc
	return negativeSamples



def featureCombinations(featureCollection):
	featureSet=[f[0] for f in featureCollection[0].featureList]
	featureCombo=[combo for x in range(1,len(featureSet)+1) for combo in itertools.combinations(featureSet,x) ]
	print len(featureCombo)
	for featureSet in featureCombo:
		print featureSet
		dataSet=convertFeatureCollection(featureCollection,True,featureSet)
		simpleClassify(dataSet,10)
		

	   
if(len(sys.argv)< 3 ):
	print "Enter feature collection location,to choose features or not"
	exit()
	
featureCollection=loadModel(sys.argv[1])

featureCombinations(featureCollection)	
	
chooseFeatures=False
chosenFeatureSet=[]
if(sys.argv[2]=="y" or sys.argv[2]=="Y"):
	chosenFeatureSet=featureSelection(featureCollection)
	chooseFeatures=True

featureSet=[f[0] for f in featureCollection[0].featureList]

dataSet=convertFeatureCollection(featureCollection,chooseFeatures,chosenFeatureSet)
errorSamplesNum=simpleClassify(dataSet,10)


errorSamples=[featureCollection[num] for num in errorSamplesNum]
studyErrors(errorSamples,"arg1Pos")
