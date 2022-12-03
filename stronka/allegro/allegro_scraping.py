import pyshorteners
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
from multiprocessing import freeze_support
import time
import json

class Allegro:
    def __init__(self, driver):
        self.driver = driver
        self.week = {"po":1,"wt":2,"cz":4,"pi":5,"so":6,"ni":7}


    def loading_page(self):
        self.driver.get("https://allegro.pl/")

    def handling_cookies(self):
        try:
            cookies = self.driver.find_element(By.XPATH, "//*[@id=\"opbox-gdpr-consents-modal\"]/div/div[2]/div/div[2]/button[2]")
            self.driver.execute_script("arguments[0].click()", cookies)
        except NoSuchElementException:
            print("No cookies")


    def searching(self, items):

        for item in items:
            self.handling_cookies()
            search = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div/div[3]/header/div/div/div/div/form/input")
            search.clear()
            search.send_keys(item)
            search.send_keys(Keys.ENTER)
            products = []

            for i in range(1,10):
                attributes = {}
                XP_url = f"//*[@id=\"search-results\"]/div[5]/div/div/div[1]/div/div/section[2]/article[{i}]/div/div/div[2]/div[1]/h2/a"
                XP_price = f"//*[@id=\"search-results\"]/div[5]/div/div/div[1]/div/div/section[2]/article[{i}]/div/div/div[2]/div[2]/div/div/span"
                XP_name = f"//*[@id=\"search-results\"]/div[5]/div/div/div[1]/div/div/section[2]/article[{i}]/div/div/div[2]/div[1]/h2/a"

                attributes["url"]   = self.driver.find_element(By.XPATH, XP_url).get_attribute('href')
                attributes["name"]  = self.driver.find_element(By.XPATH, XP_name).text
                attributes["price"] = self.driver.find_element(By.XPATH, XP_price).text
                attributes["shop"]  = "allegro"

                temp_url = attributes["url"]
                self.driver.execute_script(f"window.open('{temp_url}','_blank');")
                self.handling_cookies()
                self.driver.switch_to.window(self.driver.window_handles[1])
                XP_shop = "/html/body/div[2]/div[6]/div/div/div[6]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/div[1]/div[1]"
                XP_delivery = "/html/body/div[2]/div[6]/div/div/div[6]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[5]/div[1]/div/div/span/span[2]"
                attributes["provider"] = self.driver.find_element(By.XPATH, XP_shop).text.split()[1]
                attributes["delivery"] = self.driver.find_element(By.XPATH, XP_delivery).text
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                products.append(attributes)
            
        return json.dumps(products,indent=2)

if __name__ == "__main__":
    print("ok")
    start_time = time.time()
    shopping_list = []
    for i in range(0, 1):
        shopping_list.append(input(f"Wprowadź nazwe {i+1} produktu: "))
    freeze_support()
    options = Options()
    options.add_argument("--disable-popup-blocking")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    bot = Allegro(driver)
    bot.loading_page()
    output = bot.searching(shopping_list)
    print(output)
    print(time.time()-start_time)