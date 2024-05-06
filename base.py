from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import sqlite3
import requests

# Matric CheckBox
def matric_checkbox_click(driver) -> None:
    try:
        matric_checkbox_xpath = '//*[@id="rdlistCourse"]/tbody/tr/td[1]/label'
        matric_checkbox = driver.find_element(by=By.XPATH, value=matric_checkbox_xpath)
        matric_checkbox.click()
    except:
        pass

# Intermediate
def intermediate_checkbox_click(driver) -> None:
    try:
        intermediate_checkbox_xpath = '//*[@id="rdlistCourse"]/tbody/tr/td[2]/label'
        intermediate_checkbox = driver.find_element(by=By.XPATH, value=intermediate_checkbox_xpath)
        intermediate_checkbox.click()
    except:
        pass

# Type Roll Number
def type_roll_no(driver, roll : str) -> None:
    try:
        roll_no_field_xpath = '//*[@id="txtFormNo"]'
        roll_no_field = driver.find_element(by=By.XPATH, value=roll_no_field_xpath)
        roll_no_field.clear()
        roll_no_field.send_keys(roll)
    except:
        pass

# Select Exam Type
def select_exam_type(driver, index : int) -> None:
    try:
        select_element_xpath = '//select[@id="ddlExamType"]'
        select_element = driver.find_element(By.XPATH, select_element_xpath)
        select = Select(select_element)
        options_count = len(select.options)
        if 0 <= index < options_count:
            select.select_by_index(index)
    except:
        pass

# Select Year
def select_year(driver, year : str) -> None:
    try:
        select_element_xpath = '//select[@id="ddlExamYear"]'
        select_element = driver.find_element(By.XPATH, select_element_xpath)
        select = Select(select_element)
        for option in select.options:
            if option.get_attribute("value") == year:
                select.select_by_value(year)
                break
    except:
        pass

# View Result Button Click
def view_result_button_click(driver) -> None:
    try:
        view_result_button_xpath = '//*[@id="Button1"]'
        view_result_button = driver.find_element(By.XPATH, view_result_button_xpath)
        view_result_button.click()
    except:
        pass

# Student Class
class StudentRecord:
    grade : str = None
    batch : str = None

    def __init__(self, roll_no, reg_no, cnic, fcnic, name, fname, institute, group, result, result_sentence, image_binary):
        self.roll_no = roll_no
        self.reg_no = reg_no
        self.cnic = cnic
        self.fcnic = fcnic
        self.name = name
        self.fname = fname
        self.institute = institute
        self.group = group
        self.result = result
        self.result_sentence = result_sentence
        self.image_binary = image_binary
    
    def __str__(self):
        return f"Roll No: {self.roll_no}\nRegistration No: {self.reg_no}\nCNIC: {self.cnic}\nFather's CNIC: {self.fcnic}\nName: {self.name}\nFather's Name: {self.fname}\nInstitute: {self.institute}\nGroup: {self.group}\nResult: {self.result}\nResult in Sentence: {self.result_sentence}"

    # print representation of the object using print() function
    def __repr__(self):
        return str(self)

# Fetch Record
def fetch_record(driver) -> StudentRecord:
    
    # Roll Number
    try:
        roll_no_xpath = '//label[@id="lblRollNoval"]'
        roll_no_label = driver.find_element(by=By.XPATH, value=roll_no_xpath)
        roll_no = roll_no_label.text
    except:
        if(driver.current_url == 'http://result.biselahore.com/Error.aspx'):
            print("Student not exist")
            return
        print("Error at Roll Number Fetch")

    # Registration Number
    try:
        reg_no_xpath = '//label[@id="lblRegNum"]'
        reg_no_label = driver.find_element(by=By.XPATH, value=reg_no_xpath)
        reg_no = reg_no_label.text
    except:
        # print("Error at Registration Number Fetch")
        pass

    # Student CNIC Number
    try:
        cnic_xpath = '//label[@id="lblBFARM"]'
        cnic_label = driver.find_element(by=By.XPATH, value=cnic_xpath)
        cnic = cnic_label.text
    except:
        # print("Error at CNIC Number Fetch")
        pass

    # Father CNIC Number
    try:
        fcnic_xpath = '//label[@id="lblFatherNIC"]'
        fcnic_label = driver.find_element(by=By.XPATH, value=fcnic_xpath)
        fcnic = fcnic_label.text
    except:
        # print("Error at Father CNIC Fetch")
        pass

    # Student Name
    try:
        name_xpath = '//label[@id="Name"]'
        name_label = driver.find_element(by=By.XPATH, value=name_xpath)
        name = name_label.text
    except:
        # print("Error at Student Name Fetch")
        pass

    # Father Name
    try:
        fname_xpath = '//label[@id="lblFatherName"]'
        fname_label = driver.find_element(by=By.XPATH, value=fname_xpath)
        fname = fname_label.text
    except:
        # print("Error at Father Name Fetch")
        pass

    # Institute
    try:
        institute_xpath = '//label[@id="lblExamCenter"]'
        institute_label = driver.find_element(by=By.XPATH, value=institute_xpath)
        institute = institute_label.text
    except:
        # print("Error at Institue Name Fetch")
        pass

    # Group
    try:
        group_xpath = '//label[@id="lblGroup"]'
        group_label = driver.find_element(by=By.XPATH, value=group_xpath)
        group = group_label.text
    except:
        # print("Error at Group Name Fetch")
        pass

    # Result
    try:
        table_element = driver.find_element(by=By.ID, value="GridStudentData")
        rows = table_element.find_elements(by=By.XPATH, value=".//tr")
        last_row = rows[-1]
        cells = last_row.find_elements(by=By.XPATH, value=".//td")
        result = cells[-1].text
    except:
        # print("Error at Result Fetch")
        pass

    # Result in sentence
    try:
        result_sentence_xpath = '//*[@id="lblResultinSentences"]'
        result_sentence_label = driver.find_element(by=By.XPATH, value=result_sentence_xpath)
        result_sentence = result_sentence_label.text
    except:
        # print("Error at Result Sentence Fetch")
        pass

    # Student Image
    try:
        image_element = driver.find_element(by=By.ID, value="imgDisplay")
        image_url = image_element.get_attribute("src")
        response = requests.get(image_url)

        if response.status_code == 200:
            image_binary = response.content
            return StudentRecord(roll_no, reg_no, cnic, fcnic, name, fname, institute, group, result, result_sentence, image_binary)

    except:
        print("Error at Image Fetch")


    return StudentRecord(roll_no, reg_no, cnic, fcnic, name, fname, institute, group, result, result_sentence, "")

