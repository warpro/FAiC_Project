from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os, glob
from datetime import datetime

# Clean folder 
def folderCleaner():
    for f in glob.glob('./static/images/*.jpg'):
        os.remove(f)

# Save log
def logSaver(input_data):
    t = open("./log.txt", "at")
    now = str(datetime.now())
    now = now.rstrip("1234567890").rstrip(".")
    t.write("{} {}\n".format(now, input_data))
    t.close()

# Search and save images
def imageSearcher(input_data):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    input_data = input_data.strip()

    driver = webdriver.Chrome("chromedriver.exe",  options=options)
    driver.get("https://www.google.co.kr/imghp?hl=ko")

    # Search a Google image search for input name 
    search = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input")
    search.send_keys(input_data)
    search.send_keys(Keys.ENTER)

    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    
    # Save images 
    save_dir = "./static/images/"
    image_src_URLs = []
    for i in range(10):
        try:
            images[i].click()
            time.sleep(0.7)
            image_src_URL = driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img").get_attribute("src")
            image_src_URLs.append(image_src_URL)
            if i < 9:
                save_name = input_data + "0" + str(i+1) + ".jpg"
            else:
                save_name = input_data + str(i+1) + ".jpg"
            urllib.request.urlretrieve(image_src_URL, save_dir + save_name)
        except:
            pass

    # Finish 
    driver.quit()
    
    return image_src_URLs