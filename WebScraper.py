from bs4 import BeautifulSoup as soup
import urllib
from urllib.request import urlopen as uReq
import sqlite3

def Scraper():
	try:
		my_url = "https://en.wikipedia.org/wiki/2018_Winter_Olympics_medal_table"

		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close
		print("Connected to url")
	except:
		print("Unable to connect to url")

	#Parsing
	page_soup = soup(page_html,"html.parser")

	My_table = page_soup.find("table",{"class": "wikitable sortable plainrowheaders"})
	#find rows with countries and corresponding data
	table = My_table.findAll("tr")
	values = []
	for row in table:
		tmp = []
		#find country
		country = row.find("th")
		tmp.append(country.get_text().replace(u'\xa0', u' ').rstrip())
		#find medal values
		vals = row.findAll("td")
		for val in vals:
			tmp.append(val.get_text().rstrip())
		#append countries and medal values
		values.append(tmp)

	#Add rank if Country is tied with others
	values = values[:-1]
	for i in range(len(values)):
		if len(values[i]) == 5:
			values[i].insert(1, values[i - 1][1])

	print("-----Data Collected-----")

	values = values[1:]
	return values

def Connect_DB():
	#Create table
	try:
		conn = sqlite3.connect("./OlympicMedals.db")
		print(sqlite3.version)
		print("Connected to database")
		return conn
	except:
		print("Unable to connect to database")

def Insert_Values():
	#Create Medals table if it has not been created already	
	sql_create_medals_table = """ CREATE TABLE IF NOT EXISTS OlympicMedals (
									Rank int ,
									NOC text,
									Gold int,
									Silver int,
									Bronze int,
									Total int,
									CONSTRAINT name_unique UNIQUE (NOC)
									)"""

	conn = Connect_DB()
	values = Scraper()
	c = conn.cursor()
	c.execute(sql_create_medals_table)
	
	'''Insert values into Medals Table, throw exception if country (NOC) is not unique to stop data redundancies
	   if script is run mutiple times'''
	#MySQL would us '%s' in place of '?''
	try:
		for value in values:
			c.execute("""INSERT INTO OlympicMedals(Rank, NOC, Gold, Silver, Bronze, Total) 
						 VALUES (?, ?, ?, ?, ?, ?)""",
						 (value[1], value[0], value[2], value[3], value[4], value[5]))
			conn.commit()
	except:
		print("Unable to insert scraped data, WebScraper.py may have already ran")

Insert_Values()