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
import operator

from util import *
from feature import *
from annotated_data import *
from analysis import *



# Inherit crfsuite.Trainer to implement message() function, which receives
# progress messages from a training process.
class Trainer(crfsuite.Trainer):
    def message(self, s):
        # Simply output the progress messages to STDOUT.
        sys.stdout.write(s)

def extractCRFFeatureCollection(featureSeqCollection,iterationNum,foldNum,train):
	
#	featureSeqCollection=loadModel(featureCollectionLocation)
	dataSize=len(featureSeqCollection)
	start=iterationNum*(dataSize/foldNum)
	end=start+dataSize/foldNum
	if(train):
		featureSeqCollection=featureSeqCollection[:start]+featureSeqCollection[end+1:]
	else:
	 	featureSeqCollection=featureSeqCollection[start:end]
	crfFeatureCollection=[]
	for featureSeq in featureSeqCollection:
		xseq = crfsuite.ItemSequence()
		yseq = crfsuite.StringList()
		for feature in featureSeq:
			item=crfsuite.Item()
			for f in feature.featureList:
				item.append(crfsuite.Attribute(str(f[0])+"="+str(f[1])))
			xseq.append(item)
			yseq.append(feature.classLabel)
		crfFeatureCollection.append((xseq,yseq))
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
def genCRFModel(featureCollection,iterationNum,foldNum,crfModelLocation):
	# Create a Trainer object.
	trainer = Trainer()
	crfFeatureCollection=extractCRFFeatureCollection(featureCollection,iterationNum,foldNum,True)
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
def runCRFModel(featureCollection,iterationNum,foldNum,crfModelLocation):

	# Create a tagger object.
	tagger = crfsuite.Tagger()
	# Load the model to the tagger.
	tagger.open(crfModelLocation)
	crfCollection=extractCRFFeatureCollection(featureCollection,iterationNum,foldNum,False)
	resultSeqCollection=[]
	for feature in crfCollection:
		# Tag the sequence.
		xseq=feature[0]
		tagger.set(xseq)
		# Obtain the label sequence predicted by the tagger.
		yseq = tagger.viterbi()
		# Output the probability of the predicted label sequence.
		print tagger.probability(yseq)
		resultSeq=[]
		for t, y in enumerate(yseq):
			# Output the predicted labels with their marginal probabilities.
			print '%s:%f' % (y, tagger.marginal(y, t))
			resultSeq.append(y)
		print
		resultSeqCollection.append(resultSeq)
	return resultSeqCollection
