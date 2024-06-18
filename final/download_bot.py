import os
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def download_csv(start_year, start_month, end_year, end_month):
    start_year = int(start_year)
    start_month = int(start_month)
    end_year = int(end_year)
    end_month = int(end_month)
    options = EdgeOptions()
    prefs = {
        'download.default_directory': 'C:\\Users\\HP\\Documents\\earthquake-monitor\\final\\test_data\\',
        'profile.default_content_settings.popups': 0,
        'download.prompt_for_download': False,
        'directory_upgrade': True
    }
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Edge(options=options)
    # driver.get("https://google.com")

    for query_year in range(start_year, end_year+1):
        start_month_loop=1
        end_month_loop=12
        if(query_year == start_year):
            start_month_loop = start_month
        # last year
        if((query_year+1) == (end_year+1)):
            end_month_loop = end_month
        
        for query_month in range(start_month_loop,end_month_loop+1):
            # Open the website
            driver.get('https://scweb.cwa.gov.tw/en-us/earthquake/data/')

            # Wait for the page to load and the query condition element to be present
            query_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Search"))
            )

            # Change the value of the query condition input
            driver.execute_script("arguments[0].removeAttribute('readonly')", query_input)
            query_input.clear()
            query_input.send_keys(f"{query_month}-{query_year}")

            # Click the download button
            csv_button = driver.find_element(By.XPATH, '//a[@title="Export seismic data (Seismic activity.csv)"]')
            csv_button.click()

            if((query_year+1) == (end_year+1)):
                if((query_month+1) == (end_month+1)):
                    # Wait for the download to complete
                    time.sleep(5)

    driver.quit()



