from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stronka.ceneo.my_ceneo import Ceneo


def ceneo_scrapper(list):
    propositionsDict = {}
    products = []   
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = Options()
    options.add_argument("--headless")
    WINDOW_SIZE = "1920,1080"
    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(executable_path="/code/stronka/ceneo/chromedriver", options=options)
    
    driver.maximize_window()
    bot = Ceneo(driver)
    isFirst = True
    for element in list:
        if not isFirst:
            driver.execute_script("window.open('');")
            driver.switch_to.window(
                driver.window_handles[len(driver.window_handles) - 1]
            )
            driver.get(
                f"https://www.ceneo.pl/Zabawki;szukaj-{element.replace(' ', '+')};0112-0.htm"
            )
        else:
            driver.get(
                f"https://www.ceneo.pl/Zabawki;szukaj-{element.replace(' ', '+')};0112-0.htm"
            )
            isFirst = False
    for i in range(0, len(list)):
        tempList = []
        driver.switch_to.window(driver.window_handles[i])
        tempList, propositionsList = bot.zwrotlista()
        if tempList != []:
            numbersList = []
            for j in range(0, len(tempList)):
                numbersList.append(f"num{str(j)}")
            zipped = dict(zip(numbersList, tempList))
            propositionsDict[f"{list[i]}"] = zipped
        else:
            resultsTable = bot.wyszukiwanie(propositionsList, 1)
            for i, tempDict in enumerate(resultsTable):
                tempDict["ID"] = len(products) + i
            products.extend(resultsTable)
    return products, propositionsDict
