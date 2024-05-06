from selenium import webdriver
from base import *
import sys

def main(driver, conn, grade, roll_number, year):

    student = fetch(driver, grade, roll_number, year)

    if isinstance(student, StudentRecord):
        print(str(roll_number) + "  ")
        store_record(student, conn)


if __name__ == '__main__':

    if len(sys.argv) != 6:
        print("Usage: python main.py <start> <end> <database> <grade> <year>")
        sys.exit(1)

    start = sys.argv[1]
    end = sys.argv[2]
    database = sys.argv[3]
    grade = sys.argv[4]
    year = sys.argv[5]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("excludeSwitches=enable-logging")
    chrome_options.add_argument("silent")
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument("disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    conn = create_connection(database)
    create_table(conn)
    
    #To Load Roll Numbers from Range
    current = start
    while current <= end:
        main(driver, conn, grade, current, year)
        current = str(int(current) + 1)

    
