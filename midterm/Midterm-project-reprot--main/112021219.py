import re
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
import csv
from pprint import pformat

class Laptop:
    def __init__(self,title,price,ram=None,ssd=None):
        self.title = title
        self.price = price
        self.ram = ram
        self.ssd = ssd

    def __str__(self):
        return f"Title: {self.title}, Price: {self.price}, RAM: {self.ram}, SSD: {self.ssd}"

class EbayLaptopScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.laptop_details = []
        self.laptop_objects = []

    def scrape_laptops(self):
        laptop_details = []
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            laptop_listings = soup.find_all('div', class_='s-item__info')

            for i, laptop in enumerate(laptop_listings[:10]):
                title = laptop.find('h3', class_='s-item__title').text.strip()
                price = laptop.find('span', class_='s-item__price').text.strip()
                laptop_details.append({'Title': title, 'Price': price})
            self.laptop_details = laptop_details
            messagebox.showinfo("Scraping Completed", "Scraping completed.")
        return laptop_details

    def extract_ram_and_ssd(self, title):
        ram_pattern = r'(\d+\s*GB)'
        ram_match = re.search(ram_pattern, title)
        ram = ram_match.group(1) if ram_match else None

        ssd_pattern = r'(\d+\s*(?:GB|TB)\s*SSD)'
        ssd_match = re.search(ssd_pattern, title)
        ssd = ssd_match.group(1) if ssd_match else None
        return ram, ssd

    def process_laptops(self):
        for laptop in self.laptop_details:
            title = laptop['Title']
            price = laptop['Price']
            ram, ssd = self.extract_ram_and_ssd(title)
            laptop_obj = Laptop(title, price, ram, ssd)
            self.laptop_objects.append(laptop_obj)
            print(laptop_obj)

    def store_to_csv(self, output_file):
        if self.laptop_details:
            with open(output_file, 'w', newline='', encoding='utf8') as file:
                writer = csv.DictWriter(file, fieldnames=["Title", "Price"])
                writer.writeheader()
                writer.writerows(self.laptop_details)
            messagebox.showinfo("Data Stored", f"Details of the first 10 laptops have been saved to '{output_file}'.")

    def print_laptop_details(self):
        details_window = tk.Toplevel()
        details_window.title("Laptops Details")

        text_area = scrolledtext.ScrolledText(details_window, width=80, height=20)
        text_area.pack(expand=True, fill='both')

        text_area.insert(tk.END, pformat(self.laptop_details))
        text_area.configure(state='disabled')


class LaptopFilter:
    @staticmethod
    def display_laptops(laptops):
        for laptop in laptops:
            print(laptop)

    @staticmethod
    def filter_laptops_by_ram(ram):
        filtered_laptops = [laptop for laptop in scraper.laptop_objects if laptop.ram == ram]
        return filtered_laptops


def handle_ram_filter(ram):
    filtered_laptops = LaptopFilter.filter_laptops_by_ram(ram)
    if filtered_laptops:
        LaptopFilter.display_laptops(filtered_laptops)
    else:
        print("No laptops found with the specified RAM:", ram)


def handle_option(option):
    match option:
        case 1:
            scraper.scrape_laptops()
            scraper.process_laptops()
        case 2:
            scraper.store_to_csv(output_file)
        case 3:
            scraper.print_laptop_details()


if __name__ == "__main__":
    url = "https://www.ebay.com/b/PC-Laptops-Netbooks/177/bn_317584"
    output_file = "laptop_details_ebay_1.csv"

    scraper = EbayLaptopScraper(url)

    def option_selected(option):
        handle_option(option)

    window = tk.Tk()
    window.title("Ebay Laptop Scraper")

    tk.Label(window, text="Choose an option:").pack()

    tk.Button(window, text="Scrape laptops", command=lambda: option_selected(1)).pack()
    tk.Button(window, text="Store data to CSV", command=lambda: option_selected(2)).pack()
    tk.Button(window, text="List of laptop", command=lambda: option_selected(3)).pack()
    tk.Button(window, text="4GB of RAM", command=lambda: handle_ram_filter("4GB")).pack()
    tk.Button(window, text="8GB of RAM", command=lambda: handle_ram_filter("8GB")).pack()
    tk.Button(window, text="16GB of RAM", command=lambda: handle_ram_filter("16GB")).pack()
    tk.Button(window, text="32GB of RAM", command=lambda: handle_ram_filter("32GB")).pack()
    tk.Button(window, text="64GB of RAM", command=lambda: handle_ram_filter("64GB")).pack()

    window.mainloop()

