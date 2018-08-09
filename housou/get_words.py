from collections import OrderedDict
import csv
import MeCab
import os

# file paths
file_path = os.path.dirname(os.path.realpath(__file__))
csv_file = file_path + '/articles.csv'
readme_path = file_path + '/housou-data/README.md'
morpheme_csv_path = file_path + '/housou-data/morpheme.csv'
count_csv_path = file_path + '/housou-data/count.csv'

class ArticleStore:
    def __init__(self,csv_file,article_location):
        self.entries = []
        self.load(csv_file,article_location)

    def load(self,csv_file,article_location):
        with open(csv_file,'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.entries.append(row[article_location])

class Analyser:
    def __init__(self,entries,tagger):
        self.entries = entries
        self.articles = len(self.entries)
        self.occurances = {}
        self.morphemes = 0
        self.tagger = tagger

    def analyse(self):
        for entry in self.entries:
            parsed = self.tagger.parseToNode(entry)
            while parsed:
                lemma = parsed.feature.split(',')[6]
                if lemma == '*':
                    pass
                elif lemma in self.occurances:
                    self.occurances[lemma] += 1
                else:
                    self.occurances[lemma] = 1
                parsed = parsed.next
        self.morphemes = len(self.occurances)

    @staticmethod
    def order(ordered_dict):
        return [[x,ordered_dict[x]] for x in ordered_dict]

    def morpheme_list(self):
        morpheme_occurances = OrderedDict(sorted(self.occurances.items(),key=lambda t: t[0]))
        return self.order(morpheme_occurances)

    def count_list(self):
        count_occurances = OrderedDict(sorted(self.occurances.items(),key=lambda t: t[1],reverse=True))
        return self.order(count_occurances)

    def instances(self):
        count = 0
        for x in self.occurances:
            count += self.occurances[x]
        return count

class Readme:
    def __init__(self,file):
        self.file = file
        self.get_readme(self.file)
    
    def get_readme(self,file):
        with open(file,'r') as file:
            contents = file.read()
            original = contents.split('\n')
            self.readme = original[:-3]

    def set_stats(self,stat_list):
        for stat in stat_list:
            self.readme.append(stat)
    
    def write_readme(self):
        readme = '\n'.join(self.readme)
        with open(self.file, 'w') as file:
            file.write(readme)

def main():
    articles = ArticleStore(csv_file,2)
    tagger = MeCab.Tagger() # For neologd pass '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd' to Tagger()
    analyser = Analyser(articles.entries,tagger)
    analyser.analyse()

    stats = [
        f'- **Articles analysed:** {analyser.articles}',
        f'- **Morphemes identified:** {analyser.instances()}',
        f'- **Unique morphemes:** {analyser.morphemes}']

    readme = Readme(readme_path)
    readme.set_stats(stats)
    readme.write_readme()

    morphemes = analyser.morpheme_list()
    with open(morpheme_csv_path,'w') as file:
        wr = csv.writer(file)
        for row in morphemes:
            wr.writerow(row)

    count = analyser.count_list()
    with open(count_csv_path,'w') as file:
        wr = csv.writer(file)
        for row in count:
            wr.writerow(row)

    print(f'''⚙ Articles analysed: {analyser.articles} 
⚙ Morphemes identified: {analyser.instances()}
⚙ Unique morphemes: {analyser.morphemes}''')
