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
from pyvirtualdisplay import Display
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
		display = Display(visible=0, size=(1200, 1200))
		display.start()
		try:
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument('--no-sandbox')
			browser = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
			q = urllib.parse.quote_plus(query)
			search = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q='+q
			browser.get(search)
			scrapedValues = htmlObject(browser)
			ele = browser.find_elements_by_class_name("rllt__details")
			places = []
			for k in ele:
				txt = k.text
				places.append(self.dictListData(txt))
			print(places)
			return places
		finally:
			display.stop()
			os.popen("pkill Chrome")
			logging.info('Scraped For '+f'{query}')

	def dictListData(self, str_input):
		res = {}
		try:
			split_input = str_input.split('\n')
			if len(split_input) > 4:
				res = {'Name': split_input[0], 
						'Ratings': split_input[1],
						'Tag': split_input[2],
						'Address':split_input[3],
						'Description': split_input[4],}
			else:
				res = {'Name': split_input[0], 
						'Ratings': split_input[1],
						'Tag': split_input[2],
						'Address':split_input[3],
						'Description': "None",}
		finally:
			return res


class htmlObject(PageObject):
	# :Page Object
    #li_tag = MultiPageElement(tag_name='li')
    #a_tag = MultiPageElement(tag_name='a')
    div_tag = MultiPageElement(tag_name='div')
    #td_tag = MultiPageElement(tag_name='td')
    #span_tag = MultiPageElement(tag_name='span')

if __name__ == '__main__':
	pf = placeFinder()
	for x in ["nightclubs","Bars"]:
		res = pf.googler("Las Vegas " + x)
		print(res)