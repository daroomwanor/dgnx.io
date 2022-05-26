import os
import pandas as pd
import numpy as np
import pandas as pd
import urllib.parse
import asyncio
import json
import uuid
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
from placeFinder import placeFinder

logging.basicConfig(level=logging.INFO)

class webSocketIO(object):

	SocketIO 	= set()
	userIO 		= set()

	async def init_ws(self, ws: WebSocketServerProtocol, url: str) -> None:
		guid = str(uuid.uuid4())
		await self.addNewUserConnection(ws,guid)
		try:
			await self.webService(ws,guid)
		finally:
			await self.removeUserConnection(ws,guid)
	
	async def webService(self, ws:WebSocketServerProtocol,guid:str) -> None:
		try:
			async for msg in ws:
				json_data = json.loads(msg)
				city = json_data['city']
				pf = placeFinder()
				for x in ['restaurants', 'bars','nightclubs','things to do', 'hotels']:
					try:
						res = pf.googler(city+" "+x)
						return_data = json.dumps(res)
						await ws.send(json.dumps({'data':res, 'tableView': x}))
					except (RuntimeError, TypeError, NameError, StaleElementReferenceException) as e:
						logging.info(f'{e}')
					finally:
						logging.info(f'Disconnected {ws}')
		finally: 
			logging.info('Closed Connection '+f'{ws}')

	async def addNewUserConnection(self, ws:WebSocketServerProtocol, guid:str) -> None:
		self.SocketIO.add(ws)
		self.userIO.add(guid)
		logging.info(f'{guid} connects. '+str(len(self.SocketIO)))

	async def removeUserConnection(self, ws:WebSocketServerProtocol,guid:str) -> None:
		self.SocketIO.remove(ws)
		self.userIO.remove(guid)
		logging.info(f'{guid} disconnects.')

	async def socketBroadcastEvent(self,userWebSocket):
		pass

def Configs():
	with open("/home/ubuntu/dgnx.io/backend/configs.json", "r") as configs:
		return configs.read()

def connDB():
	_configs = Configs()
	creds = json.loads(_configs)
	connection = pymysql.connect(host=creds['db_host'],user=creds['db_user'], password=creds['db_password'], database=creds['db_schema'], cursorclass=pymysql.cursors.DictCursor)
	return connection

conn = connDB()
configs = json.loads(Configs())
server = webSocketIO()
start_server = websockets.serve(server.init_ws, configs["master_url"], configs["master_port"])
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
