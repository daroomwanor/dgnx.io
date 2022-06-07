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
	cities = ['Delhi', 'Mumbai', 'Manila', 'Shanghai', 'Seoul', 'Guangzhou', 'Beijing', 'Kolkata', 'Shenzhen', 'Istanbul', 'Bangalore', 'Ho Chi Minh City', 'Nanyang', 'Baoding', 'Chennai', 'Chengdu', 'Linyi', 'Tianjin', 'Shijiazhuang', 'Zhoukou', 'Lima', 'Hyderabad', 'Handan', 'Weifang', 'Wuhan', 'Heze', 'Ganzhou', 'Tongshan', 'Changsha', 'Fuyang', 'Jining', 'Dongguan', 'Jinan', 'Foshan', 'Hanoi', 'Pune', 'Chongqing', 'Changchun', 'Zhumadian', 'Ningbo', 'Cangzhou', 'Nanjing', 'Hefei', 'Ahmedabad', 'Zhanjiang', 'Shaoyang', 'Hengyang', 'Nantong', 'Yancheng', 'Nanning', "Xi'an", 'Shenyang', 'Tangshan', 'Zhengzhou', 'Shangqiu', 'Yantai', 'Xinyang', 'Shangrao', 'Luoyang', 'Bijie', 'Quanzhou', 'Hangzhou', 'Huanggang', 'Maoming', 'Kunming', 'Nanchong', 'Zunyi', 'Jieyang', "Lu'an", 'Yichun', 'Changde', 'Taizhou', 'Liaocheng', 'Qujing', 'Surat', 'Qingdao', 'Singapore', 'Dazhou', 'Suzhou', 'Xiangyang', 'Nangandao', 'Ankara', "Tai'an", 'Yulin', 'Dezhou', 'Yongzhou', 'Suihua', 'Qiqihar', 'Jinhua', 'Shantou', 'Sydney', 'Weinan', 'Suqian', 'Suzhou', 'Fuzhou', 'Zhaotong', 'Pudong', 'Zhangzhou', 'Bozhou', 'Melbourne', 'Nanchang', 'Xianyang', 'Taizhou', 'Huaihua', "Ji'an", 'Mianyang', 'Xiaoganzhan', 'Shaoxing', 'Yuncheng', 'Pingdingshan', 'Huizhou', "Huai'an", 'Xinpu', 'Chenzhou', 'Guilin', 'Jiujiang', 'Anqing', 'Huanglongsi', 'Jiangmen', 'Changzhou', 'Wuxi', 'Zibo', 'Jiaxing', 'Dalian', 'Hengshui', 'Harbin', 'Yangzhou', 'Yibin', 'Yiyang', 'Meizhou', 'Chifeng', 'Guiyang', 'Langfang', 'Zhangjiakou', 'Izmir', 'Linfen', 'Wenzhou', 'Luzhou', 'Jiangguanchi', 'Neijiang', 'Yanjiang', 'Zhaoqing', 'Xiaoxita', 'Guigang', 'Xiamen', 'Chuzhou', 'Fuzhou', 'Zhuzhou', 'Loudi', 'Deyang', 'Qingyuan', 'Wuhu', 'Hechi', 'Binzhou', 'Liuzhou', 'Baojishi', "Guang'an", 'Hanzhong', 'Zaozhuang', 'Anshan', 'Lanzhou', 'Chengde', 'Puyang', 'Suining', 'Jiaozuo', 'Bengbu', 'Baicheng', 'Busan', 'Qincheng', 'Taiyuan', 'Shiyan', 'Lucknow', 'Chaoyang', 'Hechi', 'Leshan', 'Yulinshi', 'Siping', 'Zhongshan', 'Changzhi', 'Qinhuangdao', 'Bazhou', 'Zhenjiang', 'Urumqi', 'Tongliao', 'Heyuan', 'Tongren', 'Qinzhou', 'Jaipur', 'Xinzhou', 'Meishan', 'Jinzhou', 'Tieling', 'Shaoguan', 'Shanwei', 'Quezon City', 'Dingxi', 'Incheon', 'Bursa', 'Ningde', 'Daqing', 'Putian', 'Huzhou', 'Wuzhou', 'Xiangtan', 'Taichung', 'Zigong', 'Mudanjiang', 'Huludao', 'Kaohsiung', 'Rizhao', 'Cawnpore', 'Baotou', 'Taipei', 'Nanping', 'Chaozhou', 'Longyan', 'Hohhot', 'Antananarivo', 'Longba', 'Weihai', 'Xuanzhou', 'Sanming', 'Yangjiang', 'Yunfu', 'Brisbane', 'Baoshan', 'Luohe', 'Qinbaling', 'Mirzapur', 'Guangyuan', 'Huangshi', 'Daegu', 'Jilin', 'Lianshan', 'Lincang', 'Antalya', 'Nagpur', 'Huainan', 'Dandong', 'Shangzhou', 'Ghaziabad', 'Jiamusi', 'Yuxi', 'Anshun', 'Konya', 'Yingkou', 'Adana', 'Sanmenxia', 'Indore', "Ma'anshan", 'Pingliang', 'Quzhou', 'Gaoping', 'Huaibei', 'Xining', "Yan'an", 'Jincheng', 'Puning', 'Lishui', 'Qingyang', 'Haiphong', 'Laibin', 'Vadodara', 'Perth', 'Vishakhapatnam', 'Gaziantep', 'Fushun', 'Pingxiang', 'Chongzuo', 'Sanliurfa', 'Hezhou', 'Jixi', 'Fuxin', 'Tainan', 'Zhuhai', 'Wuwei', 'Bhopal', 'Xiping', 'Mersin', 'Liaoyang', 'Baiyin', 'Shengli', 'Haikou', 'Shuyangzha', 'Heihe', 'Diyarbakir', 'Chinchvad', 'Shuozhou', 'Patna', 'Sanzhou', 'Kampala', 'Yushan', 'Ludhiana', 'Zhongli', 'Davao', 'Yinchuan', 'Caloocan City', 'Chengtangcun', 'Agra', 'Jingdezhen', 'Kalyan', 'Madurai', 'Benxi', 'Jamshedpur', 'Zhangjiajie', 'Beihai', 'Shuangyashan', 'Yucheng', 'Changshu', 'Lianjiang', 'Ximeicun', 'Jianguang', 'Xushan', 'Guiping', 'Leizhou', 'Gwangju', 'Nasik', 'Daejeon', 'Huangshan', 'Huazhou', 'Pizhou', 'Yangshe', 'Chizhou', 'Guyuan', "Rui'an", 'Hebi', 'Gaozhou', 'Faridabad', 'Kayseri', 'Yueqing', 'Pingdu', 'Aurangabad', 'Yutan', 'Wenling', 'Adelaide', 'Samsun', 'Rajkot', 'Liangshi', 'Fuqing', 'Xintai', 'Meerut', 'Yushu', 'Rongcheng', 'Huazhou', 'Yangquan', 'Haicheng', 'Yingtan', 'Huaiyin', 'Wuzhong', 'Jabalpur', 'Thane', 'Zhangye', 'Rucheng', 'Shaoyang', 'Dhanbad', 'Yichun', 'Laiwu', 'Jingling', 'Dayan', 'Suwon', 'Jiangyin', 'Yongcheng', 'Can Tho', 'Yiwu', 'Beidao', 'Shuangshui', 'Allahabad', 'Varanasi', 'Xinyu', 'Srinagar', 'Guankou', 'Ulsan', 'Dingzhou', 'Lianyuan', 'Rongcheng', 'Kaiyuan', 'Zhuji', 'Leiyang', 'Dadukou', 'Xiantao', 'Amritsar', 'Callao', 'Aligarh', 'Yingchuan', 'Bhiwandi', 'Zhoushan', 'Bien Hoa', 'Gwalior', 'Ankang', 'Hegang', 'Bhilai', 'Yuyao', 'Hanchuan', 'Gongzhuling', 'Haora', 'Yicheng', 'Ranchi', 'Taixing', 'Goyang', 'Bezwada', 'Mizhou', 'Xishan', 'Ezhou', 'Changwon', 'Zhongwei', 'Shouguang', 'Chandigarh', 'Tekirdag', 'Linhai', 'Wafangdian', 'Zhongxiang', 'Thu Duc', 'Mysore', 'Xinyi', 'Raipur', 'Arequipa', 'Zaoyang', 'Shuizhai', 'Kota']



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
