from ExtractDiscourseInfo import *

#Usage : filepath for pdtb-data.json && folderpath for rawdata
#return a list of relation class objects
data=extractDiscourseInfo("data/conll15st-train-dev/conll15st_data/conll15-st-03-04-15-dev/pdtb-data.json","data/conll15st-train-dev/conll15st_data/conll15-st-03-04-15-dev/raw") 
#Prints all connective Information in file
Print(data,"output") 

