from flask import Flask
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime  
from datetime import timedelta
from actions import book_slot
import pandas as pd
import time 
import logging
import re
import os


app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)



@app.route('/navigate')
def navigate():

	df = pd.read_csv('time_table.csv')
	
	
	datetime_object = datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d'), '%Y-%m-%d')  + timedelta(hours=68) 
	datetime_object = datetime_object.replace(tzinfo=None)
	calender_id = str(int(datetime_object.timestamp()*1000))

	# target_time = ['11:00am','12:00pm','1:00pm','2:00pm']
	
	

	target_time = df[datetime_object.strftime("%A")].tolist()

	app.logger.warning(datetime_object.strftime("%Y-%m-%d %A"))
	app.logger.warning(str(datetime_object.timestamp()))


	#url Silverman
	url = "https://booking.lib.buffalo.edu/spaces?lid=3154"


	# create a new Firefox session
	driver = webdriver.Chrome("/usr/local/bin/chromedriver")

	# driver = webdriver.Chrome()
	driver.implicitly_wait(30)


	next_slot = book_slot(driver=driver, url=url, target_time=target_time, calender_id = calender_id)

	if next_slot == None:
		#url lockwod
		url = "https://booking.lib.buffalo.edu/spaces?lid=3087"
		next_slot = book_slot(driver=driver, url=url, target_time=target_time, calender_id = calender_id)

	if next_slot!=None:

		next_slot = book_slot(driver=driver, url=url, target_time=target_time, calender_id=calender_id, next_slot= next_slot)


	if next_slot == None:
		return '<h1>No availbale slot</h1>'


	driver.close()


	return '<h1>Booked!</h1>'



	

	# #Selenium hands the page source to Beautiful Soup
	# soup_level1=BeautifulSoup(driver.page_source, 'lxml')

	# datalist = [] #empty list
	# x = 0 #counter

	# #Beautiful Soup finds all Job Title links on the agency page and the loop begins
	# for link in soup_level1.find_all('a', id=re.compile("^MainContent_uxLevel2_JobTitles_uxJobTitleBtn_")):
	    
	#     #Selenium visits each Job Title page
	#     python_button = driver.find_element_by_id('MainContent_uxLevel2_JobTitles_uxJobTitleBtn_' + str(x))
	#     python_button.click() #click link
	    
	#     #Selenium hands of the source of the specific job page to Beautiful Soup
	#     soup_level2=BeautifulSoup(driver.page_source, 'lxml')

	#     #Beautiful Soup grabs the HTML table on the page
	#     table = soup_level2.find_all('table')[0]
	    
	#     #Giving the HTML table to pandas to put in a dataframe object
	#     df = pd.read_html(str(table),header=0)
	    
	#     #Store the dataframe in a list
	#     datalist.append(df[0])
	    
	#     #Ask Selenium to click the back button
	#     driver.execute_script("window.history.go(-1)") 
	    
	#     #increment the counter variable before starting the loop over
	#     x += 1
	    
	#     #end loop block
	    
	# #loop has completed

	# #end the Selenium browser session
	# driver.quit()

	# #combine all pandas dataframes in the list into one big dataframe
	# result = pd.concat([pd.DataFrame(datalist[i]) for i in range(len(datalist))],ignore_index=True)

	# #convert the pandas dataframe to JSON
	# json_records = result.to_json(orient='records')

	# #pretty print to CLI with tabulate
	# #converts to an ascii table
	# print(tabulate(result, headers=["Employee Name","Job Title","Overtime Pay","Total Gross Pay"],tablefmt='psql'))

	# #get current working directory
	# path = os.getcwd()

	# #open, write, and close the file
	# f = open(path + "\\fhsu_payroll_data.json","w") #FHSU
	# f.write(json_records)
	# f.close()





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

