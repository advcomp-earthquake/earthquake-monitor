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
from datetime import datetime

# Function to download CSV
def download_csv(start_month, start_year, end_month, end_year):
    # Setup Edge options
    options = EdgeOptions()
    prefs = {
        'download.default_directory': r'D:\pythonProject\\',
        'profile.default_content_settings.popups': 0,
        'download.prompt_for_download': False,
        'directory_upgrade': True
    }
    options.add_experimental_option('prefs', prefs)

    # Path to the msedgedriver executable
    service = EdgeService(executable_path='C:/Users/PC/AppData/Local/Temp/Rar$EXa24812.36344.rartemp/msedgedriver.exe')
    driver = webdriver.Edge(service=service, options=options)

    try:
        # Open the website
        driver.get('https://scweb.cwa.gov.tw/en-us/earthquake/data/')

        # Wait for the page to load and the query condition element to be present
        query_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Search"))
        )

        current_month = start_month
        current_year = start_year

        while current_year < end_year or (current_year == end_year and current_month <= end_month):
            # Change the value of the query condition input
            driver.execute_script("arguments[0].removeAttribute('readonly')", query_input)
            query_input.clear()
            query_input.send_keys(f"{current_month:02d}-{current_year}")

            # Click the download button
            csv_button = driver.find_element(By.XPATH, '//a[@title="Export seismic data (Seismic activity.csv)"]')
            csv_button.click()

            # Wait for the download to complete
            time.sleep(5)

            # Move to the next month
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1

    finally:
        driver.quit()

# Function to handle button click
def on_download_click():
    start_month = int(start_month_spinbox.get())
    start_year = int(start_year_spinbox.get())
    end_month = int(end_month_spinbox.get())
    end_year = int(end_year_spinbox.get())

    # Validate the input
    if start_year > end_year or (start_year == end_year and start_month > end_month):
        messagebox.showerror("Invalid Input", "End date must be after start date.")
        return

    download_csv(start_month, start_year, end_month, end_year)
    messagebox.showinfo("Success", f"CSV files from {start_month}-{start_year} to {end_month}-{end_year} downloaded successfully.")

# Initialize Tkinter window
root = tk.Tk()
root.title("Earthquake Data Downloader")

# Set the window size
root.geometry("600x600")

# Create labels and spinboxes for start day and month and year
#day
tk.Label(root, text="Start Day :").pack(pady=5)
start_month_spinbox = tk.Spinbox(root, from_=1, to=31, width=5)
start_month_spinbox.pack(pady=5)

#month
tk.Label(root, text="Start Month (1-12):").pack(pady=5)
start_month_spinbox = tk.Spinbox(root, from_=1, to=12, width=5)
start_month_spinbox.pack(pady=5)

#year
tk.Label(root, text="Start Year (e.g., 2023):").pack(pady=5)
current_year = datetime.now().year
start_year_spinbox = tk.Spinbox(root, from_=2023, to=current_year, width=5)
start_year_spinbox.pack(pady=5)

# Create labels and spinboxes for end day and month and year
#day
tk.Label(root, text="End Day :").pack(pady=5)
start_month_spinbox = tk.Spinbox(root, from_=1, to=31, width=5)
start_month_spinbox.pack(pady=5)

#month
tk.Label(root, text="End Month (1-12):").pack(pady=5)
end_month_spinbox = tk.Spinbox(root, from_=1, to=12, width=5)
end_month_spinbox.pack(pady=5)

#year
tk.Label(root, text="End Year (e.g., 2024):").pack(pady=5)
end_year_spinbox = tk.Spinbox(root, from_=2023, to=current_year, width=5)
end_year_spinbox.pack(pady=5)

# Create download button
download_button = tk.Button(root, text="Download CSV", command=on_download_click)
download_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
