#k-fold cross validation file maker majigger
#!!!!!! MAY NEED TO REWRITE FOR HOLDOUT DATA TO TEST ON AT END!!!!!!

import os,re,sys
directory_of_wordsfiles ="data_WSD/word files"
directory_of_outfiles = "data_WSD/k-fold_CV"
words = []
for directory in os.listdir(directory_of_wordsfiles):
    if directory !=".DS_Store":
        words.append(directory)
for directory in os.listdir(directory_of_outfiles):#2-10
    if directory != ".DS_Store":
        folds = int(directory)
        pwd = "data_WSD/k-fold_CV/"+directory
        for each in words: #each word's 2-10 folders
            if not os.path.exists(pwd+"/"+each[:-4]):
                os.makedirs(pwd+"/"+each[:-4])
            x = 1#cycle from 1 up to x for each folder
            g = open(directory_of_wordsfiles+"/"+each,"r")
            add_to_file=""
            for line in g:
                if x > folds:
                    x = 1
                try:
                    f=open(pwd+"/"+each[:-4]+"/"+str(x)+".txt","a")
                except:
                    f=open(pwd+"/"+each[:-4]+"/"+str(x)+".txt","w")
                if len(line)!=1:
                    add_to_file+=line
                else:
                    f.write(add_to_file)
                    add_to_file = ""
                    x+=1
                    
                

                
