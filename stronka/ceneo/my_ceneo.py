import pyshorteners
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Ceneo:
    def __init__(self, driver):
        self.driver = driver

    def zwrotlista(self):
        xd = []
        total_height = int(
            self.driver.execute_script("return document.body.scrollHeight")
        )
        for i in range(1, total_height, 20):
            self.driver.execute_script("window.scrollTo(0, {});".format(i))
        lista_propozycji = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js_search-results"))
        )
        ilosc = len(lista_propozycji.find_elements(By.XPATH, "./div"))
        if ilosc > 11:
            ilosc = 11
        if ilosc > 2:
            for i in range(0, ilosc - 1):
                xd.append(
                    lista_propozycji.find_element(
                        By.XPATH, f'./div[@data-position="{i}"]/div/div[1]/a/img'
                    ).get_attribute("src")
                )
                xd.append(
                    lista_propozycji.find_element(
                        By.XPATH, f'./div[@data-position="{i}"]'
                    ).get_attribute("data-productname")
                )
        else:
            element = lista_propozycji.find_element(
                By.XPATH, f'./div[@data-position="0"]'
            )
            self.driver.execute_script("arguments[0].click()", element)
        return xd, lista_propozycji

    def wyszukiwanie(self, lista_propozycji, numer):
        if (
            lista_propozycji.find_element(
                By.XPATH,
                f'./div[@data-position="{numer-1}"]/div/div[2]/div[2]/div[1]/a[1]',
            ).text.lower()
            == "idź do sklepu"
        ):
            attributes = {}
            attributes["nazwa"] = lista_propozycji.find_element(
                By.XPATH, f'./div[@data-position="{numer-1}"]'
            ).get_attribute("data-productname")
            sklep = lista_propozycji.find_element(
                By.XPATH, f'./div[@data-position="{numer-1}"]'
            )
            attributes["cena"] = float(
                sklep.get_attribute("data-price").replace(",", ".")
            )
            attributes["cena dostawy"] = "BRAK INFORMACJI"
            attributes["sklep"] = (
                sklep.get_attribute("data-shopurl")
                .replace("https://", "", 1)
                .replace("http://", "", 1)
            )
            attributes["img_src"] = sklep.find_element(
                By.XPATH, f"./div/div/a/img"
            ).get_attribute("src")
            linkv1 = sklep.find_element(By.CLASS_NAME, "go-to-shop").get_attribute(
                "href"
            )
            try:
                attributes["link"] = pyshorteners.Shortener().tinyurl.short(linkv1)
            except:
                pass
            return attributes
        else:
            element = lista_propozycji.find_element(
                By.XPATH, f'./div[@data-position="{numer-1}"]/div/div[2]/div[2]/a[1]'
            )
            self.driver.execute_script("arguments[0].click()", element)
            products = self.raporcik()
            return products

    def raporcik(self):
        products = []
        """total_height = int(self.driver.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 20):
            self.driver.execute_script("window.scrollTo(0, {});".format(i))"""
        ilosc_ofert = self.driver.find_element(By.CLASS_NAME, "js_normal-offers")
        ilosc = len(ilosc_ofert.find_elements(By.XPATH, "./li"))
        for numerek in range(1, ilosc + 1):
            attributes = {}
            attributes["nazwa"] = self.driver.find_element(
                By.CLASS_NAME, "product-top__product-info__name"
            ).text
            if ilosc > 1:
                sklep = ilosc_ofert.find_element(By.XPATH, f"./li[{numerek}]")
            else:
                sklep = ilosc_ofert.find_element(
                    By.XPATH, f"./li/div/div[1]/div[1]/div[3]"
                )
            cena = (
                sklep.find_element(By.CLASS_NAME, "value").text
                + sklep.find_element(By.CLASS_NAME, "penny").text
            )
            cena = float(cena.replace(",", "."))
            attributes["cena"] = cena
            element = self.driver.find_element(
                By.CLASS_NAME, "gallery-carousel__media-container"
            )
            attributes["img_src"] = element.find_element(
                By.XPATH, "./div/div[1]/a/img"
            ).get_attribute("src")
            dostawa = sklep.find_element(By.CLASS_NAME, "product-delivery-info")
            cena_dostawy = dostawa.text
            if cena_dostawy[:9] != "Z wysyłką":
                if cena_dostawy.lower() == "szczegóły dostawy":
                    cena_dostawy = 9.00
                try:
                    pom = dostawa.find_element(
                        By.CLASS_NAME, "free-delivery-label"
                    ).text
                    if pom.lower() == "darmowa wysyłka":
                        cena_dostawy = 0.00
                except selenium.common.exceptions.NoSuchElementException:
                    pass
            else:
                cena_dostawy = round(
                    float(cena_dostawy[12:19].replace(",", ".")) - cena, 3
                )
            attributes["cena dostawy"] = cena_dostawy
            if ilosc == 1:
                sklep = ilosc_ofert.find_element(By.XPATH, f"./li")
            attributes["sklep"] = (
                sklep.find_element(
                    By.CLASS_NAME, "js_product-offer-link"
                ).get_attribute("innerHTML")
            ).replace("Dane i opinie o ", "")
            linkv1 = "www.ceneo.pl" + sklep.find_element(
                By.CLASS_NAME, "product-offer__container"
            ).get_attribute("data-click-url")
            try:
                attributes["link"] = pyshorteners.Shortener().tinyurl.short(linkv1)
            except:
                pass
            products.append(attributes)
        return products
