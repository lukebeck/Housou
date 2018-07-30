# Housou

Housou is a script the scrapes the NHK news home page and analyses word frequency of a selection of main articles.

The current frequency list can be found in `words.csv`. At the moment it is organised by frequency, rather than by morphemes.

As this is a new project, current frequency ratings are unrepresentative, as can be seen by the prominience of words like 台風12号. Parsing more articles will not solve this issue, only doing so over a longer period of time.

Ideally this script would be left running, checking the site periodically and adding any new article. At the moment I am periodically running it manually.

## 🔊 Requires

- lxml
- selenium
- MeCab with mecab-ipadic-neologd

For selenium to work, [chromedriver](http://chromedriver.chromium.org/downloads) needs to be downloaded and added to root folder.

## 🔊 Other

In writing this script, I found these articles helpful:
- [Running headless chrome with selenium in python](https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d)
- [Japanese text analysis in python](http://www.robfahey.co.uk/blog/japanese-text-analysis-in-python/)

## 🔊 Todo

Automatically output statistics:
- how many articles
- between what dates
- how many words