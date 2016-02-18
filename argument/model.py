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
import operator

from util import *
from feature import *
from annotated_data import *
from analysis import *
from  model_api import *
	   
if(len(sys.argv)< 3 ):
	print "Enter feature collection location,to choose features or not"
	exit()

runFeatureCombination(sys.argv[1])

exit()

if(sys.argv[2]=="y" or sys.argv[2]=="Y"):
	chooseFeatures(sys.argv[1])
else:
	simpleModelRun(sys.argv[1])
