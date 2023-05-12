import os
import time
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Function to scrape the website using Selenium
def scrape_website(url, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set up Selenium WebDriver
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for JavaScript to execute and the page to fully render
    time.sleep(5)  # Adjust the wait time as needed

    # Save the rendered HTML to a file
    file_path = os.path.join(output_dir, 'index.html')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

    # Parse the rendered HTML to find links to other pages
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a')

    # Visit each linked page and save the rendered HTML
    for link in links:
        page_url = link.get('href')
        if page_url.startswith('/'):
            page_url = url + page_url
        driver.get(page_url)
        time.sleep(5)  # Adjust the wait time as needed
        file_name = page_url.split('/')[-1]
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    # Quit the Selenium WebDriver
    driver.quit()

# Function to create a zip file from the scraped website
def create_zip(output_dir, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, output_dir)
                zip_file.write(file_path, arc_name)

# Main function to initiate the website scraping and zipping
def main():
    url = 'https://agendadusommeil.xyz'  # Replace with the website URL you want to scrape
    output_dir = 'website'  # Output directory to save the scraped web pages
    zip_file_path = 'website.zip'  # Path to save the final zip file

    scrape_website(url, output_dir)
    create_zip(output_dir, zip_file_path)

    print('Website scraping and zipping completed.')

# Run the main function
if __name__ == '__main__':
    main()
main.p