# Housou

Housou is a script the scrapes the NHK news home page and analysis word frequency of a selection of main articles.

Ideally this script would be left running, checking the site periodically and adding any new article. At the moment I am periodically running it manually.

## 🔊 Requires

- lxml
- selenium
- pandas
- MeCab

For selenium to work, [chromedriver](http://chromedriver.chromium.org/downloads) needs to be downloaded and added to root folder.

## 🔊 Todo

Add a yaml file that contains settings and statistics, like # of articles, # of words, anything else worth noting

## 🔊 Other

In writing this script, I found these articles helpful:
- [Running headless chrome with selenium in python](https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d)
- [Japanese text analysis in python](http://www.robfahey.co.uk/blog/japanese-text-analysis-in-python/)

