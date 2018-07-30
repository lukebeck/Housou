import csv
import MeCab
from collections import OrderedDict

entries = []
articles = 0
with open('articles.csv', 'r') as myfile:
    reader = csv.reader(myfile, delimiter=',')
    for row in reader:
        entries.append(row[2])
        articles +=1

occurances = {}
morphemes = 0
tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
for entry in entries:
    parsed = tagger.parseToNode(entry)
    while parsed:
        morphemes += 1
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

with open('words.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    for row in output:
        wr.writerow(row)

print(f'''
Articles analysed:      {articles} 
Morphemes identified:   {morphemes}
Unique morphemes:       {len(output)}
''')

print('Top 10 morphemes\n----------------')

for x in output[:10]:
    print(x[1],': ',x[0])