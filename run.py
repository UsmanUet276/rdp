import multiprocessing
import sys
import signal
import shutil
import os
import threading
import time
import mysql.connector
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
from bs4 import BeautifulSoup
import traceback

import re

from datetime import datetime

import psutil

# state id
st_id = "1416"

title_to_search = "Beauty Salon"
env = "localhost1"
def extract_text(title, title_to_search):
    # Check if title_to_search is present in title
    if title_to_search in title:
        # Remove title_to_search from title
        title = title.replace(title_to_search, "").strip()
        # Find the index of "in" in the modified title
        index_in = title.find("in")
        if index_in != -1:
            # Extract the text after "in"
            result = title[index_in + 3:].strip()
            # Check if result ends with a comma
            if ',' in result:
                result = result.split(',')[0].strip()
            return result
    return None


def kill_process_and_children():
    parent = psutil.Process(os.getpid())
    children = parent.children(recursive=True)
    for process in children:
        process.kill()
    parent.kill()


# Define a signal handler for SIGALRM
def handler(signum, frame):
    raise TimeoutError("Execution time limit reached")


def check_number_of_occurrences_in_db(address):
    """
    Check the number of occurrences of an address in the 'leads' table.

    Parameters:
    - address (str): The address to be checked.

    Returns:
    - int: The number of occurrences of the address in the 'leads' table.
    """
    # Establish a connection to the MySQL database
    # Connect to the MySQL database
    if env == 'localhost':
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="startyou_leads"
        )
    else:
        connection = mysql.connector.connect(
            host="alifarazco.com",
            port=3306,
            user="u244731553_leads",
            password="2021Cs142@uet.edu.pk",
            database="u244731553_leads",
        )
    try:
        # Create a cursor to interact with the database
        cursor = connection.cursor()
        print('address in function:' + address)
        # Execute a SQL query to count occurrences of the given address in the 'leads' table
        query = "SELECT COUNT(*) FROM leads WHERE address = %s"
        cursor.execute(query, (address,))

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return result[0] if result else 0

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("First")

def insert_data_into_leads_search_table(
        business_type_id, business_directory_id, country_id, state_id, city_id,
        title
):
    try:
        # Connect to the MySQL database
        if env == 'localhost':
            mydb2 = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="",
                database="startyou_leads"
            )
        else:
            mydb2 = mysql.connector.connect(
                host="alifarazco.com",
                port=3306,
                user="u244731553_leads",
                password="2021Cs142@uet.edu.pk",
                database="u244731553_leads",
            )

        # Create a cursor object to interact with the database
        cursor1 = mydb2.cursor()

        # Get today's date
        today_date = datetime.now().date()

        # SQL query to insert data into the leads table
        sql_insert_lead = f"""
            INSERT INTO lead_searches
            (business_type_id, business_directory_id, country_id, state_id, city_id,
            title) 
            VALUES 
            ({business_type_id}, {business_directory_id}, {country_id}, {state_id}, {city_id},
            '{title}');
        """

        # Execute the query
        cursor1.execute(sql_insert_lead)

        # Get the latest inserted ID
        cursor1.execute("SELECT LAST_INSERT_ID();")
        latest_id = cursor1.fetchone()[0]

        print(f"Record inserted successfully with ID: {latest_id}")

        # Commit the transaction
        mydb2.commit()

        return latest_id

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("Second")
        # Rollback the transaction in case of an error

