from flask import jsonify
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from multiprocessing import freeze_support
from .my_ceneo import Ceneo
import time



def ceneo_scrapper(list):
    start_time = time.time()
    lista_zakupow = []
    for i in range(0, 1):
        lista_zakupow.append(list)
    freeze_support()
    options = Options()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    bot = Ceneo(driver)
    bot.odpalenie_strony()
    output = bot.wyszukiwanie(lista_zakupow, 1)
    print(output)
    print(time.time()-start_time)
    return output
