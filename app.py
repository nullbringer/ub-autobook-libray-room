from flask import Flask
from flask import request
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


@app.route('/verify')
def verify():

	target_url = request.args.get('target_url')

	# create a new Firefox session
	driver = webdriver.Chrome("/usr/local/bin/chromedriver")

	driver.get(target_url)

	#After opening the url above, Selenium clicks the specific agency link
	verify_button = driver.find_element_by_id('s-lc-verify-button')
	verify_button.click() 

	driver.close()


	return '<h1>Verified!</h1>'



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

