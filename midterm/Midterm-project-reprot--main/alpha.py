import requests
from bs4 import BeautifulSoup


def scrape_ebay_laptops(url, output_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        laptop_listings = soup.find_all('div', class_='s-item__info')

        if len(laptop_listings) >= 20:
            with open(output_file, 'a') as file:
                for i, laptop in enumerate(laptop_listings[:20]):  # Limit to the first 10 laptops
                    title = laptop.find('h3', class_='s-item__title').text.strip()
                    price = laptop.find('span', class_='s-item__price').text.strip()
                    file.write(f"Laptop {i + 1}: {title} - Price: {price}\n")
            print(f"Details of the first 20 laptops have been saved to '{output_file}'.")
        else:
            print("Less than 20 laptop listings found.")
    else:
        print("Failed to retrieve data.")





if __name__ == "__main__":
    url = "https://www.ebay.com/b/PC-Laptops-Netbooks/177/bn_317584"
    output_file = "laptop_details_ebay.txt"
    scrape_ebay_laptops(url, output_file)
