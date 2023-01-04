import json

import pyshorteners
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Ceneo:
    #mydict = {}

    def __init__(self, driver):
        self.driver = driver

    def odpalenie_strony(self):
        self.driver.get("https://www.ceneo.pl/Zabawki")

    def zwrocenie_listy(self, items):
        id = 0
        mydict = {}
        for item in items:
            id = id + 1
            products = []
            wyszukiwarka = self.driver.find_element(By.ID, "form-head-search-q")
            wyszukiwarka.clear()
            wyszukiwarka.send_keys(item)
            wyszukiwarka.send_keys(Keys.ENTER)
            url = self.driver.current_url
            if url.find("OneClickSearch") == -1:
                #print("PRODUKT NIEJEDNOZNACZNY WYBIERZ")
                lista = []
                element = self.driver.find_element(By.CLASS_NAME, "dropdown-wrapper")
                self.driver.execute_script("arguments[0].click()", element)
                #element = self.driver.find_element(By.XPATH,
                 #                                  '//*[@id="body"]/div/div/div[3]/div/section/div[2]/div[2]/div/div/a[2]')
                self.driver.execute_script("arguments[0].click()", element)
                self.driver.implicitly_wait(1)  # seconds
                lista_propozycji = self.driver.find_element(By.CLASS_NAME, "js_search-results")
                ilosc = len(lista_propozycji.find_elements(By.XPATH, './div'))

                if ilosc > 11:
                    ilosc = 11
                for i in range(0, ilosc - 1):
                    #print(f'{i + 1}. ',
                     #     lista_propozycji.find_element(By.XPATH, f'./div[@data-position="{i}"]').get_attribute(
                      #        'data-productname'))
                    lista.append(lista_propozycji.find_element(By.XPATH, f'./div[@data-position="{i}"]').get_attribute(
                        'data-productname'))
                    #mydict[i] = lista_propozycji.find_element(By.XPATH, f'./div[@data-position="{i}"]').get_attribute('data-productname')
                return lista

    def wyszukiwanie(self, items, number):
        id = 0
        for item in items:
            id = id + 1
            products = []
            wyszukiwarka = self.driver.find_element(By.ID, "form-head-search-q")
            wyszukiwarka.clear()
            wyszukiwarka.send_keys(item)
            wyszukiwarka.send_keys(Keys.ENTER)
            url = self.driver.current_url
            if url.find("OneClickSearch") == -1:
                #print("PRODUKT NIEJEDNOZNACZNY WYBIERZ")
                lista = []
                element = self.driver.find_element(By.CLASS_NAME, "dropdown-wrapper")
                #self.driver.execute_script("arguments[0].click()", element)
                #element = self.driver.find_element(By.XPATH, '//*[@id="body"]/div/div/div[3]/div/section/div[2]/div[2]/div/div/a[2]')
                self.driver.execute_script("arguments[0].click()", element)
                self.driver.implicitly_wait(10)  # seconds
                lista_propozycji = self.driver.find_element(By.CLASS_NAME, "js_search-results")
                ilosc = len(lista_propozycji.find_elements(By.XPATH, './div'))

                if ilosc > 11:
                    ilosc = 11
                for i in range (0, ilosc-1):

                    lista.append(lista_propozycji.find_element(By.XPATH, f'./div[@data-position="{i}"]').get_attribute('data-productname'))
                ##
                    if lista_propozycji.find_element(By.XPATH,
                                                     f'./div[@data-position="{i}"]/div/div[2]/div[2]/div[1]/a[1]').text.lower() == 'idź do sklepu':
                        attributes = {"id": i + 1}
                        attributes["nazwa"] = lista_propozycji.find_element(By.XPATH,
                                                                            f'./div[@data-position="{i}"]').get_attribute(
                            'data-productname')
                        sklep = lista_propozycji.find_element(By.XPATH, f'./div[@data-position="{i}"]')
                        attributes["cena"] = float(sklep.get_attribute('data-price').replace(',', '.'))
                        attributes["cena dostawy"] = "BRAK INFORMACJI"
                        attributes["sklep"] = sklep.get_attribute('data-shopurl').replace('https://', '', 1).replace(
                            'http://', '', 1)
                        linkv1 = sklep.find_element(By.CLASS_NAME, 'go-to-shop').get_attribute('href')
                        try:
                            attributes["link"] = pyshorteners.Shortener().tinyurl.short(linkv1)
                        except:
                            pass
                        products.append(attributes)
                    else:
                        element = lista_propozycji.find_element(By.XPATH,
                                                                f'./div[@data-position="{i}"]/div/div[2]/div[2]/a[1]')
                        self.driver.execute_script("arguments[0].click()", element)
                        products.append(self.raporcik(ajdi=i))
            else:
                products.append(self.raporcik(ajdi=id))
        print(products)
        return products


    def raporcik(self, ajdi):
        attributes = {"id": ajdi}
        attributes["nazwa"] = self.driver.find_element(By.CLASS_NAME, 'product-top__product-info__name').text
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "product-offers-actions")))
        self.driver.execute_script("arguments[0].click()", element)
        element2 = element.find_element(By.XPATH, './div[1]/div/a[1]')
        self.driver.execute_script("arguments[0].click()", element2)
        sklepy = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, "product-offers__list")))
        ilosc_ofert = self.driver.find_element(By.CLASS_NAME, 'js_prevent-middle-button-click').text
        ilosc_ofert = int(ilosc_ofert[8:9])
        if ilosc_ofert == 1:
            sklep = self.driver
        else:
            sklep = sklepy.find_element(By.XPATH, './li[1]')
        cena = sklep.find_element(By.CLASS_NAME, "value").text + sklep.find_element(By.CLASS_NAME, "penny").text
        cena = float(cena.replace(',', '.'))
        attributes["cena"] = cena
        dostawa = sklep.find_element(By.CLASS_NAME, "product-delivery-info")
        cena_dostawy = dostawa.text
        if cena_dostawy[:9] != "Z wysyłką":
            if cena_dostawy.lower() == "szczegóły dostawy":
                cena_dostawy = 9.00
            try:
                pom = dostawa.find_element(By.CLASS_NAME, "free-delivery-label").text
                if pom.lower() == "darmowa wysyłka":
                    cena_dostawy = 0.00
            except selenium.common.exceptions.NoSuchElementException:
                pass
        else:
            cena_dostawy = round(float(cena_dostawy[12:19].replace(',', '.')) - cena, 3)
        attributes["cena dostawy"] = cena_dostawy
        attributes["sklep"] = sklep.find_element(By.CLASS_NAME, "product-offer__container").get_attribute('data-shopurl')
        linkv1 = sklep.find_element(By.CLASS_NAME, 'go-to-shop').get_attribute('href')
        try:
            attributes["link"] = pyshorteners.Shortener().tinyurl.short(linkv1)
        except:
            pass
        return attributes