def add_leads_to_db(id, title, website, phone, address, unique_emails, business_type_id, business_directory_id,
                    country_id, state_id,
                    city_id, map_link):
    id = id if id is not None else 0
    title = title if title is not None else 0
    website = website if website is not None else 0
    phone = phone if phone is not None else 0
    address = address if address is not None else 0
    business_type_id = business_type_id if business_type_id is not None else 0
    business_directory_id = business_directory_id if business_directory_id is not None else 0
    country_id = country_id if country_id is not None else 0
    state_id = state_id if state_id is not None else 0
    city_id = city_id if city_id is not None else 0
    emails = 0 if not unique_emails else ','.join(list(unique_emails))
    # Connect to the MySQL database
    if env == 'localhost':
        mydb1 = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="startyou_leads"
        )
    else:
        mydb1 = mysql.connector.connect(
            host="alifarazco.com",
            port=3306,
            user="u244731553_leads",
            password="2021Cs142@uet.edu.pk",
            database="u244731553_leads",
        )

    cursor = mydb1.cursor()

    try:
        # Check if the phone number already exists
        existing_phone_query = f"SELECT * FROM leads WHERE address = '{address}';"
        print(existing_phone_query)
        cursor.execute(existing_phone_query)
        existing_phone_result = cursor.fetchone()
        print(existing_phone_result)
        if website == 'abc.com':
            website = 0
        if not existing_phone_result:
            # Phone number doesn't exist, proceed with the insertion
            today_date = datetime.now().date()
            business_sub_type_id = '0'
            offer_id = '0'
            business_name = title
            date = today_date
            status = '0'
            completed_by = '0'

            # SQL query to insert data into the leads table
            print(map_link)
            sql_insert_lead = f"""
                INSERT INTO leads 
                (search_id, business_type_id, business_directory_id, country_id, state_id, city_id,
                business_sub_type_id, offer_id, business_name, website, phone, address, 
                emails, date, status, completed_by, map_link) 
                VALUES 
                ({id},{business_type_id}, {business_directory_id}, {country_id}, {state_id}, {city_id}, 
                {business_sub_type_id}, {offer_id}, '{business_name}', '{website}', 
                '{phone}', '{address}', '{emails}', {date}, {status}, '{completed_by}', '{map_link}');
            """

            # Execute the query
            cursor.execute(sql_insert_lead)
            cursor.execute("SELECT LAST_INSERT_ID();")
            latest_id = cursor.fetchone()[0]

            for email in unique_emails:
                sql_insert_emails = f"""
                                INSERT INTO lead_emails 
                                (lead_id, email) 
                                VALUES 
                                ('{latest_id}', '{email}');
                            """

                # Execute the query
                cursor.execute(sql_insert_emails)

            # Commit the transaction
            mydb1.commit()
            print("Record inserted successfully.")
        else:
            print("Address already exists. Record not inserted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("Third")
        # Rollback the transaction in case of an error
        mydb1.rollback()

    finally:
        # Close the cursor and the database connection
        cursor.close()
        mydb1.close()


def main():
    global re
    start_time12 = time.time()  # Get the current time
    # Get today's date
    today_date = datetime.now().date()
    # Connect to the MySQL database
    if env == 'localhost':
        mydb = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="startyou_leads"
        )
    else:
        mydb = mysql.connector.connect(
            host="alifarazco.com",
            port=3306,
            user="u244731553_leads",
            password="2021Cs142@uet.edu.pk",
            database="u244731553_leads",
        )

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("excludeSwitches=enable-logging")
    chrome_options.add_argument("silent")
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument("disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver2 = webdriver.Chrome(options=chrome_options)
    last_value = 0

    website2 = "https://www.google.com/maps/"
    path = 'msedgedriver.exe'

    # Set the user agent string
    user_agent = "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254"
    chrome_options.add_argument(f"user-agent={user_agent}")

    driver.maximize_window()
    driver2.maximize_window()
    driver.get(website2)

    # driver.maximize_window()

    def extract_text_by_xpath(xpath):
        element = driver.find_element(By.XPATH, xpath)
        return element.text.strip()


    cursor = mydb.cursor()
    query = "SELECT id FROM business_directories WHERE title = %s;"
    cursor.execute(query, (title_to_search,))

    # Fetch the result
    result = cursor.fetchone()
    directory_id = result[0] if result else None

    query = "SELECT COUNT(*) AS total_count FROM lead_searches WHERE state_id = %s AND business_directory_id = %s AND is_done = 1;"
    cursor.execute(query, (st_id, directory_id))

    # Fetch the result
    result = cursor.fetchone()
    total_count = result[0] if result else 0

    query = "SELECT COUNT(*) AS total_count FROM lead_searches WHERE state_id = %s AND business_directory_id = %s;"
    cursor.execute(query, (st_id, directory_id))

    # Fetch the result
    result = cursor.fetchone()
    total_count2 = result[0] if result else 0

    query = "SELECT COUNT(*) AS total_count FROM cities WHERE state_id = %s;"
    cursor.execute(query, (st_id,))

    # Fetch the result
    result = cursor.fetchone()
    total_city_count = result[0] if result else 0

    if total_count >= total_city_count:
        query = "SELECT * FROM states WHERE id = %s;"
        cursor.execute(query, (st_id,))

        # Fetch the result
        state = cursor.fetchone()
        if state:
            query = "SELECT * FROM business_directories WHERE title = %s;"
            cursor.execute(query, (title_to_search,))

            # Fetch the result
            directory = cursor.fetchone()
            if directory:
                business_type_id = directory[1]  # Fill this with appropriate value
                business_directory_id = directory[0]
                country_id = state[2]
                status = 1
                is_completed = 1

                # Execute the query to insert into leads_completed table
                insert_query = """
                            INSERT INTO leads_completed 
                            (business_type_id, business_directory_id, country_id, state_id, status, created_at, updated_at, is_completed) 
                            VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), %s);
                        """
                cursor.execute(insert_query,
                               (business_type_id, business_directory_id, country_id, st_id, status, is_completed))
                mydb.commit()

                print("Row inserted into leads_completed table successfully.")

            else:
                print("No directory found with title:", title_to_search)
        else:
            print("No state found with ID:", st_id)

        raise SystemExit("Cities in states are all scraped. Stopping code execution.")

    if total_count2 >= total_city_count:
        raise SystemExit("Cities in states are all scraped. Stopping code execution.")

    # query = "SELECT title FROM business_directories;"
    # cursor.execute(query)
    #
    # # Fetch one matching record
    # business_directories = cursor.fetchall()
    # for title_to_search_tuple in business_directories:

    try:
        cursor = mydb.cursor()

        # Use a parameterized query
        sql_query_business_directories = "SELECT id, title, business_type_id FROM business_directories WHERE title = %s;"
        cursor.execute(sql_query_business_directories, (title_to_search,))

        # Fetch one matching record
        business_directory = cursor.fetchone()

        sql_query_business_directories = f"SELECT id ,title FROM business_types WHERE id = {business_directory[2]};"

        # Execute the query
        cursor.execute(sql_query_business_directories)

        # Fetch one matching record
        business_type = cursor.fetchone()

        # Display the result
        if business_directory:
            print(business_directory)
        else:
            print(f"No business directory found with the title '{title_to_search}'.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("Fourth")

    b_id = str(business_directory[0])
    try:
        query = "SELECT * FROM lead_searches WHERE state_id = " + st_id + " AND business_directory_id = "+ b_id +" ORDER BY id DESC LIMIT 1;"
        cursor.execute(query)
        search = cursor.fetchone()
        search = search[6]

        print(search)

        result = extract_text(search, title_to_search)
        print(result)

        query = "SELECT * FROM cities WHERE name = '" + result + "' AND state_id = " + st_id + ";"
        cursor.execute(query)
        city_searched = cursor.fetchone()
        city_searched = city_searched[0]
        city_searched = str(city_searched)
        print(city_searched)
    except:
        city_searched = 0

    # Get countries
    sql_query_city = """SELECT id FROM cities WHERE state_id = %s AND id >= %s;"""

    cursor.execute(sql_query_city, (st_id, city_searched))

    # Fetch the city IDs
    cities = cursor.fetchall()

    # Iterate through city IDs
    for city_id_tuple in cities:
        if time.time() - start_time12 >= 3600:
            start_time12 = 0
            break
        try:
            # Extract the number from the tuple
            city_id = city_id_tuple[0]

            # Now you can use the city_id in your second query
            sql_query_city_details = f"SELECT * FROM cities WHERE id = {city_id};"

            # Connect to the MySQL database
            if env == 'localhost':
                mydb = mysql.connector.connect(
                    host="localhost",
                    port=3306,
                    user="root",
                    password="",
                    database="startyou_leads"
                )
            else:
                mydb = mysql.connector.connect(
                    host="alifarazco.com",
                    port=3306,
                    user="u244731553_leads",
                    password="2021Cs142@uet.edu.pk",
                    database="u244731553_leads",
                )

            cursor = mydb.cursor()
            # Execute the second query
            cursor.execute(sql_query_city_details)

            # Fetch the details (if needed)
            city = cursor.fetchone()

            # Print or process the city details as needed
            if city:
                # SQL query to get the corresponding country
                sql_query_country = f"SELECT id, name FROM countries WHERE id = {city[4]};"

                # Execute the query
                cursor.execute(sql_query_country)

                # Fetch the country
                country = cursor.fetchone()

                if country:
                    # SQL query to get the corresponding state
                    sql_query_state = f"SELECT id, name FROM states WHERE id = {city[2]};"

                    # Execute the query
                    cursor.execute(sql_query_state)

                    # Fetch the state
                    state = cursor.fetchone()

                    # Display the results
                    print("City:", city)
                    print("Country:", country)
                    print("State:", state)
                else:
                    print(f"Country with ID {city[4]} not found.")
            else:
                print(f"City with ID {city_id} not found.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            print("Fifth")

        finally:
            # Close the cursor and the database connection
            cursor.close()

        cursor = mydb.cursor()
        # get directories

        search_box = driver.find_element(By.ID, 'searchboxinput')
        search_box.clear()
        search_query = f'{business_directory[1]} in {city[1]}, {state[1]}'
        print(search_query)
        search_query = search_query.replace("'", "")
        query = "SELECT * FROM lead_searches WHERE title = %s;"
        cursor.execute(query, (search_query,))

        # Fetch one matching record
        matching_records = cursor.fetchall()
        if len(matching_records) >= 1:
            last_record = matching_records[-1]  # Get the last record
            print(last_record[6])

            # Check if is_done column of the last record is 1
            if last_record[7] == 1:
                continue
            elif last_record[7] == 0:
                # Delete the last record
                last_record_id = last_record[0]  # Assuming 'id' is the primary key column

                delete_query = "DELETE FROM leads WHERE search_id = %s;"
                cursor.execute(delete_query, (last_record_id,))

                delete_query = "DELETE FROM lead_searches WHERE id = %s;"
                cursor.execute(delete_query, (last_record_id,))
                # Commit the deletion
                mydb.commit()
        # Type text into the search box
        search_box.send_keys(search_query)

        # Find the search button by its ID
        search_button = driver.find_element(By.ID, 'searchbox-searchbutton')

        # Click the search button
        try:
            search_button.click()
        except:
            print("Search button not found")
        inserted_id = insert_data_into_leads_search_table(
            business_type_id=business_type[0],
            business_directory_id=business_directory[0],
            country_id=country[0],
            state_id=state[0],
            city_id=city[0],
            title=search_query)
        time.sleep(10)
        # time.sleep(100)
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Results for")]/div/div/a')))

            # Find the specific element to scroll within
            results_element = driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for")]')
        except:
            continue

        # Get the initial scroll height within the element
        last_height = driver.execute_script("return arguments[0].scrollHeight;", results_element)
        print(last_height)
        start_index = 0
        results = []
        el_count = 0

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        csv_filename = f"{business_directory[1]}_{city[1]}_{state[1]}_{country[1]}_{formatted_datetime}.csv"
        columns = ['business_type', 'business_directory', 'country', 'state', 'city', 'business_name', 'website',
                   'phone',
                   'address', 'emails', 'date']
        if os.path.exists(csv_filename):
            base_name, extension = os.path.splitext(csv_filename)
            count = 1
            new_filename = f'{base_name}{count}{extension}'

            # Keep incrementing the count until a unique filename is found
            while os.path.exists(new_filename):
                count += 1
                new_filename = f'{base_name}{count}{extension}'

            # Rename the file
            shutil.move(csv_filename, new_filename)
        # df = pd.DataFrame(columns=columns)
        # df.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False)

        a = 0
        # Extract data using infinite scroll
        count = 0
        while True:
            time.sleep(3)
            # Wait for a moment (optional, you can adjust the time according to your needs)
            temp_count = 0
            while True:
                if temp_count == 3:
                    print(0)
                    break
                try:
                    results_element = driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for")]')
                    temp_height = driver.execute_script("return arguments[0].scrollHeight;", results_element)
                    if temp_height == last_height:
                        # Scroll a little bit up
                        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollTop - 100);",
                                              results_element)

                        # Wait for a moment (optional)
                        time.sleep(1)

                        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", results_element)
                        temp_count += 1
                        print(1)
                    else:
                        break
                except:
                    print(2)
                    continue

            # Calculate new scroll height and compare it with last scroll height
            print(3)
            time.sleep(10)
            try:
                results_element = driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for")]')
            except:
                print("Result  section not foundf")
                continue
            new_height = driver.execute_script("return arguments[0].scrollHeight;", results_element)
            print(new_height)
            print(4)
            start_index += 6
            if new_height == last_height:
                print(5)
                break
            else:
                print(6)
                last_height = new_height

        # time.sleep(600)
        try:
            elements = driver.find_elements(By.XPATH, '//div[contains(@aria-label, "Results for")]/div/div/a')
        except:
            continue

        # # Filter visible elements
        # visible_elements = [element for element in elements if element.is_displayed()]
        #
        # # Further refinement using explicit wait for visibility (optional)
        # refined_elements = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@aria-label, "Results for")]/div/div[./a]'))
        # )
        # elements = refined_elements
        print(len(elements))
        # ... (your existing code)
        # elements = driver.find_elements(By.XPATH, '//div[contains(@aria-label, "Results for")]/div/div/a')[start_index:]
        # df = pd.DataFrame(columns=columns)
        temp1 = a
        # Loop through each result and click on the link to gather more details
        for el in elements:
            if temp1 >= 1:
                temp1 -= 1
                continue

            a += 1
            # attrib = el.find_element(By.XPATH, './a')
            try:
                driver.execute_script("arguments[0].scrollIntoView(false);", el)
            except:
                continue

            max_retries = 3
            for _ in range(max_retries):
                try:
                    driver.execute_script("arguments[0].click();", el)
                    time.sleep(2)
                    break  # Break the loop if click is successful
                except Exception as e:
                    print(f"Click attempt failed: {e}")
                    time.sleep(1)  # Add a short delay before retrying
            phone = "None"
            print("pre title break")
            try:
                time.sleep(2)
                title = el.find_element(By.XPATH,
                                        '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1').text
            except:
                print("title break")
                continue
            # print(title)

            map_link = "0"
            try:
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Actions for")]')))

                btns = driver.find_elements(By.XPATH, '//div[contains(@aria-label, "Actions for")]/div')

                last_div = btns[-1]

                # Find the button inside the last div and click it
                button_inside_last_div = last_div.find_element(By.XPATH, './/button')
                text_share_element = button_inside_last_div.find_element(By.XPATH, "./div")
                text_share = text_share_element.text

                button_inside_last_div.click()

                if text_share == "Share":
                    wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//div[contains(@jsaction, "modal.backgroundClick")]//input')))

                    map_link_input = driver.find_elements(By.XPATH,
                                                          '//div[contains(@jsaction, "modal.backgroundClick")]//input')

                    map_link_input = map_link_input[0]

                    map_link = map_link_input.get_attribute('value')
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                "//div[contains(@jsaction, 'modal.backgroundClick')]//button[contains(@aria-label, 'Close')]")))

                    # Find the button element
                    close_btn = driver.find_element(By.XPATH,
                                                    "//div[contains(@jsaction, 'modal.backgroundClick')]//button[contains(@aria-label, 'Close')]")

                    # Click the button
                    close_btn.click()

                else:
                    map_link = driver.execute_script("return navigator.clipboard.readText();")

                print(map_link)

            except:
                print(
                    "************************************************Map Link Error************************************************")
                try:
                    close_btn = driver.find_element(By.XPATH,
                                                    "//div[contains(@jsaction, 'modal.backgroundClick')]//button[contains(@aria-label, 'Close')]")

                    # Click the button
                    close_btn.click()
                except:
                    continue

            try:
                wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Information for")]')))
                components = driver.find_elements(By.XPATH, '//div[contains(@aria-label, "Information for")]/div')
            except:
                continue
            # print(f"len: {len(components)}")
            # Use regular expressions to identify address, phone, and website
            try:
                div = driver.find_element(By.XPATH,
                                          '//img[contains(@src, "//www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png")]/../../..')
                address = div.find_element(By.XPATH, './div[2]/div').text.strip()
                print(address)
                # abc = check_number_of_occurrences_in_db(address)
                count += 1
                # if abc == 1:
                #     continue
            except:
                try:
                    # Wait for the button to be located
                    button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//button[contains(@aria-label, "Address: ")]'))
                    )

                    # Get the text from aria-label attribute
                    aria_label = button.get_attribute("aria-label")

                    # Extract the address from the aria-label
                    address = aria_label.replace("Address: ", "")

                    print(address)

                except Exception as e:
                    address = 0
            website = "abc.com"
            for i in range(3, len(components) + 1):
                try:
                    try:
                        # print(1)
                        temp = components[i].find_element(By.XPATH, './button/div/div[2]/div[1]').text.strip()
                    except:
                        # print(2)
                        temp = components[i].find_element(By.XPATH, './a/div/div[2]/div[1]').text.strip()
                    # Define regular expressions for phone and website
                    # print(3)
                    phone_pattern = re.compile(r'(\d{3}[-.\s]?){1,2}\d{3}[-.\s]?\d{4}', re.IGNORECASE)
                    # print(4)
                    website_pattern = re.compile(
                        r'^(((?!-))(xn--|_)?[a-z0-9-]{0,61}[a-z0-9]{1,1}\.)*(xn--)?([a-z0-9][a-z0-9\-]{0,60}|[a-z0-9-]{1,30}\.[a-z]{2,})$',
                        re.IGNORECASE)

                    # Check if temp contains phone using regex
                    # print(4)
                    if phone_pattern.search(temp):
                        # print(5)
                        phone = temp
                    # print(6)
                    if website_pattern.search(temp):
                        # Extract website using the appropriate XPath
                        # print(7)
                        try:
                            # print(1)
                            temp = components[i].find_element(By.XPATH, './button/div/div[2]/div[1]')
                        except:
                            # print(2)
                            temp = components[i].find_element(By.XPATH, './a').get_attribute('href').strip()
                        website = temp
                    # print(8)
                except:
                    abc = 3
            if phone == "None":
                try:
                    div = driver.find_element(By.XPATH,
                                              '//img[contains(@src, "//www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png")]/../../..')
                    phone = div.find_element(By.XPATH, './div[2]/div').text.strip()
                    print(phone)
                except:
                    try:
                        # Wait for the button to be located
                        button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//button[contains(@data-item-id, "phone:tel:")]'))
                        )

                        # Get the text from aria-label attribute
                        aria_label = button.get_attribute("data-item-id")

                        # Extract the address from the aria-label
                        phone = aria_label.replace("phone:tel:", "")

                        print(phone)

                    except Exception as e:
                        phone = 0

            try:
                if website != "None":
                    # Open the website
                    driver2.get(website)

                    # Wait for the page to fully load
                    WebDriverWait(driver2, 20).until(
                        lambda driver2: driver2.execute_script("return document.readyState") == "complete")

                    try:
                        close_button = WebDriverWait(driver2, 10).until(EC.presence_of_element_located(
                            (By.XPATH, "//div[contains(@aria-label, 'Close')]")))
                        close_button.click()
                    except:
                        abc = 0

                    # Get the HTML source of the page
                    page_source = driver2.page_source

                    # Use BeautifulSoup to parse the HTML
                    soup = BeautifulSoup(page_source, 'html.parser')

                    # Use a regular expression to find email addresses
                    import re

                    email_pattern = re.compile(
                        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?!jpg|jpeg|gif|webp|png|svg)[A-Za-z]{2,}\b')

                    # Use a set to store unique email addresses
                    unique_emails = set(re.findall(email_pattern, str(soup)))
                    emails = 0 if not unique_emails else ','.join(list(unique_emails))

                    first_facebook_link = None
                    for a_tag in soup.find_all('a', href=True):
                        if 'facebook' in a_tag['href']:
                            first_facebook_link = a_tag['href']
                            break

                    if first_facebook_link:
                        driver2.get(first_facebook_link)
                        WebDriverWait(driver2, 20).until(
                            lambda driver2: driver2.execute_script("return document.readyState") == "complete")

                        try:

                            close_btn = WebDriverWait(driver2, 10).until(
                                EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Close')]")))
                            def click_close_button():
                                try:
                                    close_button = WebDriverWait(driver2, 10).until(EC.presence_of_element_located(
                                        (By.XPATH, "//div[contains(@aria-label, 'Close')]")))
                                    close_button.click()
                                    print("clicked")
                                    return True
                                except:
                                    print("not clicked")
                                    return False

                            # Loop to continuously click on the element until it's not found anymore
                            while True:
                                if not click_close_button():
                                    break
                        except Exception as e:
                            print(e)
                        page_source = driver2.page_source

                        # Use BeautifulSoup to parse the HTML
                        soup2 = BeautifulSoup(page_source, 'html.parser')

                        # Use a regular expression to find email addresses
                        import re

                        email_pattern = re.compile(
                            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?!jpg|jpeg|gif|webp|png|svg)[A-Za-z]{2,}\b')

                        # Use a set to store unique email addresses
                        unique_emails = set(re.findall(email_pattern, str(soup2)))
                        emails = 0 if not unique_emails else ','.join(list(unique_emails))


                    print("email not found in home page")
                    contact_page_link = None
                    for a_tag in soup.find_all('a'):
                        if 'contact' in a_tag.get('href', '').lower():
                            contact_page_link = a_tag.get('href')
                            if contact_page_link.startswith('/'):
                                contact_page_link = contact_page_link[1:]
                                contact_page_link = website + contact_page_link
                                print(contact_page_link)
                            else:
                                print(contact_page_link)
                            break
                    if contact_page_link:
                        driver2.get(contact_page_link)
                        WebDriverWait(driver2, 20).until(
                            lambda driver2: driver2.execute_script("return document.readyState") == "complete")
                        page_source = driver2.page_source

                        # Use BeautifulSoup to parse the HTML
                        soup = BeautifulSoup(page_source, 'html.parser')

                        # Use a regular expression to find email addresses
                        import re

                        email_pattern = re.compile(
                            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?!jpg|jpeg|gif|webp|png|svg)[A-Za-z]{2,}\b')

                        # Use a set to store unique email addresses
                        unique_emails = set(re.findall(email_pattern, str(soup)))
                        emails = 0 if not unique_emails else ','.join(list(unique_emails))

                    if emails == 0:
                        first_facebook_link = None
                        for a_tag in soup.find_all('a', href=True):
                            if 'facebook' in a_tag['href']:
                                first_facebook_link = a_tag['href']
                                break

                        if first_facebook_link:
                            driver2.get(first_facebook_link)
                            WebDriverWait(driver2, 20).until(
                                lambda driver2: driver2.execute_script("return document.readyState") == "complete")

                            try:
                                close_btn = WebDriverWait(driver2, 10).until(
                                    EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Close')]")))

                                def click_close_button():
                                    try:
                                        close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                            (By.XPATH, "//div[contains(@aria-label, 'Close')]")))
                                        close_button.click()
                                        return True
                                    except:
                                        return False

                                # Loop to continuously click on the element until it's not found anymore
                                while True:
                                    if not click_close_button():
                                        break
                            except Exception as e:
                                print(e)

                            page_source = driver2.page_source

                            # Use BeautifulSoup to parse the HTML
                            soup2 = BeautifulSoup(page_source, 'html.parser')

                            # Use a regular expression to find email addresses
                            import re

                            email_pattern = re.compile(
                                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?!jpg|jpeg|gif|webp|png|svg)[A-Za-z]{2,}\b')

                            # Use a set to store unique email addresses
                            unique_emails = set(re.findall(email_pattern, str(soup2)))
                            emails = 0 if not unique_emails else ','.join(list(unique_emails))

                    results.append({
                        'title': title,
                        'website': website,
                        'phone': phone,
                        'address': address,
                        'emails': emails,
                    })
                    add_leads_to_db(inserted_id, title, website, phone, address, unique_emails, business_type[0],
                                    business_directory[0],
                                    country[0], state[0], city[0], map_link)
                    print('address before function:' + address)
                    no = check_number_of_occurrences_in_db(address)
                    # if no <= 1 and emails != 0:
                    #     df = pd.concat([df, pd.DataFrame({
                    #         'business_type': business_type[1],
                    #         'business_directory': business_directory[1],
                    #         'country': country[1],
                    #         'state': state[1],
                    #         'city': city[1],
                    #         'business_name': [title],
                    #         'website': [website],
                    #         'phone': [phone],
                    #         'address': [address],
                    #         'emails': [emails],
                    #         'date': today_date
                    #     })], ignore_index=True)
            except Exception as e:
                unique_emails = []
                add_leads_to_db(inserted_id, title, 0, phone, address, unique_emails, business_type[0],
                                business_directory[0],
                                country[0], state[0], city[0], map_link)
                print(f"An error occurred while extracting emails from {website}: {e}")
            finally:
                print('1e')
                # Go back to the previous page
                # driver.back()
            # Scroll down within the element
        # df.to_csv(csv_filename, mode='a', header=not os.path.exists(csv_filename), index=False)
        # Connect to the MySQL database
        if env == 'localhost':
            mydb = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="",
                database="startyou_leads"
            )
        else:
            mydb = mysql.connector.connect(
                host="alifarazco.com",
                port=3306,
                user="u244731553_leads",
                password="2021Cs142@uet.edu.pk",
                database="u244731553_leads",
            )

        cursor = mydb.cursor()
        el_count = len(elements)
        # Execute the SELECT query to get the id
        select_query = "SELECT id FROM lead_searches WHERE title = %s;"
        cursor.execute(select_query, (search_query,))
        result = cursor.fetchone()

        if result:
            # Extracting the id from the result
            search_id = result[0]
            print("ID found:", search_id)
            # Execute the SELECT query to count the number of leads
            select_leads_count_query = "SELECT COUNT(*) FROM leads WHERE search_id = %s;"
            cursor.execute(select_leads_count_query, (search_id,))
            leads_count_result = cursor.fetchone()
            if leads_count_result:
                leads_count_result = leads_count_result[0]
            else:
                leads_count_result = 0
            # Now, update the 'is_done' field
            update_query = "UPDATE lead_searches SET is_done = 1, leads_count = %s, items_count = %s WHERE id = %s;"
            cursor.execute(update_query, (leads_count_result, el_count, search_id,))
            mydb.commit()

            print("is_done updated successfully.")
        else:
            print("No records found for the given title:", search_query)

        cursor.close()

        # results_element = driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for")]')
        # # Scroll to the bottom
        # driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", results_element)


if __name__ == "__main__":
    while True:
        try:
            main()
        except TimeoutError:
            print("Execution time limit reached. Restarting...")
            time.sleep(10)  # Sleep for 10 seconds before restarting

            # Kill the current process before restarting
            current_process = subprocess.Popen(["pgrep", "-f", sys.argv[0]], stdout=subprocess.PIPE)
            output, _ = current_process.communicate()
            if output:
                for pid in output.split():
                    os.kill(int(pid), signal.SIGKILL)

            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            if tb:
                print(f"Error occurred at line {tb[-1][1]}: {e}")
            else:
                print(f"Error occurred: {e}")
            time.sleep(5)
