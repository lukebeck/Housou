import csv
import MeCab
from collections import OrderedDict

# useful for testing
def display_dict(d):
    for x in d:
        print(f'{x}: {d[x]}')

def count_words_in_node(node):
    occurances = {}
    while node:
        lemma = node.feature.split(',')[6]
        if lemma == '*':
            pass
        elif lemma in occurances:
            occurances[lemma] += 1
        else:
            occurances[lemma] = 1
        node = node.next
    return occurances

occurances = {}
with open('words.csv','r') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        occurances[row[0]] = int(row[1])

entries = []
with open('articles.csv', 'r') as myfile:
    reader = csv.reader(myfile, delimiter=',')
    for row in reader:
        entries.append(row[2])

tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
for entry in entries:
    parsed = tagger.parseToNode(entry)
    while parsed:
        lemma = parsed.feature.split(',')[6]
        if lemma == '*':
            pass
        elif lemma in occurances:
            occurances[lemma] += 1
        else:
            occurances[lemma] = 1
        parsed = parsed.next

words = OrderedDict(sorted(occurances.items(),key=lambda t: t[0]))
count = OrderedDict(sorted(occurances.items(),key=lambda t: t[1],reverse=True))


# Just change to words for word ordered output
output = []
for i in count:
    row = [i,count[i]]
    output.append(row)

print('Most frequent words:')
for row in output[:20]:
    print(f'{row[1]} :: {row[0]}')

with open('words.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    for row in output:
        wr.writerow(row)
    

# data = {'word': [key for key in frequency],
#         'freq': [frequency[key] for key in frequency]}


### FOR EVENTUAL PANDAS IMPLEMENTATION
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# 
# data = {'word': [key for key in frequency],
#         'freq': [frequency[key] for key in frequency]}
# df = pd.DataFrame(data)
# df.index.name = 'index'
# df = df.sort_values('word')
# df.reset_index(drop=True, inplace=True)
# df.to_csv('freq.csv',header=True,index=False)
# dfb = df[df['word']=='いる'].index.values.astype(int)[0] # WORKS!
# df.loc[df.filename == 'test2.dat', 'n'] = df2[df2.filename == 'test2.dat'].loc[0]['n']
# print(dfb)
# df.word.unique() 