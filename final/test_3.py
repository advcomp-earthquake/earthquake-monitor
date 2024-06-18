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
def download_csv(query_start_month, query_start_year,query_end_month,query_end_year):
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

        # Change the value of the query condition input
        driver.execute_script("arguments[0].removeAttribute('readonly')", query_input)
        for query_year in range(query_start_year, query_end_year):
            for query_month in range(query_start_month, query_end_month):
                query_input.clear()
                query_input.send_keys(f"{query_month}-{query_year}")

                # Click the download button
                csv_button = driver.find_element(By.XPATH, '//a[@title="Export seismic data (Seismic activity.csv)"]')
                csv_button.click()

        # Wait for the download to complete
        time.sleep(10)

    finally:
        driver.quit()

# Function to handle button click
def on_download_click():
    # query_month = month_entry.get()
    # query_year = year_entry.get()
    query_start_month = start_month_var.get()
    query_start_year = start_year_var.get()
    query_end_month = end_month_var.get()
    query_end_year = end_year_var.get()
    if not query_start_month.isdigit() or not query_start_year.isdigit():
        messagebox.showerror("Invalid Input", "Month and Year should be numbers.")
        return

    if int(query_start_month) < 1 or int(query_start_month) > 12:
        messagebox.showerror("Invalid Input", "Month should be between 1 and 12.")
        return
    
    if not query_end_month.isdigit() or not query_end_year.isdigit():
        messagebox.showerror("Invalid Input", "Month and Year should be numbers.")
        return

    if int(query_end_month) < 1 or int(query_end_month) > 12:
        messagebox.showerror("Invalid Input", "Month should be between 1 and 12.")
        return

    download_csv(query_start_month, query_start_year, query_end_month, query_end_year)
    messagebox.showinfo("Success", f"CSV for {query_start_month}-{query_start_year} to {query_end_month}-{query_end_year} downloaded successfully.")

# Initialize Tkinter window
root = tk.Tk()
root.title("Earthquake Data Downloader")

# Variables to store selected start and end dates
start_year_var = tk.StringVar(root)
start_month_var = tk.StringVar(root)
start_day_var = tk.StringVar(root)
end_year_var = tk.StringVar(root)
end_month_var = tk.StringVar(root)
end_day_var = tk.StringVar(root)

# Set default values
start_year_var.set("2024")  # Default start year
start_month_var.set("01")   # Default start month
start_day_var.set("01")     # Default start day
end_year_var.set("2024")    # Default end year
end_month_var.set("01")     # Default end month
end_day_var.set("01")       # Default end day

# Create labels for the Spinboxes
label_year = tk.Label(root, text="Year:")
label_month = tk.Label(root, text="Month:")
label_day = tk.Label(root, text="Day:")

# Create labels and Spinboxes for start date
start_date_label = tk.Label(root, text="Start Date")
start_year_label = tk.Label(root, text="Year:")
start_year_spin = tk.Spinbox(root, from_=1900, to=2100, textvariable=start_year_var, width=5)
start_month_label = tk.Label(root, text="Month:")
start_month_spin = tk.Spinbox(root, from_=1, to=12, textvariable=start_month_var, format="%02.0f", width=3)
start_day_label = tk.Label(root, text="Day:")
start_day_spin = tk.Spinbox(root, from_=1, to=31, textvariable=start_day_var, format="%02.0f", width=3)

# Create labels and Spinboxes for end date
end_date_label = tk.Label(root, text="End Date")
end_year_label = tk.Label(root, text="Year:")
end_year_spin = tk.Spinbox(root, from_=1900, to=2100, textvariable=end_year_var, width=5)
end_month_label = tk.Label(root, text="Month:")
end_month_spin = tk.Spinbox(root, from_=1, to=12, textvariable=end_month_var, format="%02.0f", width=3)
end_day_label = tk.Label(root, text="Day:")
end_day_spin = tk.Spinbox(root, from_=1, to=31, textvariable=end_day_var, format="%02.0f", width=3)

# Arrange the widgets in the window
start_date_label.pack(pady=10)
start_year_label.pack()
start_year_spin.pack()
start_month_label.pack()
start_month_spin.pack()
start_day_label.pack()
start_day_spin.pack()

end_date_label.pack(pady=10)
end_year_label.pack()
end_year_spin.pack()
end_month_label.pack()
end_month_spin.pack()
end_day_label.pack()
end_day_spin.pack()

# Create labels and entries for month and year
# tk.Label(root, text="Month (1-12):").pack(pady=5)
# month_entry = tk.Entry(root)
# month_entry.pack(pady=5)

# tk.Label(root, text="Year (e.g., 2024):").pack(pady=5)
# year_entry = tk.Entry(root)
# year_entry.pack(pady=5)

# Create download button
download_button = tk.Button(root, text="Download CSV", command=on_download_click)
download_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
