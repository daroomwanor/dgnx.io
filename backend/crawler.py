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
			chrome_options.add_argument("start-maximized")
			chrome_options.add_argument('--no-sandbox')
			chrome_options.add_argument("disable-infobars")
			chrome_options.add_argument("--disable-dev-shm-usage")
			browser = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
			q = urllib.parse.quote_plus(placeType+" "+city)
			search = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q='+q
			browser.get(search)
			ele = browser.find_elements(by=By.CLASS_NAME, value="rllt__details")
			places = []
			imgs = browser.find_elements(by=By.CLASS_NAME, value="tLipRb")
			for k in range(len(ele)):
				thumbnails = imgs[k].get_attribute('src')
				place = self.dictListData(ele[k].text)
				if "Name" in place.keys():
					self.uploadToDB(placeType,city,place,thumbnails)
		except (RuntimeError, TypeError, NameError, pysqlite3.OperationalError,KeyError,IndexError) as e:
			pass
		finally:
			display.stop()
			os.popen("sudo pkill Chrome")

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
			pass

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
	global_cities = ['Jakarta', 'Sao Paulo', 'Mexico City', 'Cairo', 'Lagos', 'Rio de Janeiro', 'Paris', 'London', 'Bogota', 'Madrid', 'Giza', 'Nairobi', 'Toronto', 'Guadalajara', 'Belo Horizonte', 'Surabaya', 'Alexandria', 'Barcelona', 'Johannesburg', 'Monterrey', 'Montreal', 'Brasilia', 'Birmingham', 'Salvador', 'Rome', 'Kano', 'Manchester', 'Ibadan', 'Medellin', 'Cali', 'Fortaleza', 'Bandung', 'Bekasi', 'Tijuana', 'Accra', 'Vancouver', 'Tangerang', 'Medan', 'Kumasi', 'Leeds', 'Curitiba', 'Meru', 'Manaus', 'Ecatepec', 'Makassar', 'Newcastle', 'Depok', 'Semarang', 'Puebla', 'Recife', 'Madinat as Sadis min Uktubar', 'Belem', 'Porto Alegre', 'Onitsha', 'Palembang', 'Leon de los Aldama', 'Birstall', 'Owerri', 'Goiania', 'Milan', 'Guarulhos', 'Juarez', 'Barranquilla', 'Calgary', 'Abuja', 'Vila Velha', 'Mombasa', 'Maiduguri', 'Benin City', 'Cilacap', 'Bandar Lampung', 'Campinas', 'Zapopan', 'Ciudad Nezahualcoyotl', 'Nezahualcoyotl', 'Sevilla', 'Mexicali', 'Ikare', 'Sao Goncalo', 'Vereeniging', 'Sao Luis', 'Edmonton', 'Bogor', 'Cartagena', 'Ogbomoso', 'Maceio', 'Patam', 'Shubra al Khaymah', 'Nice', 'Port Harcourt']
	global_cities_2 = ['Delhi', 'Mumbai', 'Manila', 'Shanghai', 'Seoul', 'Guangzhou', 'Beijing', 'Kolkata', 'Shenzhen', 'Istanbul', 'Bangalore', 'Ho Chi Minh City', 'Nanyang', 'Baoding', 'Chennai', 'Chengdu', 'Linyi', 'Tianjin', 'Shijiazhuang', 'Zhoukou', 'Lima', 'Hyderabad', 'Handan', 'Weifang', 'Wuhan', 'Heze', 'Ganzhou', 'Tongshan', 'Changsha', 'Fuyang', 'Jining', 'Dongguan', 'Jinan', 'Foshan', 'Hanoi', 'Pune', 'Chongqing', 'Changchun', 'Zhumadian', 'Ningbo', 'Cangzhou', 'Nanjing', 'Hefei', 'Ahmedabad', 'Zhanjiang', 'Shaoyang', 'Hengyang', 'Nantong', 'Yancheng', 'Nanning', "Xi'an", 'Shenyang', 'Tangshan', 'Zhengzhou', 'Shangqiu', 'Yantai', 'Xinyang', 'Shangrao', 'Luoyang', 'Bijie', 'Quanzhou', 'Hangzhou', 'Huanggang', 'Maoming', 'Kunming', 'Nanchong', 'Zunyi', 'Jieyang', "Lu'an", 'Yichun', 'Changde', 'Taizhou', 'Liaocheng', 'Qujing', 'Surat', 'Qingdao', 'Singapore', 'Dazhou', 'Suzhou', 'Xiangyang', 'Nangandao', 'Ankara', "Tai'an", 'Yulin', 'Dezhou', 'Yongzhou', 'Suihua', 'Qiqihar', 'Jinhua', 'Shantou', 'Sydney', 'Weinan', 'Suqian', 'Suzhou', 'Fuzhou', 'Zhaotong', 'Pudong', 'Zhangzhou', 'Bozhou', 'Melbourne', 'Nanchang', 'Xianyang', 'Taizhou', 'Huaihua', "Ji'an", 'Mianyang', 'Xiaoganzhan', 'Shaoxing', 'Yuncheng', 'Pingdingshan', 'Huizhou', "Huai'an", 'Xinpu', 'Chenzhou', 'Guilin', 'Jiujiang', 'Anqing', 'Huanglongsi', 'Jiangmen', 'Changzhou', 'Wuxi', 'Zibo', 'Jiaxing', 'Dalian', 'Hengshui', 'Harbin', 'Yangzhou', 'Yibin', 'Yiyang', 'Meizhou', 'Chifeng', 'Guiyang', 'Langfang', 'Zhangjiakou', 'Izmir', 'Linfen', 'Wenzhou', 'Luzhou', 'Jiangguanchi', 'Neijiang', 'Yanjiang', 'Zhaoqing', 'Xiaoxita', 'Guigang', 'Xiamen', 'Chuzhou', 'Fuzhou', 'Zhuzhou', 'Loudi', 'Deyang', 'Qingyuan', 'Wuhu', 'Hechi', 'Binzhou', 'Liuzhou', 'Baojishi', "Guang'an", 'Hanzhong', 'Zaozhuang', 'Anshan', 'Lanzhou', 'Chengde', 'Puyang', 'Suining', 'Jiaozuo', 'Bengbu', 'Baicheng', 'Busan', 'Qincheng', 'Taiyuan', 'Shiyan', 'Lucknow', 'Chaoyang', 'Hechi', 'Leshan', 'Yulinshi', 'Siping', 'Zhongshan', 'Changzhi', 'Qinhuangdao', 'Bazhou', 'Zhenjiang', 'Urumqi', 'Tongliao', 'Heyuan', 'Tongren', 'Qinzhou', 'Jaipur', 'Xinzhou', 'Meishan', 'Jinzhou', 'Tieling', 'Shaoguan', 'Shanwei', 'Quezon City', 'Dingxi', 'Incheon', 'Bursa', 'Ningde', 'Daqing', 'Putian', 'Huzhou', 'Wuzhou', 'Xiangtan', 'Taichung', 'Zigong', 'Mudanjiang', 'Huludao', 'Kaohsiung', 'Rizhao', 'Cawnpore', 'Baotou', 'Taipei', 'Nanping', 'Chaozhou', 'Longyan', 'Hohhot', 'Antananarivo', 'Longba', 'Weihai', 'Xuanzhou', 'Sanming', 'Yangjiang', 'Yunfu', 'Brisbane', 'Baoshan', 'Luohe', 'Qinbaling', 'Mirzapur', 'Guangyuan', 'Huangshi', 'Daegu', 'Jilin', 'Lianshan', 'Lincang', 'Antalya', 'Nagpur', 'Huainan', 'Dandong', 'Shangzhou', 'Ghaziabad', 'Jiamusi', 'Yuxi', 'Anshun', 'Konya', 'Yingkou', 'Adana', 'Sanmenxia', 'Indore', "Ma'anshan", 'Pingliang', 'Quzhou', 'Gaoping', 'Huaibei', 'Xining', "Yan'an", 'Jincheng', 'Puning', 'Lishui', 'Qingyang', 'Haiphong', 'Laibin', 'Vadodara', 'Perth', 'Vishakhapatnam', 'Gaziantep', 'Fushun', 'Pingxiang', 'Chongzuo', 'Sanliurfa', 'Hezhou', 'Jixi', 'Fuxin', 'Tainan', 'Zhuhai', 'Wuwei', 'Bhopal', 'Xiping', 'Mersin', 'Liaoyang', 'Baiyin', 'Shengli', 'Haikou', 'Shuyangzha', 'Heihe', 'Diyarbakir', 'Chinchvad', 'Shuozhou', 'Patna', 'Sanzhou', 'Kampala', 'Yushan', 'Ludhiana', 'Zhongli', 'Davao', 'Yinchuan', 'Caloocan City', 'Chengtangcun', 'Agra', 'Jingdezhen', 'Kalyan', 'Madurai', 'Benxi', 'Jamshedpur', 'Zhangjiajie', 'Beihai', 'Shuangyashan', 'Yucheng', 'Changshu', 'Lianjiang', 'Ximeicun', 'Jianguang', 'Xushan', 'Guiping', 'Leizhou', 'Gwangju', 'Nasik', 'Daejeon', 'Huangshan', 'Huazhou', 'Pizhou', 'Yangshe', 'Chizhou', 'Guyuan', "Rui'an", 'Hebi', 'Gaozhou', 'Faridabad', 'Kayseri', 'Yueqing', 'Pingdu', 'Aurangabad', 'Yutan', 'Wenling', 'Adelaide', 'Samsun', 'Rajkot', 'Liangshi', 'Fuqing', 'Xintai', 'Meerut', 'Yushu', 'Rongcheng', 'Huazhou', 'Yangquan', 'Haicheng', 'Yingtan', 'Huaiyin', 'Wuzhong', 'Jabalpur', 'Thane', 'Zhangye', 'Rucheng', 'Shaoyang', 'Dhanbad', 'Yichun', 'Laiwu', 'Jingling', 'Dayan', 'Suwon', 'Jiangyin', 'Yongcheng', 'Can Tho', 'Yiwu', 'Beidao', 'Shuangshui', 'Allahabad', 'Varanasi', 'Xinyu', 'Srinagar', 'Guankou', 'Ulsan', 'Dingzhou', 'Lianyuan', 'Rongcheng', 'Kaiyuan', 'Zhuji', 'Leiyang', 'Dadukou', 'Xiantao', 'Amritsar', 'Callao', 'Aligarh', 'Yingchuan', 'Bhiwandi', 'Zhoushan', 'Bien Hoa', 'Gwalior', 'Ankang', 'Hegang', 'Bhilai', 'Yuyao', 'Hanchuan', 'Gongzhuling', 'Haora', 'Yicheng', 'Ranchi', 'Taixing', 'Goyang', 'Bezwada', 'Mizhou', 'Xishan', 'Ezhou', 'Changwon', 'Zhongwei', 'Shouguang', 'Chandigarh', 'Tekirdag', 'Linhai', 'Wafangdian', 'Zhongxiang', 'Thu Duc', 'Mysore', 'Xinyi', 'Raipur', 'Arequipa', 'Zaoyang', 'Shuizhai', 'Kota']
	placeTypes = ['restaurants', 'bars', 'nightclub', 'attractions', 'hotels']
	for city in global_cities:
		print(city)
		for placeType in placeTypes:
			try:
				pf.googler(city, placeType)
			finally:
				time.sleep(10.0)
