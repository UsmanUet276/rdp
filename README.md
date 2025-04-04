# 🕷️ Multi-threaded Web Scraper with MySQL Integration

This Python-based web scraper is built for efficient data scraping using multithreading, allowing the scraping process to run in parallel chunks. The scraped data is parsed and structured using `BeautifulSoup` and `pandas`, then saved directly into a MySQL database using `mysql-connector-python`. `psutil` is used to monitor system performance and resource usage during execution.

---

## 🚀 Features

- ⚡ Multi-threaded scraping for faster performance  
- 🌐 Dynamic content support using Selenium  
- 🍜 HTML parsing with BeautifulSoup4  
- 📊 Data processing and formatting with pandas  
- 💾 Direct storage to MySQL DB  
- 🧠 System monitoring with psutil  

---

## 🧰 Requirements

Install the required dependencies via pip:

```bash
pip install -r requirements.txt
```

Ensure that you have:

- ChromeDriver or another browser driver installed and added to your system's PATH.  
- A MySQL server running with proper credentials.

You can create a `requirements.txt` file with the following content:

```
mysql-connector-python
pandas
selenium
beautifulsoup4
psutil
```

---

## 🧪 Usage

To run the scraper, simply execute the following command:

```bash
python run.py
```

This will:

1. Divide the list of URLs into chunks.
2. Start multiple threads for scraping.
3. Use Selenium to render dynamic pages (if needed).
4. Parse the HTML content using BeautifulSoup.
5. Process the data with pandas.
6. Store the processed data into a MySQL database.

---

## 📈 Monitoring

The scraper utilizes `psutil` to track:

- Memory usage  
- CPU load  
- Thread activity  

You can extend the logging and statistics to monitor the system performance during the scraping process.

---

## 📌 Notes

- Ensure that your Selenium browser driver version matches the version of your browser.
- Adjust the number of threads and the chunk size for optimal performance, depending on the server and website being scraped.
- Make sure to respect the `robots.txt` file and terms of service of the target websites.
- For websites that require dynamic content rendering, Selenium will handle the page rendering, while BeautifulSoup will be used for parsing the content.
