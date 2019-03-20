from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime  
from datetime import timedelta
import time 

def book_slot(driver, url, target_time, calender_id, next_slot=None):

	driver.get(url)

	#After opening the url above, Selenium clicks the specific agency link
	select_date_button = driver.find_element_by_class_name('fc-goToDate-button')
	select_date_button.click() 


	target_td = driver.find_element_by_xpath('//td[@data-date="'+calender_id+'"]')
	target_td.click()

	driver.implicitly_wait(5)

	available_rooms = driver.find_elements_by_xpath('//*[@id="eq-time-grid"]/div[2]/div/table/tbody/tr/td[3]/div/div/div/div[1]/div/table/tbody/tr')

	# available_rooms = available_rooms_body.find_elements_by_xpath(".//*")


	if next_slot==None:

		for room in available_rooms:
			av_slots = room.find_elements_by_css_selector('a.s-lc-eq-avail')

			should_book = True
			order_in_time = 0


			target_slot_list = []

			for slot in av_slots:

				slot_title = slot.get_attribute("title").split('-')[0].strip()
				room_no = slot.get_attribute("title").split('-')[1].strip()
				slot_time = slot_title.split(' ')[0].strip()
				weekday = slot_title.split(' ')[1].strip()

				if(order_in_time ==len(target_time)):
					break

				if(slot_time == target_time[order_in_time]):
					target_slot_list.append(slot)
					order_in_time = order_in_time + 1

				else:
					if(order_in_time != 0):
						should_book = False
						break


			if(should_book and len(target_slot_list) == len(target_time)):

				## book first pair of slots

				next_slot_title = target_slot_list[2].get_attribute("title")

				target_slot_list[0].click()

				submit_button = driver.find_element_by_id('submit_times') 
				submit_button.click() 


				submit_button = driver.find_element_by_id('terms_accept') 
				submit_button.click() 
				

				form_fname = driver.find_element_by_id("fname")
				form_lname = driver.find_element_by_id("lname")
				form_email = driver.find_element_by_id("email")

				form_fname.send_keys("Amlan")
				form_lname.send_keys("Gupta")
				form_email.send_keys("amlangup@buffalo.edu")

				driver.find_element_by_id("btn-form-submit").click()

				time.sleep(5)

				return next_slot_title
	else:

		for room in available_rooms:
			av_slots = room.find_elements_by_css_selector('a.s-lc-eq-avail')

			for slot in av_slots:
				if(slot.get_attribute("title") == next_slot):

					slot.click()

					submit_button = driver.find_element_by_id('submit_times') 
					submit_button.click() 


					submit_button = driver.find_element_by_id('terms_accept') 
					submit_button.click() 
					

					form_fname = driver.find_element_by_id("fname")
					form_lname = driver.find_element_by_id("lname")
					form_email = driver.find_element_by_id("email")

					form_fname.send_keys("Atrayee")
					form_lname.send_keys("Nag")
					form_email.send_keys("atrayeen@buffalo.edu")

					driver.find_element_by_id("btn-form-submit").click()

					time.sleep(5)

					return True




	return None



	


