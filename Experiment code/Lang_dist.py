import scipy
import H_Map
import numpy as np
import example
import os




def main(path, labels):
    dictionary_lang = {}
    dictionary_opt = {}
    myPath = path  
    myFiles=os.listdir(myPath)
    for f1 in myFiles:
        
        f = open(str(f1), 'rU')
        file_text=f.read()
        
        list_ques=file_text.split("}")
        languages=labels
        for key in languages:
           
           
            dictionary_temp = {}
            dictionary_temp2 = {}
            for j in languages:
                if(j!=key):
                    dictionary_temp[j] = 0
                    dictionary_temp2[j] = 0
            dictionary_lang[key] = dictionary_temp
            dictionary_opt[key] = dictionary_temp2
         
        for i in list_ques[:-1]:
            target=i.split('target": "')[1].split('"')[0]
            
            guess=i.split('guess": "')[1].split('"')[0]
            if((target in languages) and (guess in languages) and (target !=guess)):
               
                
                dictionary_lang[target][guess] = dictionary_lang[target][guess]+1
                dictionary_lang[guess][target] = dictionary_lang[guess][target]+1
            options=i.split('choices": [')[1].split('],')[0]
            options=options.split(', ')
            if(len(options)>3 and (target in languages)): 
                for j in options:
                    
                    j=j.replace('"', '')
                    if (j != target)and (j in languages):
                        dictionary_opt[target][j]=dictionary_opt[target][j]+1
                        dictionary_opt[j][target]=dictionary_opt[j][target]+1
        #print(dictionary_lang)
        #print(dictionary_opt)

        DRF = np.zeros((len(languages),len(languages)))
        for k in range(len(languages)):
            for l in range(len(languages)):
                if(k!=l):
                    x=languages[k]
                    y=languages[l]
                    DRF[k,l]=1-dictionary_lang[x][y]/dictionary_opt[x][y]
                else: 
                    DRF[k,l]=0
        #print(DRF)
        #H_Map.main(DRF)
        #UPGMA.main(DRF,languages)
        return DRF
