from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stronka.ceneo.my_ceneo import Ceneo


def ceneo_scrapper(list):
    listy_propozycji = {}
    produkty = []   
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(executable_path="/code/stronka/ceneo/chromedriver", options=options)
    
    driver.maximize_window()
    bot = Ceneo(driver)
    pierwszy = True
    for elem in list:
        if not pierwszy:
            driver.execute_script("window.open('');")
            driver.switch_to.window(
                driver.window_handles[len(driver.window_handles) - 1]
            )
            driver.get(
                f"https://www.ceneo.pl/Zabawki;szukaj-{elem.replace(' ', '+')};0112-0.htm"
            )
        else:
            driver.get(
                f"https://www.ceneo.pl/Zabawki;szukaj-{elem.replace(' ', '+')};0112-0.htm"
            )
            pierwszy = False
    for i in range(0, len(list)):
        xd = []
        driver.switch_to.window(driver.window_handles[i])
        xd, lista_propozycji = bot.zwrotlista()
        if xd != []:
            lista_numer = []
            for j in range(0, len(xd)):
                lista_numer.append(f"num{str(j)}")
            zipped = dict(zip(lista_numer, xd))
            listy_propozycji[f"{list[i]}"] = zipped
        else:
            tab = bot.wyszukiwanie(lista_propozycji, 1)
            for i, slownik in enumerate(tab):
                slownik["ID"] = len(produkty) + i
            produkty.extend(tab)
    return produkty, listy_propozycji
