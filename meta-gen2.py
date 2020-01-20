# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 06:36:01 2019

@author: Sajid Hasan Sifat
"""
# summarizer
# pip install beautifulsoup4
# python -m pip install lxml


import bs4 as bs
import urllib.request
import re
import nltk

nltk.download('stopwords')
import heapq

source = urllib.request.urlopen('https://globalone.org.uk/assc/').read()
soup = bs.BeautifulSoup(source)

soup = bs.BeautifulSoup(source, 'lxml')

# get text
text1 = ""
text2 = ""
text3 = ""
# text1 = soup.get_text()
# text2 = soup.get_text()
# text3 = soup.get_text()


# parse url data

for paragraph in soup.find_all('div'):
    text1 += paragraph.text

for paragraph in soup.find_all('p'):
    text2 += paragraph.text

for paragraph in soup.find_all('tr'):
    text3 += paragraph.text

text = ""
text = text1 + text2 + text3
# preprocessing data

text = re.sub(r'\[[0-9]*\]+', ' ', text)
text = re.sub(r'\s+', ' ', text)
clean_text = text.lower()
clean_text = re.sub(r'\W', ' ', clean_text)
clean_text = re.sub(r'\d', ' ', clean_text)
clean_text = re.sub(r'\s+', ' ', clean_text)

# tokenize
sentences = nltk.sent_tokenize(text)

stop_words = nltk.corpus.stopwords.words('english')

# histogram

word2count = {}
for word in nltk.word_tokenize(clean_text):
    if word not in stop_words:
        if word not in word2count.keys():
            word2count[word] = 1
        else:
            word2count[word] += 1

# weighted histogram
for key in word2count.keys():
    word2count[key] = word2count[key] / max(word2count.values())

# scoring sentences
sent2score = {}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word2count.keys():
            if len(sentence.split(' ')) < 35 and len(sentence.split(' ')) > 8:
                if sentence not in sent2score.keys():
                    sent2score[sentence] = word2count[word]
                else:
                    sent2score[sentence] += word2count[word]

# summarizing

best_sentences = heapq.nlargest(5, sent2score, key=sent2score.get)

print('------------- Summary --------------')
for sentences in best_sentences:
    print(sentences)

