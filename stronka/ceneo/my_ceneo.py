import pyshorteners
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from decimal import Decimal

class Ceneo:
    def __init__(self, driver):
        self.driver = driver

    def zwrotlista(self):
        tempList = []
        total_height = int(
            self.driver.execute_script("return document.body.scrollHeight")
        )
        for i in range(1, total_height, 20):
            self.driver.execute_script("window.scrollTo(0, {});".format(i))
        propositionsList = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js_search-results"))
        )
        propositionsCounter = len(propositionsList.find_elements(By.XPATH, "./div"))
        if propositionsCounter > 11:
            propositionsCounter = 11
        if propositionsCounter > 2:
            for i in range(0, propositionsCounter - 2):
                tempList.append(
                    propositionsList.find_element(
                        By.XPATH, f'./div[@data-position="{i}"]/div/div[1]/a/img'
                    ).get_attribute("src")
                )
                tempList.append(
                    propositionsList.find_element(
                        By.XPATH, f'./div[@data-position="{i}"]'
                    ).get_attribute("data-productname")
                )
        else:
            """lement = propositionsList.find_element(
                By.XPATH, f'./div[@data-position="0"]'
            )
            self.driver.execute_script("arguments[0].click()", element)"""
        return tempList, propositionsList

    def wyszukiwanie(self, propositionsList, number):
        if (
            propositionsList.find_element(
                By.XPATH,
                f'./div[@data-position="{number-1}"]/div/div[2]/div[2]/div/a',
            ).text.lower()
            == "idź do sklepu"
        ):
            products = []
            attributes = {}
            attributes["nazwa"] = propositionsList.find_element(
                By.XPATH, f'./div[@data-position="{number-1}"]'
            ).get_attribute("data-productname")
            shop = propositionsList.find_element(
                By.XPATH, f'./div[@data-position="{number-1}"]'
            )
            attributes["cena"] = float(shop.get_attribute("data-price").replace(",", "."))
            attributes["cena_dostawy"] = 0
            attributes["sklep"] = (
                shop.get_attribute("data-shopurl")
                .replace("https://", "", 1)
                .replace("http://", "", 1)
            )
            attributes["img_src"] = shop.find_element(
                By.XPATH, f"./div/div/a/img"
            ).get_attribute("src")
            linkv1 = shop.find_element(By.CLASS_NAME, "go-to-shop").get_attribute(
                "href"
            )
            try:
                attributes["link"] = pyshorteners.Shortener().tinyurl.short(linkv1)
            except:
                pass
            products.append(attributes)
            return products
        else:
            element = propositionsList.find_element(
                By.XPATH, f'./div[@data-position="{number-1}"]/div/div[2]/div[2]/a[1]'
            )
            self.driver.execute_script("arguments[0].click()", element)
            products = self.raporcik()
            return products

    def raporcik(self):
        products = []
        self.driver.get(f'{self.driver.current_url};0280-0.htm')
        try:
            element = self.driver.find_element(By.CLASS_NAME, "show-remaining-offers__trigger")
            self.driver.execute_script("arguments[0].click()", element)
        except selenium.common.exceptions.NoSuchElementException:
            pass
        finally:
            total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
            for i in range(1, total_height, 20):
                self.driver.execute_script("window.scrollTo(0, {});".format(i))
            offersNumber = self.driver.find_element(By.CLASS_NAME, "js_normal-offers")
            propositionsCounter = len(offersNumber.find_elements(By.XPATH, "./li"))
            for number in range(1, propositionsCounter+1):
                attributes = {}
                attributes["nazwa"] = self.driver.find_element(
                    By.CLASS_NAME, "product-top__product-info__name"
                ).text
                if propositionsCounter > 1:
                    shop = offersNumber.find_element(By.XPATH, f"./li[{number}]")
                else:
                    shop = offersNumber.find_element(
                        By.XPATH, f"./li/div/div[1]/div[1]/div[3]"
                    )
                if shop.get_attribute("class") == "product-offers__list__ado-item ado-common":
                    continue
                price = (
                    shop.find_element(By.CLASS_NAME, "value").text
                    + shop.find_element(By.CLASS_NAME, "penny").text
                ).replace(" ","").replace(",", ".")
                attributes["cena"] = float(price)
                element = self.driver.find_element(
                    By.CLASS_NAME, "gallery-carousel__media-container"
                )
                attributes["img_src"] = element.find_element(
                    By.XPATH, "./div/div[1]/a/img"
                ).get_attribute("src")
                shipping = shop.find_element(By.CLASS_NAME, "product-delivery-info")
                deliveryPrice = shipping.text
                if deliveryPrice[:9] != "Z wysyłką":
                    if deliveryPrice.lower() == "szczegóły dostawy":
                        deliveryPrice = 9.00
                    try:
                        pom = shipping.find_element(
                            By.CLASS_NAME, "free-delivery-label"
                        ).text
                        print(pom)
                        if pom.lower() == "darmowa wysyłka":
                            deliveryPrice = 0.00
                    except selenium.common.exceptions.NoSuchElementException:
                        pass
                else:
                    deliveryPrice = float(deliveryPrice[12:19].replace(",", ".")) - float(price)
                print(deliveryPrice)
                attributes["cena_dostawy"] = deliveryPrice
                if propositionsCounter == 1:
                    shop = offersNumber.find_element(By.XPATH, f"./li")
                attributes["sklep"] = (
                    shop.find_element(
                        By.CLASS_NAME, "js_product-offer-link"
                    ).get_attribute("innerHTML")
                ).replace("Dane i opinie o ", "")
                linkv1 = "www.ceneo.pl" + shop.find_element(
                    By.CLASS_NAME, "product-offer__container"
                ).get_attribute("data-click-url")
                try:
                    attributes["link"] = pyshorteners.Shortener().tinyurl.short(linkv1)
                except:
                    pass
                products.append(attributes)
            return products
