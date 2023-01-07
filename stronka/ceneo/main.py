from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stronka.ceneo.my_ceneo import Ceneo


def ceneo_scrapper(list):
    produkty = []
    options = Options()
    driver = webdriver.Chrome(executable_path="D:\chromedriver.exe",options=options)
    driver.maximize_window()
    bot = Ceneo(driver)
    pierwszy = True
    for elem in list:
        if not pierwszy:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
            driver.get(f"https://www.ceneo.pl/Zabawki;szukaj-{elem.replace(' ', '+')};0112-0.htm")
        else:
            driver.get(f"https://www.ceneo.pl/Zabawki;szukaj-{elem.replace(' ', '+')};0112-0.htm")
            pierwszy = False
    for i in range(0, len(list)):
        xd = []
        driver.switch_to.window(driver.window_handles[i])
        xd, lista_propozycji = bot.zwrotlista()
        if xd != []:
            num = int(input('Dawej liczbe'))
            tab = bot.wyszukiwanie(lista_propozycji, num)
            for i, slownik in enumerate(tab):
                slownik['ID'] = len(produkty) + i
            produkty.extend(tab)
        else:
            tab = bot.raporcik()
            for i, slownik in enumerate(tab):
                slownik['ID'] = len(produkty) + i
            produkty.extend(tab)
    return produkty