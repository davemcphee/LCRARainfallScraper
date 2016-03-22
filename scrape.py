"""
LCRA website rainfall scraper for AURA
"""

import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


outfile = open('LadyBirdLakeLevelWithZeroeValues.csv', 'w')


dateList = []			# fill with datetime objects each spanning 180 days, as per LCRA's max interval
						# dateList[i] = [start date, end date]
yearsOfData = 10
daysOfData = yearsOfData * 365
end = datetime.date.today()
finishDate = datetime.date.today() - datetime.timedelta(days = daysOfData)

lcraUrl = 'http://hydromet.lcra.org/chronhist.aspx'		# Date1 is start date, Date2 is end data. date format is mm/dd/YYYY
driver = webdriver.Firefox()
driver.get(lcraUrl)
gauge = Select(driver.find_element_by_id("DropDownList1"))
gauge.select_by_value("4543")
sensor = Select(driver.find_element_by_id("DropDownList2"))
sensor.select_by_value("STAGE")
submit = driver.find_element_by_name("Button1")
submit.click()

while True:
	start = end - datetime.timedelta(days = 180)
	if start < finishDate:
		break
	dateList.append([start.strftime("%m/%d/%Y"), end.strftime("%m/%d/%Y")])
	end = start - datetime.timedelta(days = 1)


def makeSoup(source):
	soup = BeautifulSoup(source, "html5lib")
	table = soup.find('table')
	rows = table.find_all('tr')
	for row in rows:
		tds = row.findChildren('td')
		if len(tds) == 3:
			string = tds[0].get_text() + ', ' + tds[1].get_text() + '\n'
			outfile.write(string)

			
for i in dateList:
	start = i[0]
	end = i[1]
	print("Searching between %s and %s" % (start, end))
	date1 = driver.find_element_by_id("Date1")
	date2 = driver.find_element_by_id("Date2")
	submit = driver.find_element_by_name("Button1")
	date1.clear()
	date2.clear()
	date1.send_keys(start)
	date2.send_keys(end)
	submit.click()
	makeSoup(driver.page_source)

outfile.close()
driver.quit()



	
	
	




