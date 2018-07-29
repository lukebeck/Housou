import csv
import MeCab
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

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

entries = []
with open('articles.csv', 'r') as myfile:
    reader = csv.reader(myfile, delimiter=',')
    for row in reader:
        entries.append(row[2])

text = "テスト"

frequency = []
tagger = MeCab.Tagger()
for entry in entries:
    parsed = tagger.parseToNode(entry)
frequency = count_words_in_node(parsed)



### FOR EVENTUAL PANDAS IMPLEMENTATION
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