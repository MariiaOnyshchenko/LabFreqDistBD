from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import tokenize_uk
import collections
import pymorphy2
import pymorphy2_dicts_uk
with open("земля.txt", encoding = "utf-8") as data_1:
    text_1 = data_1.read()
    
conn = sqlite3.connect('bdlab_1.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS wordforms_freq
                  (word_form VARCHAR,
                  gen_freq INTEGER, 
                  sample_1 INTEGER, 
                  sample_2 INTEGER,
                  sample_3 INTEGER,
                  sample_4 INTEGER,
                  sample_5 INTEGER,
                  sample_6 INTEGER,
                  sample_7 INTEGER,
                  sample_8 INTEGER,
                  sample_9 INTEGER,
                  sample_10 INTEGER,
                  sample_11 INTEGER,
                  sample_12 INTEGER,
                  sample_13 INTEGER,
                  sample_14 INTEGER,
                  sample_15 INTEGER,
                  sample_16 INTEGER,
                  sample_17 INTEGER,
                  sample_18 INTEGER,
                  sample_19 INTEGER,
                  sample_20 INTEGER)
''')

c.execute('''CREATE TABLE IF NOT EXISTS wordforms_all
                  (word_form VARCHAR,
                  lemma VARCHAR,
                  pos VARCHAR)
''')

splitted_1 = tokenize_uk.tokenize_uk.tokenize_words(text_1)
for i in range (1, len(splitted_1)-1):
    #скорочення
    if splitted_1[i] == '.' and splitted_1[i+1][0].islower()==True:
        splitted_1[i-1] = splitted_1[i-1]+'.'
    #слова через дефіс
    if splitted_1[i] == '-':
        splitted_1[i-1] = splitted_1[i-1]+'-'+splitted_1[i+1] 
        splitted_1[i+1]='0'  
splitted_2 = []
for token in splitted_1:
    if token[0].isalpha()==True:
        splitted_2.append(token)
for j in range (len(splitted_2)):
    splitted_2[j]=splitted_2[j].lower()
print(splitted_2)

# перевірка
edited_list = splitted_2[:20000]
print (splitted_2[19999])
print (edited_list[-1])

#ЧАСТИНА 2
dict_of_lists = {}
sample_number = 1
volume = 0
while sample_number < 21:
    dict_of_lists["sample_{0}_list".format(sample_number)] = splitted_2[volume:(volume+1000)]
    volume += 1000
    sample_number +=1

freq_dict={}
def freq(sample_number):
    for i in dict_of_lists.keys():
        if str(sample_number) in i:
            words = dict_of_lists[i]
    counter = collections.Counter(words)
    samp_freq = dict(counter)
    for word_form in samp_freq.keys():
        if word_form not in freq_dict.keys():
            freq_dict[word_form]=[word_form]
            iterator = 1
            while iterator < sample_number:
                freq_dict[word_form].append(0)
                iterator+=1
        freq_dict[word_form].append(samp_freq[word_form])
    for key in freq_dict.keys():
        if key not in words:
            freq_dict[key].append(0)
for i in range (1,21):
    freq(i)
for key in freq_dict.keys():
    freq_dict[key].insert(1, sum(freq_dict[key][1:]))
values1 = list(freq_dict.values())
values1_ordered = sorted(values1, key=lambda x: x[1], reverse=True)
print (values1_ordered)

morph = pymorphy2.MorphAnalyzer(lang='uk')
all_dict={}
for key in freq_dict.keys():
    all_dict[key]=[key]
    all_dict[key].insert(1, morph.parse(key)[0].normal_form)
    all_dict[key].insert(2, morph.parse(key)[0].tag.POS)
    if all_dict[key][2] == None:
       all_dict[key][2]  = 'NOTDEF'
values2 = list(all_dict.values())
print (values2)

for i in values1_ordered:
   c.execute("""INSERT OR IGNORE INTO wordforms_freq
                      VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", i)
conn.commit()

for i in values2:
   c.execute("""INSERT OR IGNORE INTO wordforms_all
                      VALUES ( ?, ?, ?)""", i)
conn.commit()

doc_sents=tokenize_uk.tokenize_uk.tokenize_sents(text_1)
def tfidf():
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(doc_sents)
    print(tfidf_matrix)
    features_names = tfidf_vectorizer.get_feature_names()
    tfidf_scores = tfidf_matrix.toarray()[1]
    sorted_keywords = [(word, score) for score,word in sorted(zip(tfidf_scores, features_names), reverse=True)]
    for tpl in sorted_keywords[:5]:
        print(tpl)

tfidf()

conn.close()

