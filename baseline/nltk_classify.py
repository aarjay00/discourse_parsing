
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
reload(sys)
sys.setdefaultencoding("utf-8")
import  cPickle as pickle
import nltk
import numpy as np
from nltk.classify import SklearnClassifier
from sklearn.linear_model import LogisticRegression as maxent


def genModel(corpus):
	classifier = nltk.classify.NaiveBayesClassifier.train(corpus)
	classifier = nltk.classify.MaxentClassifier.train(corpus,"GIS", trace=0, max_iter=100)
	classifier=SklearnClassifier(maxent()).train(corpus)
	return classifier

def runModel(corpus,corpus_f,corpus_l,cycleLen):
	combinedData=zip(corpus,corpus_f,corpus_l)
	for i in range(0,20):
		np.random.shuffle(corpus)
	corpus,corpus_f,corpus_l=zip(*combinedData)
	
	avg_p=0.0
	avg_r=0.0
	avg_f=0.0
	avg_acc=0.0
	for iteration in range(0,cycleLen):
		print "Iteration",iteration,"-"*50
		size=len(corpus)/cycleLen
		start=size*iteration
		end=start+size
		test_f=corpus_f[start:end]
		test_l=corpus_l[start:end]
		train=corpus[:start]+corpus[end+1:]
		
		tp=0
		tn=0
		fp=0
		fn=0
		
		classifier=genModel(train)
		tNum=0
		for testInst in test_f:
			pdist=classifier.prob_classify(testInst)
			if(pdist.prob("Yes") >= pdist.prob("No")):
				if(test_l[tNum]=="Yes"):
					tp+=1
				else:
					fp+=1
			else:
				if(test_l[tNum]=="No"):
					tn+=1
				else:
					fn+=1
			tNum+=1
		print tp,fp,tn,fn	 	
		p=1.0*tp/(tp+fn)
		r=1.0*tp/(tp+fp)
		f=2.0*p*r/(p+r)
		acc=1.0*(tp+tn)/(tp+tn+fp+fn)
		avg_p=(avg_p*iteration+p)/(iteration+1)
		avg_r=(avg_r*iteration+r)/(iteration+1)
		avg_f=(avg_f*iteration+f)/(iteration+1)
		avg_acc=(avg_acc*iteration+acc)/(iteration+1)
	print avg_p,avg_r,avg_f,avg_acc

			




filePath="./fList"
fileFD=codecs.open(filePath,"rb")
fcollec=pickle.load(fileFD)
fileFD.close()


corpus=[]
corpus_f=[]
corpus_l=[]

for f in fcollec:
	d={}
	label=f[1]
	features=f[0]
	for feature in features:
		d[feature[0]]=feature[1]
	corpus.append((d,label))
	corpus_f.append(d)
	corpus_l.append(label)


runModel(corpus,corpus_f,corpus_l,10)



