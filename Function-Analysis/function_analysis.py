import pandas as pd
import numpy as np
pd.set_option("display.precision", 2)

import nltk
from nltk.book import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

import re
import glob

filename = 'Sentiment.csv'
df = pd.read_csv(filename)
fd = df.drop(['Unnamed: 0', 'ChapterNumber', 'ParagraphNumber', 'SentenceNumber', 'TextBeforeRefMention', 'TextWhereRefMention', 'TextAfterRefMention'], axis = 1)

median2 = fd["SourceID"].median()

fd["SourceID"].replace(np.nan,median2,inplace=True)

model1 = fd["Title"].mode().values[0]
model2 = fd["Authors"].mode().values[0]
model3 = fd["ReferenceID"].mode().values[0]
model4 = fd["PublishedDate"].mode().values[0]

fd["Title"] = fd["Title"].replace(np.nan,model1)
fd["Authors"] = fd["Authors"].replace(np.nan,model2)
fd["ReferenceID"] = fd["ReferenceID"].replace(np.nan,model3)
fd["PublishedDate"] = fd["PublishedDate"].replace(np.nan,model4)

#print(fd.isnull().sum())

fd.drop_duplicates(inplace=True)

duplicate = fd.duplicated()
print(duplicate.sum())

data = fd['Title']

def text_cleaner(clean_text):
    rules = [
        {r'>\s+': u'>'},  # remove spaces after a tag opens or closes
        {r'\s+': u' '},  # replace consecutive spaces
        {r'\s*<br\s*/?>\s*': u'\n'},  # newline after a <br>
        {r'</(div)\s*>\s*': u'\n'},  # newline after </p> and </div> and <h1/>...
        {r'</(p|h\d)\s*>\s*': u'\n\n'},  # newline after </p> and </div> and <h1/>...
        {r'<head>.*<\s*(/head|body)[^>]*>': u''},  # remove <head> to </head>
        {r'<a\s+href="([^"]+)"[^>]*>.*</a>': r'\1'},  # show links instead of texts
        {r'[ \t]*<[^<]*?/?>': u''},  # remove remaining tags
        {r'^\s+': u''}  # remove spaces at the beginning
    ]
    for rule in rules:
        for (k, v) in rule.items():
            regex = re.compile(k)
            clean_text = regex.sub(v, clean_text)
            clean_text = clean_text.rstrip()
            return clean_text.lower()

for titles in data:
    tokens = word_tokenize(titles)
    print(tokens)
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in tokens if not w in stop_words]
    filtered_sentence = []
    for w in tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    conv = [line.strip() for line in filtered_sentence]
    texts = [[word.lower() for word in text.split()] for text in conv]
    #print(texts)
    clean_str = text_cleaner(str(texts))
    print(clean_str)
