import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time
# def scrape_website(website):
#     print("Launching chrome browser...")
#     chrome_driver_path=r"C:\Users\rk186\OneDrive\Desktop\Ai web Scraper\chromedriver.exe"
#     options=webdriver.ChromeOptions()
#     # driver=webdriver.Chrome(service=Service(chrome_driver_path),options=options)
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="114.0.5735.90").install()), options=options)
#     try:
#         driver.get(website)
#         print("Page loaded...")
#         html=driver.page_source
#         time.sleep(10)
#         return html
#     finally:
#         driver.quit()
def scrape_website(website):
    print("Launching Chromium browser...")

    # Set options for Chromium (headless mode)
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"  
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the driver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="120.0.6099.109").install()), options=chrome_options)
    
    try:
        # Open the website
        driver.get(website)
        print("Page loaded...")
        
        # Get page source (HTML content)
        html = driver.page_source
        time.sleep(5)  # Optional wait time to let the page fully load
        
        return html
    
    finally:
        driver.quit()  

def extract_boby_content(html_content):
    soup=BeautifulSoup(html_content,"html.parser")
    body_content=soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup=BeautifulSoup(body_content,"html.parser")
    for script_or_style in soup(["script","style"]):
        script_or_style.extract()
        
    cleanned_content=soup.get_text(separator="\n")
    cleanned_content="\n".join(line.strip() for line in cleanned_content.splitlines() if line.strip())
    
    return cleanned_content

def split_dom_content(dom_content,max_lenght=6000):
    return [
        dom_content[i : i +max_lenght] for i in range(0,len(dom_content),max_lenght)
    ]
    
