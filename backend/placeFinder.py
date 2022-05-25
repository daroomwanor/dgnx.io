import os
import time
import pandas as pd
import numpy as np
import pandas as pd
import urllib.parse
import asyncio
import json
import logging
import websockets
from websockets import WebSocketServerProtocol
import math
import pymysql.cursors
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from page_objects import PageObject, MultiPageElement, PageElement

logging.basicConfig(level=logging.INFO)

class placeFinder(object):

	def googler(self, query):
		try:
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument('--no-sandbox')
			browser = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
			q = urllib.parse.quote_plus(query)
			search = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q='+q
			browser.get(search)
			scrapedValues = htmlObject(browser)
			pdata = []
			for x in scrapedValues.div_tag:
				pdata.append(x.text)
			pdF = pd.DataFrame(pdata, columns=['div_data'])
			no_dup = pdF.drop_duplicates(subset=['div_data'])
			scrapedData = []
			for x in no_dup['div_data'].values:
				splitLine = x.split('\n')
				if len(splitLine) > 4 and len(splitLine) < 9:
					scrapedData.append(self.dictListData(x))
			browser.quit()
			return scrapedData
		finally:
			logging.info('Scraped For '+f'{query}')

	def dictListData(self, str_input):
		split_input = str_input.split('\n')
		return {'Name': split_input[0], 
				'Ratings': split_input[1],
				'Tag': split_input[2],
				'Address':split_input[3],
				'Description': split_input[4],}

class htmlObject(PageObject):
	# :Page Object
    #li_tag = MultiPageElement(tag_name='li')
    #a_tag = MultiPageElement(tag_name='a')
    div_tag = MultiPageElement(tag_name='div')
    #td_tag = MultiPageElement(tag_name='td')
    #span_tag = MultiPageElement(tag_name='span')

if __name__ == '__main__':
	for x in ["nightclubs","gentlemen clubs"]:
		res = placeFinder("Las Vegas " + x)
		print(res)