# Create a database connection to a SQLite database
def create_connection(db_file : str):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print("Connected to SQLite database")
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Create a table in the SQLite database
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                fname TEXT,
                cnic TEXT,
                fcnic TEXT,
                roll_no TEXT UNIQUE,
                reg_no TEXT,
                study_group TEXT,
                institute TEXT,
                photo BLOB,
                result TEXT
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON students (name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fname ON students (fname)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cnic ON students (cnic)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fcnic ON students (fcnic)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_roll_no ON students (roll_no)")

        print("Table created successfully.")
    except sqlite3.Error as e:
        print(e)

# Store in Local DB
def store_record(record: StudentRecord, conn) -> None:

    try:
        cursor = conn.cursor()

        if record.grade == "10th":
            cursor.execute('''INSERT INTO students (roll_no_10th, school_reg_no, cnic, fcnic, name, fname, school, school_group, 
                                                    result_10th, school_photo, batch) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (record.roll_no, record.reg_no, record.cnic, record.fcnic, record.name, record.fname,
                    record.institute, record.group, record.result + "\t" + record.result_sentence, sqlite3.Binary(record.image_binary), record.batch))
        
        elif record.grade == "12th":
            if record.image_binary != "":
                cursor.execute('''INSERT INTO students (roll_no, reg_no, cnic, fcnic, name, fname, institute, study_group, 
                                                    result, photo) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (record.roll_no, record.reg_no, record.cnic, record.fcnic, record.name, record.fname,
                    record.institute, record.group, record.result + "\t" + record.result_sentence, sqlite3.Binary(record.image_binary)))
            else:
                cursor.execute('''INSERT INTO students (roll_no, reg_no, cnic, fcnic, name, fname, institute, study_group, 
                                                    result) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (record.roll_no, record.reg_no, record.cnic, record.fcnic, record.name, record.fname,
                    record.institute, record.group, record.result + "\t" + record.result_sentence))

        conn.commit()
    except Exception as e:
        print("Error Storing: " + record.roll_no)
        print(e)
        print("\n")
        with open("ErrorStore.txt", "a") as file:
            file.write(record.roll_no + "\n")


def fetch(driver, grade, roll_number, year):
    try:
        driver.get("http://result.biselahore.com/")

        if(grade == "10th" or grade == "9th"):
            matric_checkbox_click(driver)
        elif(grade == "12th" or grade == "11th"):
            intermediate_checkbox_click(driver)

        if(grade == "9th" or grade == "11th"):
            select_exam_type(driver, 2)
        elif(grade == "12th" or grade == "10th"):
            select_exam_type(driver, 1)

        type_roll_no(driver, str(roll_number))
        select_year(driver, year)


        view_result_button_click(driver)
        student = fetch_record(driver)

        if student is not None:
            student.grade = grade
            return student
        else:
            return None

    except Exception as e:
        print(e)
        if(driver.current_url != 'http://result.biselahore.com/Error.aspx'):
            print("Found But Error While Fetch: " + roll_number)
            with open("ErrorFetch.txt", "a") as file:
                file.write(roll_number + "\n")
        else:
            print("Error Fetching: " + roll_number)
            with open("Error404.txt", "a") as file:
                file.write(roll_number + "\n")
        return e