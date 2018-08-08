import csv
from . import driver
import os

# file paths
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_path = dir_path + '/articles.csv'
driver_path = dir_path + '/chromedriver'

## main NHK page ##
# url
main_url = 'https://www3.nhk.or.jp/news/catnew.html?utm_int=news_contents_news-main_more'
# xpath
links_xpath = '//div[@class="content--items"]/ul/li/a/@href'

## Article pages ##
# urls extracted in main()
root_url = 'https://www3.nhk.or.jp/'
# xpaths
xpaths = {
    'title': '//h1[@class="content--title"]',
    'date': '//p[@class="content--date"]/time',
    'content': '//section[@class="content--detail-main"]'}

# Article titles in csv file
# For duplicate checking
titles = []
with open(csv_path,'r') as file:
    reader = csv.reader(file)
    for row in reader:
        titles.append(row[0])

def housou():
    # Initialise driver
    d = driver.Driver(driver_path)
    # Extract HTML tree from main NHK page
    tree = d.getTree(main_url)
    # Extract article links from main NHK page
    links = d.getElements(tree,links_xpath)
    # If unique, write article contents to csv
    for link in links:
        url = root_url + link
        tree = d.getTree(url)
        entry = d.getContent(tree,xpaths)
        if entry[0] in titles:
            print(entry[0])
            print('㊢ 複写の記事を飛びました')
            pass
        else:
            print(entry[0])
            d.write(entry,csv_path)
            print('㊣ データベースに記事を入力できました')
    # Tear down the driver upon completion
    d.tearDown()