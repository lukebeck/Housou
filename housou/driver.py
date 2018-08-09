import csv
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Driver:
    '''Chrome driver object for web scraping'''
    def __init__(self,path):
        '''Set driver path and options and initialise driver'''
        print('Initialising driver')
        self.path = path
        self.options = self.setOptions()
        self.driver = webdriver.Chrome(
            chrome_options=self.options,
            executable_path=self.path)
        print('driver initialised')

    def setOptions(self):
        '''Return options for headless chrome driver'''
        print('Setting options')
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        return options

    def getTree(self,url):
        '''Return HTML tree from given url'''
        self.driver.get(url)
        print('Extracting tree from url')
        innerHTML = self.driver.execute_script('return document.body.innerHTML')
        return html.fromstring(innerHTML)

    def getElements(self,tree,_xpath):
        '''Get a list of elements from specified xpath'''
        print('Extracting elements from tree')
        value = tree.xpath(_xpath)
        return value

    def getContent(self,tree,xpaths):
        '''Extract content from specified xpaths'''
        print('Extracting contents from tree')
        entry = []
        for key in xpaths:
            value = self.concatenate(tree.xpath(xpaths[key]))
            value = value.replace('\n', '\\n')
            entry.append(value)
        return entry

    def tearDown(self):
        '''Tear down driver'''
        print('Tearing down driver')
        self.driver.close()
        self.driver.quit()

    @staticmethod
    def concatenate(x):
        return '\t'.join([y.text_content() for y in x])

    @staticmethod
    def write(entry,csv_path):
        with open(csv_path,'a') as file:
            wr = csv.writer(file)
            wr.writerow(entry)