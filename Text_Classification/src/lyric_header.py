#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import time
import re
import os
from bs4 import BeautifulSoup
import spacy



def extract_artists_page(artists, input_url, destination_dir):
    '''artists is a list of strings (artist names). input_url is a str (url)
        destination_dir is a str (dir path).
        The function loop on the artists and find the artist page and save
        the artist_page link in destination_dir'''
    for artist in artists:
        url = input_url + artist
        print(url)
        resp = requests.get(url)
        with open(destination_dir + artist.replace(' ', '_') + '.html', 'w',    
                encoding='utf8') as file:
            file.write(resp.text)
        time.sleep(0.5)
    return None

def create_lyrics_links_list(input_dir):
    '''input_dir is a str (path of the dir where are artist pages)
       The function returns 2 dictionaries:
           1) lyrics_links_dict with the name of artists as key and
              the links of songs as values
           2) title_dict with the name of the artist as key and the 
                title of the songs as values'''
    lyrics_links_dict = {}
    title_dict = {}
    regLyric = r"(/lyric/\d+/\w+\+?\w+/([\w+\+]+))\""
    regArtist = r"\w+-?\w+"
    for filename in os.listdir(input_dir):
        matchArtist = re.search(regArtist, filename)
        nameArtist = matchArtist.group(0)
        lyrics_links_dict[nameArtist] = []
        title_dict[nameArtist] = []
        with open(os.path.join(input_dir, filename), 'r') as file:
            text = file.read()
            links = re.findall(regLyric, text)
        for link in links:
            lyrics_links_dict[nameArtist].append('https://www.lyrics.com' + link[0])
            title_dict[nameArtist].append(link[1].replace('+', '_'))
    return lyrics_links_dict, title_dict

def extract_lyrics_page(lyrics_links_dict, title_dict, dest_dir):
    '''lyrics_links_dict and title_dict are dictionaries. The first
       contains autor as key and song links as values and the second
       contains autor as key and song titles as values.
       The function create an html file for each song and store it in
       a directory'''
    for artist, links in lyrics_links_dict.items():
        for i in range(10):
            url = links[i]
            resp = requests.get(url)
            filename = str(i) + '.' + title_dict[artist][i] + '__' +  artist + '.html'
            with open(dest_dir +  filename, 'w') as file:
                print('Writing...', filename)
                file.write(resp.text)
            time.sleep(0.3)
    return None

def generate_text_artist_DF(song_dir):
    '''song_dir is a str (path of the directory where the lyriks.html
       are saved).
    The function extrapolate the text and the name of the autor and 
    generate and returns a dictionary data with 2 keys: 'lyrics' 
    and 'artist_name'. '''   
    data ={'lyric':[], 'artist_name':[]}    
    for filename in os.listdir(song_dir):
        if filename.endswith(".html"):
            with open(os.path.join(song_dir, filename), 'r') as file:
                html = file.read()
                soup = BeautifulSoup(html, features="html.parser")
                try:
                    artist = soup.find(class_="lyric-artist").a.text
                    artist = artist.replace(' ', '_')
                    lyric_text = soup.pre.text
                except AttributeError:
                    continue         
                #print(artist)
                #print(lyric_text)
                if artist == "Elton_John" or \
                    artist == "James_Brown" or \
                    artist == "Madonna":
                    data['lyric'].append(lyric_text)
                    data['artist_name'].append(artist)
    return data

#Cleaning data 
    
def clean_text(X_df):
    '''X_df is a Pandas DataFrame with two columns:
        'lyric' and 'artist_name'. The function uses
        spaCy to clean the text in the 'lyric' column.
        It returns a cleaned dictionary'''       
    #converting the lyric column of X to a list
    nlp = spacy.load("en_core_web_md")
    lyrics_list = X_df['lyric'].tolist()
    artist_list = X_df['artist_name'].tolist()
    # define a new dictionary for the cleaned text
    cleaned_lyrics_dict = {'lyric':[], 'artist_name':artist_list}
    #loop to tokenize each lyric and clean it
    for i in range(len(lyrics_list)):
        tokens = nlp(lyrics_list[i])
        token_list = []
        for token in tokens:
            if (token.is_alpha)\
            and (not token.is_punct) \
            and (not token.is_left_punct) \
            and (not token.is_right_punct) \
            and (not token.is_digit) \
            and (not token.is_bracket) \
            and (not token.is_oov) \
            and (not token.is_currency) \
            and (not token.is_quote) \
            and \
            ((token.pos_ == 'PROPN') \
            or (token.pos_ == 'VERB') \
            or (token.pos_ == 'NOUN') \
            or (token.pos_ == 'ADJ') \
            or (token.pos_ == 'NUM')):
                word = token.lemma_          
                token_list.append(word.lower())
        cleaned_lyric = " ".join(token_list)
        cleaned_lyrics_dict['lyric'].append(cleaned_lyric)     
    return cleaned_lyrics_dict



































