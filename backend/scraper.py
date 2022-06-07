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

	def googler(self,placeName,city):
		display = Display(visible=0, size=(1200, 1200))
		display.start()
		try:
			path = '/usr/bin/chromedriver'
			s = Service(path)
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument('--no-sandbox')
			browser = webdriver.Chrome(path, options=chrome_options)
			q = urllib.parse.quote_plus(placeName+" "+city)
			search = 'https://www.google.com/search?q='+q
			print(search)
			browser.get(search)
			ele = browser.find_elements(by=By.CLASS_NAME, value="UDZeY")
			website = browser.find_elements(by=By.CLASS_NAME, value="ab_button")
			res={}
			if len(ele) > 0:
				res = self.dictListData(ele[0].text)
				res['Website']= website[0].get_attribute('href')
			else:
				web_details = browser.find_elements(by=By.CLASS_NAME, value="rllt__details")
				res['Address'] = web_details[1].text
			return res
		except (RuntimeError, TypeError, NameError, pysqlite3.OperationalError,KeyError,IndexError) as e:
			print(e)
		finally:
			display.stop()
			os.popen("pkill Chrome")

	def uploadToDB(self,address,phone,website,description,hours,guid):
		try:
			query = "UPDATE placesTable SET address = ?, phone = ?, website= ?, description = ?, info = ? WHERE guid = ?"
			cur = conn.cursor()
			cur.execute(query, (address, phone, website, description, hours, guid))
			conn.commit()
			print(cur.lastrowid)
			return cur.lastrowid
			print("Logged")
		except (RuntimeError, TypeError, NameError, pysqlite3.OperationalError,KeyError) as e:
			print(e)
		finally:
			print(city)
	
	def checkLine(self, line):
		res = {}
		split_line = line.split(':')
		if split_line[0] == "Address":
			res['Address']= split_line[1]
		if split_line[0] == "Phone":
			res['Phone'] = split_line[1]
		split_str = line.split(" ")
		if split_str[0] in ["Closes", "Open"]:
			res['Hours'] = line
		return res

	def dictListData(self, str_input):
		res = {}
		try:
			split_input = str_input.split('\n')
			res['Info'] = split_input[0]
			for x in split_input:
				line = self.checkLine(x)
				if "Address" in line.keys():
					res['Address'] = line["Address"]
				if "Phone" in line.keys():
					res['Phone'] = line["Phone"]
				if "Hours" in line.keys():
					res['Hours'] = line["Hours"]
			return res
		finally:
			pass

def isPlaceFound(city):
	try:
		query = 'SELECT guid,placeName,city FROM placesTable WHERE city = "'+city+'"'
		cur = conn.cursor()
		cur.execute(query)
		return cur.fetchall()
	except (RuntimeError, TypeError, NameError,KeyError, NoneType) as e:
		print(e)
	finally:
		pass

if __name__ == '__main__':
	pf = placeFinder()
	cities = [ 'Kano', 'Manchester', 'Ibadan', 'Medellin', 'Cali', 'Fortaleza', 'Bandung', 
	'Bekasi', 'Tijuana', 'Accra', 'Vancouver', 'Tangerang', 'Medan', 'Kumasi', 'Leeds', 'Curitiba', 'Meru', 'Manaus', 'Ecatepec', 
	'Makassar', 'Newcastle', 'Depok', 'Semarang', 'Puebla', 'Recife', 'Madinat as Sadis min Uktubar', 'Belem', 'Porto Alegre', 'Onitsha', 
	'Palembang', 'Leon de los Aldama', 'Birstall', 'Owerri', 'Goiania', 'Milan', 'Guarulhos', 'Juarez', 'Barranquilla', 'Calgary', 'Abuja', 
	'Vila Velha', 'Mombasa', 'Maiduguri', 'Benin City', 'Cilacap', 'Bandar Lampung', 'Campinas', 'Zapopan', 'Ciudad Nezahualcoyotl', 'Nezahualcoyotl', 
	'Sevilla', 'Mexicali', 'Ikare', 'Sao Goncalo', 'Vereeniging', 'Sao Luis', 'Edmonton', 'Bogor', 'Cartagena', 'Ogbomoso', 'Maceio', 'Patam', 'Shubra al Khaymah', 
	'Nice', 'Port Harcourt']


	for city in cities:
		places = isPlaceFound(city)
		logging.info('Scraped For '+f'{city}')
		for place in places:
			try:
				data = pf.googler(place[1],place[2])
				print(data)
				logging.info('Got: '+f'{data}')
				if "Phone" not in data.keys():
					data['Phone'] = None
				if "Address" not in data.keys():
					data['Address'] = None
				if "Website" not in data.keys():
					data['Website'] = None
				if "Info" not in data.keys():
					data['Info'] = None
				if "Hours" not in data.keys():
					data['Hours'] = None
				
				pf.uploadToDB(data['Address'], data['Phone'], data['Website'], data['Info'], data['Hours'], place[0])
				time.sleep(1.0)
			except (RuntimeError, TypeError, NameError,KeyError, AttributeError) as e:
				print(e)
			finally:
				pass
