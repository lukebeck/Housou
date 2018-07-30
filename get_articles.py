import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import lxml
import requests
from lxml import html

# Chromedriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--disable-extensions')
chrome_driver = os.getcwd() + '/chromedriver'

#Urls
url = 'https://www3.nhk.or.jp/news/'
root_url = 'https://www3.nhk.or.jp/'

# Xpaths
link_path = '//article[@class="module module--news-main index-main"]//dt/a/@href'
content_path = '//section[@class="content--detail-main"]'
title_path = '//h1[@class="content--title"]/text()'
date_path = '//p[@class="content--date"]/time/text()'

# Get page links from NHK news homepage inner HTML
print('🔐 Extracing links...')
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver.get(url)
innerHTML = driver.execute_script("return document.body.innerHTML")
tree = html.fromstring(innerHTML)
links = tree.xpath(link_path)
print('🔓 Extracted!')

titles = []
with open('articles.csv','r') as file:
    reader = csv.reader(file)
    for row in reader:
        titles.append(row[0])

# scape linked article pages
for link in links:
    driver.get(root_url + link)
    innerHTML = driver.execute_script('return document.body.innerHTML')
    tree = html.fromstring(innerHTML)
    # Get content
    title = tree.xpath(title_path)[0]
    if title in titles:
        print(f'㊢ 複写の記事 :: {title}')
        print('     記事を飛びました')
        pass
    else:
        content = tree.xpath(content_path)[0].text_content()
        date = tree.xpath(date_path)[0]
        # echo content to command line
        print(f'リンク :: {link}')
        print(f'     題名 :: {title}')
        print(f'     日付 :: {date}')
        print(f'     内容 :: {content[0:20]}...')
        # Add to entries csv
        entry = [
            title,
            date,
            content]
        with open('articles.csv','a') as file:
            wr = csv.writer(file)
            wr.writerow(entry)

driver.quit()