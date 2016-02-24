import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")

import crfsuite
import  cPickle as pickle
import nltk
import numpy as np
import time
import itertools
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression as maxent
from sklearn.svm import SVC
import operator

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
	return (averageAcc,negativeSamples)


def featureCombinations(featureCollection):
	featureSet=[f[0] for f in featureCollection[0].featureList]
	featureCombo=[combo for x in range(1,len(featureSet)+1) for combo in itertools.combinations(featureSet,x) ]
	print len(featureCombo)
	resultCollection=[]
	for featureSet in featureCombo:
		dataSet=convertFeatureCollection(featureCollection,True,featureSet)
		acc,err=simpleClassify(dataSet,10)
		resultCollection.append((acc,featureSet,err))
	resultCollection=sorted(resultCollection,key=operator.itemgetter(0))
	for i in resultCollection:
		print i[0],i[1]
	errorCollection = [featureCollection[num] for num in resultCollection[-1][2]]
	studyErrors(errorCollection,"arg2SubTreePos")
	return resultCollection[-1]



def runFeatureCombination(featureCollectionLocation):	   
	
	featureCollection=loadModel(sys.argv[1])

	return featureCombinations(featureCollection)	
def chooseFeatures(featureCollectionLocation):
	featureCollection=loadModel(sys.argv[1])
	chosenFeatureSet=featureSelection(featureCollection)
	
	featureSet=[f[0] for f in featureCollection[0].featureList]
	chosenFeatureSet=featureSelection(featureSet)
	dataSet=convertFeatureCollection(featureCollection,True,chosenFeatureSet)
	
	avgAccuracy,errorSamplesNum=simpleClassify(dataSet,10)
	
	errorSamples=[featureCollection[num] for num in errorSamplesNum]
	print "avgAccuracy is ",averageAcc
	studyErrors(errorSamples,"arg2SubTreePos")
def simpleModelRun(featureCollectionLocation):
	featureCollection=loadModel(sys.argv[1])

	featureSet=[f[0] for f in featureCollection[0].featureList]

	dataSet=convertFeatureCollection(featureCollection,False,featureSet)
	avgAccuracy,errorSamplesNum=simpleClassify(dataSet,10)

	errorSamples=[featureCollection[num] for num in errorSamplesNum]
	print "avgAccuracy is ",averageAcc
	studyErrors(errorSamples,"arg2SubTreePos")


def getModel(featureCollection,iterationNum,foldNum):
	
	featureSet=[f[0] for f in featureCollection[0].featureList]
	dataSet=convertFeatureCollection(featureCollection,False,featureSet)
	
	dataSize=len(dataSet)
	start=iterationNum*(dataSize/foldNum)
	end=start+(dataSize/foldNum)
	testDataSet=dataSet[start:end]
	trainDataSet=dataSet[:start]+dataSet[end+1:]
	classifier=genClassifer(trainDataSet)
	return classifier



# Inherit crfsuite.Trainer to implement message() function, which receives
# progress messages from a training process.
class Trainer(crfsuite.Trainer):
    def message(self, s):
        # Simply output the progress messages to STDOUT.
        sys.stdout.write(s)

def extractCRFFeatureCollection(featureCollectionLocation,iterationNum,foldNum,train=True):
	
	featureSeqCollection=loadModel(featureCollectionLocation)
	dataSize=len(featureSeqCollection)
	start=iterationNum*(dataSize/foldNum)
	end=start+dataSize/foldNum
	if(train):
		featureSeqCollection=featureSeqCollection[:start]+featureSeqCollection[end+1:]
	else:
	 	featureSeqCollection=featureCollectionLocation[start:end]
	crfFeatureCollection=[]
	for featureSeq in featureSeqCollection:
		xseq = crfsuite.ItemSequence()
		yseq = crfsuite.StringList()
		for feature in featureSeq:
			item=crfsuite.Item()
			for f in feature:
				item.append(crfsuite.Attribute(f[0]+"="+str(f[1])))
			xseq.append(item)
			yseq.append(feature.classLabel)
		crfFeatureCollection.append((xseq,tuple(yseq)))
	return crfFeatureCollection
'''
	xseq = crfsuite.ItemSequence()
	yseq = crfsuite.StringList()
	for line in fi:
		line = line.strip('\n')
		if not line:
		# An empty line presents an end of a sequence.
			yield xseq, tuple(yseq)
			xseq = crfsuite.ItemSequence()
			yseq = crfsuite.StringList()
			continue

		# Split the line with TAB characters.
		fields = line.split('\t')

		# Append attributes to the item.
		item = crfsuite.Item()
		for field in fields[1:]:
			p = field.rfind(':')
			if p == -1:
			# Unweighted (weight=1) attribute.
				item.append(crfsuite.Attribute(field))
			else:
			# Weighted attribute
				item.append(crfsuite.Attribute(field[:p], float(field[p+1:])))

		# Append the item to the item sequence.
		xseq.append(item)
		# Append the label to the label sequence.
		yseq.append(fields[0])
'''
def genCRFModel(featureCollectionLocation,iterationNum,foldNum,crfModelLocation):
	# Create a Trainer object.
	trainer = Trainer()
	crfCollection=extractCRFFeatureCollection(featureCollectionLocation,iterationNum,foldNum,True)
	for feature in crfFeatureCollection:
		trainer.append(feature[0],feature[1],0)
	# Use L2-regularized SGD and 1st-order dyad features.
	trainer.select('l2sgd', 'crf1d')

	# Set the coefficient for L2 regularization to 0.1
	trainer.set('c2', '0.1')
	
	# This demonstrates how to list parameters and obtain their values.
#	for name in trainer.params():
#		print name, trainer.get(name), trainer.help(name)

	# Start training; the training process will invoke trainer.message()
	# to report the progress.
	trainer.train(crfModelLocation, -1)
	return trainer
def runCRFModel(featureCollectionLocation,iterationNum,foldNum,crfModelLocation):

	# Create a tagger object.
	tagger = crfsuite.Tagger()
	# Load the model to the tagger.
	tagger.open(sys.argv[1])
	crfCollection=extractCRFFeatureCollection(featureCollectionLocation,itertionNum,foldNum,False)
	for feature in crfCollection:
		# Tag the sequence.
		xseq=feature[0]
		tagger.set(xseq)
		# Obtain the label sequence predicted by the tagger.
		yseq = tagger.viterbi()
		# Output the probability of the predicted label sequence.
		print tagger.probability(yseq)
		for t, y in enumerate(yseq):
			# Output the predicted labels with their marginal probabilities.
			print '%s:%f' % (y, tagger.marginal(y, t))
		print
