#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 09:35:34 2021

@author: cubo
"""
import pandas as pd
import requests
import pickle
from lyric_header import create_lyrics_links_list
from lyric_header import generate_text_artist_DF
from lyric_header import clean_text

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

'''
parser = argparse.ArgumentParser(description='Use CVec or Tfidf')
parser.add_argument("vectorizer", help="CVec to use CountVectorizer\
                    or Tfidf to use TfidfVectorizer")
parser.add_argument("classifier", help="lr: LogisticRegressor\
                    or rf: RandomForest")
args = parser.parse_args()
vectorizer = args.vectorizer
classif = args.classifier
'''
base_url = 'https://www.lyrics.com/artist/'
resp = requests.get(base_url)
artists = ['Elton-John' , 'James-Brown', 'Madonna']
artist_dir = r'../data/raw_data/artists/'
song_dir = r'../data/raw_data/songs/'

#extract_artists_page(artists, base_url, artist_dir)

lyrics_links_dict, title_dict = create_lyrics_links_list(artist_dir)
#extract_lyrics_page(lyrics_links_dict, title_dict, song_dir)

data = generate_text_artist_DF(song_dir)
lyricsDF = pd.DataFrame(data)

cleaned_lyrics_dict = clean_text(lyricsDF)

cleaned_lyricsDF = pd.DataFrame(cleaned_lyrics_dict)
#cleaned_lyricsDF.to_csv('../data/processed_data/cleaned_lyrics.csv')

## importing the cleaned_lyrics and convert into DF    
#clean_lyricsDF = pd.read_csv('../data/processed_data/cleaned_lyrics.csv', 
#                                 index_col=0)

y = cleaned_lyricsDF['artist_name']
x = cleaned_lyricsDF['lyric']

x_t, x_v, y_t, y_v = train_test_split(x,y)

with open("../data/processed_data/Xy/x_t.pickle", "wb") as file:
    pickle.dump(x_t, file)
with open("../data/processed_data/Xy/x_v.pickle", "wb") as file:
    pickle.dump(x_v, file)
with open("../data/processed_data/Xy/y_t.pickle", "wb") as file:
    pickle.dump(y_t, file)
with open("../data/processed_data/Xy/y_v.pickle", "wb") as file:
    pickle.dump(y_v, file)

### cvec lr
cvec_lr_model = make_pipeline(
                            CountVectorizer(),
                            LogisticRegression(class_weight='balanced',
                                               max_iter=10000)
                            )

grid_lr = {'logisticregression__C' : [0.5, 1, 1.5]}

cv = GridSearchCV(
    cvec_lr_model,
    param_grid=grid_lr,
    scoring='balanced_accuracy',
    return_train_score=True,
    n_jobs=1)

print('Fitting cvec_lr_model')
cv.fit(x_t, y_t)

cvec_lr_final_model = cv.best_estimator_

print('Saving model ...')
with open('../data/processed_data/fitted_pipelines/cvec_lr_fin_model.pickle', \
          'wb') as file:
    pickle.dump(cvec_lr_final_model, file)
 
### tfidt lr   
tfidt_lr_model = make_pipeline(
                            TfidfVectorizer(),
                            LogisticRegression(class_weight='balanced',
                                               max_iter=10000)
                            )

cv = GridSearchCV(
    tfidt_lr_model,
    param_grid=grid_lr,
    scoring='balanced_accuracy',
    return_train_score=True,
    n_jobs=1)

print('Fitting tfidt_lr_model')
cv.fit(x_t, y_t)

tfidt_lr_final_model = cv.best_estimator_

print('Saving model ...')
with open('../data/processed_data/fitted_pipelines/tfidt_lr_fin_model.pickle', \
          'wb') as file:
    pickle.dump(tfidt_lr_final_model, file)
    
### cvec rf   
cvec_rf_model = make_pipeline(
                            CountVectorizer(),
                            RandomForestClassifier(),
                            )

grid_rf = {'randomforestclassifier__n_estimators' : [50, 100, 150],
        'randomforestclassifier__max_depth': [4, 6, 8],}

cv = GridSearchCV(
    cvec_rf_model,
    param_grid=grid_rf,
    scoring='balanced_accuracy',
    return_train_score=True,
    n_jobs=1)

print('Fitting cvec_rf_model')
cv.fit(x_t, y_t)

cvec_rf_final_model = cv.best_estimator_

print('Saving model ...')
with open('../data/processed_data/fitted_pipelines/cvec_rf_fin_model.pickle', \
          'wb') as file:
    pickle.dump(cvec_rf_final_model, file) 
    
### tfidt rf   
tfidt_rf_model = make_pipeline(
                            TfidfVectorizer(),
                            RandomForestClassifier(),
                            )

cv = GridSearchCV(
    tfidt_rf_model,
    param_grid=grid_rf,
    scoring='balanced_accuracy',
    return_train_score=True,
    n_jobs=1)

print('Fitting tfidt_rf_model')
cv.fit(x_t, y_t)

tfidt_rf_final_model = cv.best_estimator_

print('Saving model ...')
with open('../data/processed_data/fitted_pipelines/tfidt_rf_fin_model.pickle', \
          'wb') as file:
    pickle.dump(tfidt_rf_final_model, file)  
    
 
    
 
