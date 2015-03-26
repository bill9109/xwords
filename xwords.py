#!/usr/bin/env python
# -*_ coding:utf-8 -*-
 
import sys
import urllib2
import json
import string

shanbay_api = 'https://api.shanbay.com/bdc/search/?word='
wikipedia_api = 'http://en.wikipedia.org/w/api.php?action=query&prop=langlinks&continue&format=json&lllimit=500&&titles='
dictionaryapi_dict_key = '9bd7dde6-caae-4265-bd33-d1cf98b3a1ac'
dictionaryapi_thes_key = '4ab2e225-f16a-4fc4-8296-8837b03b762e'

ignore_file = './db/ignore'
known_file = './db/known'
prep_file = './db/prep'
pron_file = './db/pron'

toelf_dict_uri = './dict/toefl_xdf'

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
    ignores = load_ignore()
    if word in ignores :
        return False
    return True

def search_shanbay(word):
    js = json.load(urllib2.urlopen(shanbay_api+word))
    pronun = ""
    defin = ""
    if js['status_code'] == 0:
        pronun = js['data']['pronunciation'].encode('utf-8')
        defin = js['data']['definition'].encode('utf-8').replace('\n','\t')
    return '/'+pronun+'/'+defin

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
    text = text.replace("'s"," ")
    trans = string.maketrans("',.;!?-","       ")
    text = text.translate(trans)
    words = text.lower().split()
    words = [x for x in words if isword(x)]
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

def count_words(words):
    wordcount = {}
    for word in words :
        if word in wordcount :
            wordcount[word] +=1
        else :
            wordcount[word] = 1
    #fre = sorted(wordcount,key=wordcount.get,reverse=True)
    return wordcount

def sort_words(words):
    res = sorted(words,key=words.get,reverse=True)
    return res

def load_toefl():
    words = []
    f = open(toelf_dict_uri,"rU")
    for line in f :
        words.append(line.rstrip())
    return words
    
def istoefl(word):
    return word in toelf

def print_word(word):
    s = "" 
    if istoefl(word):
        s += '*'
    s+="\t%d"%counter[word]  #print frefrequency of the word in text"
    s+="\t"+word  #print the word 
    s+="\t"+search_shanbay(word)
    print s

    
if __name__ == '__main__':

    twords = load_words(sys.argv[1])
    counter = count_words(twords)
    fre = sort_words(counter)
    toelf = load_toefl()

    for word in fre :
        if word in toelf:
            print_word(word)

