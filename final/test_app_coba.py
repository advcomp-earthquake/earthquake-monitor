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

# Function to download CSV
def download_csv(query_month, query_year):
    # Setup Edge options
    options = EdgeOptions()
    prefs = {
        'download.default_directory': r'C:\\Users\\HP\\Documents\\earthquake-monitor\\final\\test_data\\',
        'profile.default_content_settings.popups': 0,
        'download.prompt_for_download': False,
        'directory_upgrade': True
    }
    options.add_experimental_option('prefs', prefs)

    # Path to the msedgedriver executable
    # service = EdgeService(executable_path='C:/Users/PC/AppData/Local/Temp/Rar$EXa24812.36344.rartemp/msedgedriver.exe')
    # driver = webdriver.Edge(service=service, options=options)
    driver = webdriver.Edge(options=options)


    try:
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

        # Wait for the download to complete
        time.sleep(5)

    finally:
        driver.quit()

# Function to handle button click
def on_download_click():
    query_month = month_entry.get()
    query_year = year_entry.get()

    if not query_month.isdigit() or not query_year.isdigit():
        messagebox.showerror("Invalid Input", "Month and Year should be numbers.")
        return

    if int(query_month) < 1 or int(query_month) > 12:
        messagebox.showerror("Invalid Input", "Month should be between 1 and 12.")
        return

    download_csv(query_month, query_year)
    messagebox.showinfo("Success", f"CSV for {query_month}-{query_year} downloaded successfully.")

# Initialize Tkinter window
root = tk.Tk()
root.title("Earthquake Data Downloader")

# Create labels and entries for month and year
tk.Label(root, text="Month (1-12):").pack(pady=5)
month_entry = tk.Entry(root)
month_entry.pack(pady=5)

tk.Label(root, text="Year (e.g., 2024):").pack(pady=5)
year_entry = tk.Entry(root)
year_entry.pack(pady=5)

# Create download button
download_button = tk.Button(root, text="Download CSV", command=on_download_click)
download_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
