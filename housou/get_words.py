import csv
import MeCab
from collections import OrderedDict

import os

file_path = os.path.dirname(os.path.realpath(__file__))
csv_file = file_path + '/articles.csv'

def analyse():
    entries = []
    articles = 0
    with open(csv_file, 'r') as myfile:
        reader = csv.reader(myfile, delimiter=',')
        for row in reader:
            entries.append(row[2])
            articles +=1

    occurances = {}
    morphemes = 0
    # For neologd pass '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd' to Tagger()
    tagger = MeCab.Tagger()
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

    morpheme = OrderedDict(sorted(occurances.items(),key=lambda t: t[0]))
    count = OrderedDict(sorted(occurances.items(),key=lambda t: t[1],reverse=True))

    # Just change to words for word ordered output
    output_count = []
    for i in count:
        row = [i,count[i]]
        output_count.append(row)

    output_morpheme = []
    for i in morpheme:
        row = [i,morpheme[i]]
        output_morpheme.append(row)

    def table(output):
        header = 'Morpheme | Count\n'
        divider = '--- | ---:\n'
        table = ''
        for x in output:
            table = table + f'{x[0]} | {x[1]}\n'
        return header + divider + table


    with open(file_path + '/housou-data/README.md','r') as file:
        contents = file.read()
        original_readme = contents.split('\n')
        readme = original_readme[:-4]
    
    articles_analyse = f'- **Articles analysed:** {articles}'
    morphemes_identified = f'- **Morphemes identified:** {morphemes}'
    unique_morphemes = f'- **Unique morphemes:** {len(output_morpheme)}'
 
    readme.append(articles_analyse)
    readme.append(morphemes_identified)
    readme.append(unique_morphemes)

    readme = '\n'.join(readme)

    with open(file_path + '/housou-data/README.md', 'w') as myfile:
        myfile.write(readme)

    with open(file_path + '/housou-data/count.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        for row in output_count:
            wr.writerow(row)

    with open(file_path + '/housou-data/morpheme.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        for row in output_morpheme:
            wr.writerow(row)

    print(f'''△ Articles analysed: {articles} 
△ Morphemes identified: {morphemes}
△ Unique morphemes: {len(output_morpheme)}
△ Most frequency morphemes:''')

    for x, y in output_count[:7]:
        print(y,x)