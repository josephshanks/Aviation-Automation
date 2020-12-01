from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')

#To answer the given question specifically, a list of the four aircrafts: Pilatus PC-12, Cessna Caravan, Beechcraft Super King Air 200, Cessna Citation Excel/ELS
airplane_types=['PC12','C208','BE20','C56X']
aircraft_avg_dict = {}

# Using Chrome to access web
driver = webdriver.Chrome('./chromedriver1')

def retrive_aircraft_information(airplane_code):
    '''
    INPUT: string - Aircraft Code
    '''
    # Open the website
    driver.get('https://flightaware.com/live/aircrafttype/')
    
    # Path to textbox to insert given airplane_code
    airplane=driver.find_element_by_xpath("/html/body/div[3]/div[1]/form/div/input")
    airplane.send_keys(airplane_code)
    
    # Clicks button after airplane code is entered
    button=driver.find_element_by_xpath("/html/body/div[3]/div[1]/form/div/button")
    button.click()

def plot_average_flight_time():
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_title('Average Flight Times by Aircraft Type')
    ax.set_xlabel('Aircraft Type')
    ax.set_ylabel('Avg Flight Time (min)');
    for k in sorted(aircraft_avg_dict):
        ax.bar(k,aircraft_avg_dict[k])
    plt.show()
    
# Run this cell for four browsers to open for each aircraft listed above
for i in airplane_types:
    total_flight_time = 0
    number_of_flights = 0
    
    retrive_aircraft_information(i)
    content = driver.find_element_by_class_name("prettyTable")
    table_body = content.find_element_by_tag_name("tbody")
    flight_rows = table_body.find_elements_by_tag_name("tr")
    
    flight_list = []
    for flight in flight_rows:
        flight_information_columns = flight.find_elements_by_tag_name('td')
        ident = flight_information_columns[0].text
        airplane_type = flight_information_columns[1].text
        origin = flight_information_columns[2].text
        destination = flight_information_columns[3].text
        departure = flight_information_columns[4].text
        arrival = flight_information_columns[5].text
        flight_time = flight_information_columns[6].text

        flight_data = {}

        flight_data['ident'] = ident
        flight_data['airplane_type'] = airplane_type
        flight_data['origin'] = origin
        flight_data['destination'] = destination
        flight_data['departure'] = departure
        flight_data['arrival'] = arrival
        flight_data['travel_time'] = flight_time

        flight_list.append(flight_data)

        #generate the excel spreadsheet with name equal to i (aircraft)
        data_spreadsheet=pd.DataFrame(data=flight_list)
        data_spreadsheet.to_excel(i + '.xlsx')

        # Check for empty values
        if flight_time == '':
            continue
        else:
            duration = flight_time.split(':')
            hours = int(duration[0])
            minutes = int(duration[1])

            hours *= 60
            total = hours + minutes
            total_flight_time += total
            number_of_flights += 1

    # Error check to make sure at least one value was gathered.
        if number_of_flights == 0:
            print('No recorded flights')

    avg_flight_time = total_flight_time / number_of_flights
    
    aircraft_avg_dict[i] = avg_flight_time

# Create and show graph  
plot_average_flight_time()

