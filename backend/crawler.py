import os
import time
import pandas as pd
import numpy as np
import pandas as pd
import urllib.parse
import asyncio
import uuid
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
import pysqlite3


conn = pysqlite3.connect("/home/ubuntu/dgnx.io/frontend/db/vos.db")

logging.basicConfig(level=logging.INFO)

class placeFinder(object):

	def googler(self,city, placeType):
		display = Display(visible=0, size=(1200, 1200))
		display.start()
		try:
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument('--no-sandbox')
			browser = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
			q = urllib.parse.quote_plus(placeType+" "+city)
			search = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q='+q
			browser.get(search)
			ele = browser.find_elements_by_class_name("b9tNq")
			places = []
			for k in ele:
				img = k.find_elements_by_class_name("tLipRb")
				print(img)
				txt = self.dictListData(k.text)
				#self.uploadToDB(placeType,city,txt)
				print(places.append(txt))
			return places
		finally:
			display.stop()
			os.popen("pkill Chrome")
	
	def isPlaceFound(self, placeName, city):
		try:
			query = "SELECT Id FROM placesTable WHERE placeName = ? AND city = ?"
			cur = conn.cursor()
			cur.execute(query,(placeName,city))
			return cur.fetchall()
		except (RuntimeError, TypeError, NameError, pysqlite3.OperationalError) as e:
			print(e)

	def uploadToDB(self,placeType,city,place):
		try:
			guid = str(uuid.uuid4())
			query = "INSERT INTO placesTable(guid, city, placeType, placeName, ratings, reviews) VALUES(?,?,?,?,?,?)"
			cur = conn.cursor()
			cur.execute(query, (guid, city, placeType, place['Name'], place['Ratings'], place['Tag']))
			conn.commit()
			print(cur.lastrowid)
			return cur.lastrowid
		except (RuntimeError, TypeError, NameError, pysqlite3.OperationalError) as e:
			print(e)

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

if __name__ == '__main__':
	pf = placeFinder()
	pf.googler("Las Vegas", "restaurants")
