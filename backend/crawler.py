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
from selenium.webdriver.chrome.service import Service


conn = pysqlite3.connect("/home/ubuntu/dgnx.io/frontend/db/vos.db")

logging.basicConfig(level=logging.INFO)

class placeFinder(object):

	def googler(self,city, placeType):
		display = Display(visible=0, size=(1200, 1200))
		display.start()
		try:
			path = '/usr/bin/chromedriver'
			s = Service(path)
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument('--no-sandbox')
			browser = webdriver.Chrome(path, options=chrome_options)
			q = urllib.parse.quote_plus(placeType+" "+city)
			search = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q='+q
			browser.get(search)
			ele = browser.find_elements(by=By.CLASS_NAME, value="rllt__details")
			places = []
			imgs = browser.find_elements(by=By.CLASS_NAME, value="tLipRb")
			for k in range(len(ele)):
				thumbnails = imgs[k].get_attribute('src')
				place = self.dictListData(ele[k].text)
				self.uploadToDB(placeType,city,place,thumbnails)
				places.append(place)
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
		except (RuntimeError, TypeError, NameError, pysqlite3.OperationalError,KeyError) as e:
			print(e)
		finally:
			pass

	def uploadToDB(self,placeType,city,place,thumbnails):
		try:
			if len(self.isPlaceFound(place['Name'],city)) == 0:
				guid = str(uuid.uuid4())
				query = "INSERT INTO placesTable(guid, city, placeType, placeName, ratings, reviews,thumbnails) VALUES(?,?,?,?,?,?,?)"
				cur = conn.cursor()
				cur.execute(query, (guid, city, placeType, place['Name'], place['Ratings'], place['Tag'], thumbnails))
				conn.commit()
				print(cur.lastrowid)
				return cur.lastrowid
			else:
				print("Logged")
		except (RuntimeError, TypeError, NameError, pysqlite3.OperationalError,KeyError) as e:
			print(e)
		finally:
			print(city)

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
	cities_ = ['New York', 'Los Angeles', 'Chicago', 'Miami', 'Dallas', 'Philadelphia', 'Houston', 'Atlanta', 'Washington', 'Boston', 'Phoenix', 'Seattle', 'San Francisco', 'Detroit', 'San Diego', 'Minneapolis', 'Tampa', 'Denver', 'Brooklyn', 'Queens', 'Riverside', 'Baltimore', 'Las Vegas', 'Portland', 'San Antonio', 'St. Louis', 'Sacramento', 'Orlando', 'San Jose', 'Cleveland', 'Pittsburgh', 'Austin', 'Cincinnati', 'Kansas City', 'Manhattan', 'Indianapolis', 'Columbus', 'Charlotte', 'Virginia Beach', 'Bronx', 'Milwaukee', 'Providence', 'Jacksonville', 'Salt Lake City', 'Nashville', 'Richmond', 'Memphis', 'Raleigh', 'New Orleans', 'Louisville']
	cities = ['Sacramento', 'Orlando', 'San Jose', 'Cleveland', 'Pittsburgh', 'Austin', 'Cincinnati', 'Kansas City', 'Manhattan', 'Indianapolis', 'Columbus', 'Charlotte', 'Virginia Beach', 'Bronx', 'Milwaukee', 'Providence', 'Jacksonville', 'Salt Lake City', 'Nashville', 'Richmond', 'Memphis', 'Raleigh', 'New Orleans', 'Louisville']
	placeTypes = ['restaurants', 'bars', 'nightclub', 'attractions', 'hotels']
	for city in cities:
		for placeType in placeTypes:
			try:
				pf.googler(city, placeType)
			finally:
				pass
