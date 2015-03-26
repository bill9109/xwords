#!/usr/bin/evn python

#url = "http://www.shanbay.com/wordlist/77914/75094/?page=4"
from bs4 import BeautifulSoup
import urllib2
import re

shanbay_portal = "http://www.shanbay.com/wordbook/77914/"
shanbay_url = "http://www.shanbay.com/"

def get_pages():
    s = []
    html = urllib2.urlopen(shanbay_portal)
    parsed_html = BeautifulSoup(html)
    for link in parsed_html.find_all(href=re.compile("wordlist")):
        s.append(shanbay_url+link.get('href'))
    return s

def craw_page(url):
    html = urllib2.urlopen(url)
    parsed_html = BeautifulSoup(html)
    for word in parsed_html.find_all('td',attrs={"class":"span2"}):
        print word.text
    
if __name__ == '__main__':
    webs = get_pages()
    for web in webs :
        for page in range(1,5) :
            t = web+"?page=%d"%page
            craw_page(t)
