#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 19:18:30 2021

@author: cubo
"""
import argparse
import pandas as pd
import pickle
import sys

parser = argparse.ArgumentParser(description='options: cl, tl, cr, tr')

parser.add_argument("vec_mod_switcher", help=
                    'cl: countVectorizer + LogReg\
                        tl: tfidtVectorizer + LogReg\
                            cr: countVectorizer + RandFor\
                                tr: tfidtVectorizer + RandFor')
                   
parser.add_argument("snippet", help="small piece of song (str)", type=str)
args = parser.parse_args()
vec_mod = args.vec_mod_switcher
snippet =[args.snippet]


if vec_mod == 'cl':
    with open("../data/processed_data/fitted_pipelines/cvec_lr_fin_model.pickle", "rb") as file:
              fitted_model = pickle.load(file)   
elif vec_mod == 'tl':
    with open("../data/processed_data/fitted_pipelines/tfidt_lr_fin_model.pickle", "rb") as file:
              fitted_model = pickle.load(file)
elif vec_mod == 'cr':
    with open("../data/processed_data/fitted_pipelines/cvec_rf_fin_model.pickle", "rb") as file:
              fitted_model = pickle.load(file)
elif vec_mod == 'tr':
    with open("../data/processed_data/fitted_pipelines/tfidt_rf_fin_model.pickle", "rb") as file:
              fitted_model = pickle.load(file)
else:
    print('Error! vectorizer must be "cl", "tl", "cr", or "tr"')
    print()
    sys.exit()
     
pred = fitted_model.predict_proba(snippet)
predDF = pd.DataFrame(pred,
        columns = fitted_model.classes_,
        index = snippet)
print(predDF)  
   
    
   
    
   
    
   