#!/usr/bin/env python
# -*_ coding:utf-8 -*-
 
import sys
import urllib2
import json

shanbay_api = 'https://api.shanbay.com/bdc/search/?word='
wikipedia_api = 'http://en.wikipedia.org/w/api.php?action=query&prop=langlinks&continue&format=json&lllimit=500&&titles='

ignore_file = './db/ignore'
known_file = './db/known'
prep_file = './db/prep'
pron_file = './db/pron'

ignore_known = True
ignore_prep = True
ignore_pron = True

min_word_len = 3
max_word_len = 15

def isword(word):
    if not word.isalpha() :
        return False
    if len(word)<min_word_len or len(word)>max_word_len :
        return False
    return True

def search_shanbay(word):
    js = json.load(urllib2.urlopen(shanbay_api+word))
    pronun = ""
    defin = ""
    if js['status_code'] == 0:
        pronun = js['data']['pronunciation'].encode('utf-8')
        defin = js['data']['definition'].encode('utf-8').replace('\n','\t')
    return pronun+defin

def search_wikipedia(word):
    wiki_res = urllib2.urlopen(wikipedia_api+word)
    js = json.load(wiki_res)
    if 'langlinks' in js['query']['pages'].values()[0].keys():    
        for x in js['query']['pages'].values()[0]['langlinks'] :
            if x['lang']=='zh':
                return x['*']
    '''
    else:
        return word.upper()+" does not exist on Wikipedia. "
        '''

def load_words(files):
    text = ""
    f = open(files,"rU")
    for line in f :
        text += line
    words = text.lower().split()
    for word in words :
        if not isword(word) :
            words.remove(word)
    return words


def load_ignore():
    files = []
    text = ""
    files.append(ignore_file)
    if ignore_known :
        files.append(known_file)
    if ignore_prep :
        files.append(prep_file)
    if ignore_pron :
        files.append(pron_file)

    for file in files :
        f = open(file,"rU")
        for line in f:
            text += line
    words = text.lower().split()
    return words

def sort_words(words):
    wordcount = {}
    for word in words :
        if word in wordcount :
            wordcount[word] +=1
        else :
            wordcount[word] = 1
    fre = sorted(wordcount,key=wordcount.get,reverse=True)
    return fre

if __name__ == '__main__':

    twords = load_words(sys.argv[1])
    ignore = load_ignore()
    words = sort_words(twords) 

    for word in words :
        if word not in ignore :
            print word,search_shanbay(word)

