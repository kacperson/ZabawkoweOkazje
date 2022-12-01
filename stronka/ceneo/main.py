from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from multiprocessing import freeze_support
from ceneo import Ceneo
import time
if __name__ == '__main__':
    start_time = time.time()
    lista_zakupow = []
    for i in range(0, 1):
        lista_zakupow.append(input(f"Wprowadź nazwe {i+1} produktu: "))
    freeze_support()
    options = Options()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    bot = Ceneo(driver)
    bot.odpalenie_strony()
    for elem in lista_zakupow:
        print(elem)
        bot.wyszukiwanie(elem)
    print(time.time()-start_time)