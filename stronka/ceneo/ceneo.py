import pyshorteners
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Ceneo:
    def __init__(self, driver):
        self.driver = driver

    def odpalenie_strony(self):
        self.driver.get("https://www.ceneo.pl")

    def wyszukiwanie(self, itemek):
        wyszukiwarka = self.driver.find_element(By.ID, "form-head-search-q")
        wyszukiwarka.clear()
        wyszukiwarka.send_keys(itemek)
        wyszukiwarka.send_keys(Keys.ENTER)
        url = self.driver.current_url
        if url.find("OneClickSearch") == -1:
            if len(self.driver.find_elements(By.ID, "searchInAllCategoriesBtn"))>0:
                element = self.driver.find_element(By.ID, "searchInAllCategoriesBtn")
                if element.is_displayed():
                    element = self.driver.find_element(By.ID, "searchInAllCategoriesBtn")
                    self.driver.execute_script("arguments[0].click()", element)
                    element = self.driver.find_element(By.CLASS_NAME, "header-search__button")
                    self.driver.execute_script("arguments[0].click()", element)
            print("PRODUKT NIEJEDNOZNACZNY WYBIERZ")
            lista = []
            element = self.driver.find_element(By.CLASS_NAME, "dropdown-wrapper")
            self.driver.execute_script("arguments[0].click()", element)
            element = self.driver.find_element(By.XPATH, '//*[@id="body"]/div/div/div[3]/div/section/div[2]/div[2]/div/div/a[2]')
            self.driver.execute_script("arguments[0].click()", element)
            self.driver.implicitly_wait(1)  # seconds
            lista_propozycji = self.driver.find_element(By.CLASS_NAME, "js_products-list-main")
            ilosc = len(lista_propozycji.find_elements(By.XPATH, './div'))
            print(ilosc)
            if ilosc > 12:
                ilosc = 12
            for i in range (0, ilosc-2):
                print(lista_propozycji.find_element(By.XPATH, f'./div[@data-position="{i}"]').get_attribute('data-productname'))
                lista.append(lista_propozycji.find_element(By.XPATH, f'./div[@data-position="{i}"]').get_attribute('data-productname'))
            numer = int(input(f"Wybierz produkt od 1-{ilosc-2}: "))
            element = lista_propozycji.find_element(By.XPATH, f'./div[@data-position="{numer-1}"]')
            self.driver.execute_script("arguments[0].click()", element)
            self.raporcik()
        else:
            self.raporcik()


    def raporcik(self):
        element = self.driver.find_element(By.CLASS_NAME, "dropdown-wrapper")
        self.driver.execute_script("arguments[0].click()", element)
        element2 = element.find_element(By.XPATH, './div/a[3]')
        self.driver.execute_script("arguments[0].click()", element2)
        with open('somefile.txt', 'w', encoding="utf-8") as the_file:
            the_file.write(self.driver.page_source)
        #sklepy = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "product-offers__list")))
        sklep = self.driver.find_element(By.XPATH, '//div[@data-position="1"]')
        podstawa = sklep.find_element(By.CLASS_NAME, "value").text
        grosze =  sklep.find_element(By.CLASS_NAME, "penny").text
        cena = podstawa+grosze
        nazwa_sklepu = sklep.find_element(By.CLASS_NAME, "product-offer__container").get_attribute('data-shopurl')
        linkv1 = sklep.find_element(By.CLASS_NAME, 'go-to-shop').get_attribute('href')
        try:
            link = pyshorteners.Shortener().tinyurl.short(linkv1)
        except:
            pass
        print(cena)
        print(nazwa_sklepu)
        print(link)