from bot.settings import *
from abc import ABC
import os
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd


class Tools(ABC):
    def __init__(self, webdriver, url) -> None:
        self.webdriver = webdriver
        self.url = url
        try:
            sheets = os.path.join(os.getcwd(), 'sheets')
            if not os.path.exists(sheets):
                os.mkdir(sheets)
        except:
            pass
        self.create_sheets()

    def open_url(self, url):
        return self.webdriver.get(url)
         
    def find(self, locator):
        return self.webdriver.find_element(*locator)

    def finds(self, locator):
        return self.webdriver.find_elements(*locator)

    def click_in_element(self, locator, t):
        WebDriverWait(self.webdriver, t).until(EC.presence_of_element_located(locator))
        self.find(locator).click()
    
    def create_list(self, tag):
        req = self.webdriver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        tags = soup.find_all(tag)
        lista = []
        for t in tags:
            lista.append(t.text.strip())
            lista = list(filter(('').__ne__, lista))
        return lista

    def split_list(self, list, num):
        splited_list = []
        a = int(len(list) / num)
        len_l = len(list)
        for i in range(a):
            start = int(i*len_l/a)
            end = int((i+1)*len_l/a)
            splited_list.append(list[start:end])
        return splited_list

    def split_list2(self, list, num):
        """
        Recebe uma lista e a divide em partes de acordo com num.
        Se a divisao da lista pela qtd de elementos(num) nao for exata,
        se for maior em 1 elemento, entao esse elemento é retirado,
        se for mais do que 1, sera acrecentado zeros ate dar a qtd de elementos
        para uma divisao exata.

        Args:
            list (list): lista a ser dividida
            num (integer): numero com quantidade de partes a ser dividida

        Returns:
            list: lista
        """
        splited_list = []
        a = int(len(list) / num)
        b = int(len(list) % num)
        if b == 1:
            len_l = len(list[:-1])
        else:
            while b != 0:
                list.append('0')
                b = int(len(list) % num)
                len_l = len(list)
                a = int(len(list) / num)
            len_l = len(list)
        for i in range(a):
            start = int(i * len_l / a)
            #print("start ", start)
            end = int((i+1) * len_l/a)
            #print(end)
            splited_list.append(list[start:end])
            #print(len(splited_list))
        return splited_list

    def create_sheets(self):
        sheets = os.path.join(os.getcwd(), 'sheets')

        df = pd.DataFrame(columns=COLS.get("cols"))
        path = os.path.join(sheets, 'tabela_meta.xlsx')
        df.to_excel(path, index=False)

        df1 = pd.DataFrame(columns=COLS.get("cols"))
        path = os.path.join(sheets, 'tabela_amazon.xlsx')
        df1.to_excel(path, index=False)

        df2 = pd.DataFrame(columns=COLS.get("cols"))
        path = os.path.join(sheets, 'tabela_apple.xlsx')
        df2.to_excel(path, index=False)

        df3 = pd.DataFrame(columns=COLS.get("cols"))
        path = os.path.join(sheets, 'tabela_netflix.xlsx')
        df3.to_excel(path, index=False)

        df4 = pd.DataFrame(columns=COLS.get("cols"))
        path = os.path.join(sheets, 'tabela_google.xlsx')
        df4.to_excel(path, index=False)
        
class Config():
    def __init__(self) -> None:
        self.s = Service(ChromeDriverManager().install())  
        self.opt = ChromeOptions()
        self.ua = UserAgent()
        self.ua_agent = self.ua.random
        
        prefs = {
            "download.default_directory" : os.getcwd() ,         
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1, 
            "safebrowsing.disable_download_protection": True,
            }
        self.opt.add_argument(f'--user-agent={self.ua_agent}')
        self.opt.add_experimental_option("excludeSwitches", ["enable-logging"])        
        self.opt.add_experimental_option("prefs", prefs)
        self.opt.add_argument('--kiosk-printing')
        self.opt.add_argument("--start-maximized") 
        self.opt.add_argument("--disable-infobars") 