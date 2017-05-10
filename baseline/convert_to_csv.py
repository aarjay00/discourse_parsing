import  numpy as np
from sklearn.feature_extraction import DictVectorizer
import cPickle as pickle
from folderWalk import folderWalk
import util
def convert_to_csv(file_path,output_file_path):
    file_list = folderWalk(file_path)
    dict_feature_list = []
    dict_class_list = []
    for file in file_list:
        feature = util.loadModel(file)
        dict_feature_list.append(dict(feature.featureList))
        dict_class_list.append({"class":feature.classLabel})

    feature_list = convert_dict_to_feature_vector(dict_feature_list)
    class_list = convert_dict_to_feature_vector(dict_class_list)
    np.savetxt(output_file_path,np.asarray(feature_list),delimiter=",",fmt="%1.0f")
    np.savetxt(output_file_path+"_labels",np.asarray(class_list),delimiter=",",fmt="%1.0f")


def convert_dict_to_feature_vector(feature_dict_list):

    vectorizer = DictVectorizer(sparse=False)
    feature_vector_list = vectorizer.fit_transform(feature_dict_list)
    return feature_vector_list