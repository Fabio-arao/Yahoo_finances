from tools.tools import Tools
from time import sleep
from api_sheets import Api_sheets
from bot.settings import *
from bot.locators import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import os

class Yahoo(Tools):
    def collect(self):
        for key, url in URLS.items():
            print_log(f"[INFO] Coletando infos de {key}")
            self.open_url(url) 
            element = WebDriverWait(self.webdriver, 1).until(EC.visibility_of_element_located(L_YAHOO))
            time = 0
            while time != 20:
                self.webdriver.execute_script("arguments[0].scrollIntoView();", element)
                time +=1
            sleep(4)
            td = self.create_list('td')
            self.remove_data_broken(td)
            td_data = self.split_list2(td, 7)
            self.collect_data(td_data, key)
            self.api = Api_sheets(key)

    def collect_data(self, list, key):
        sheets = os.path.join(os.getcwd(), 'sheets')
        path = os.path.join(sheets, f'tabela_{key}.xlsx')
        df = pd.read_excel(path)
        for i in list:
            try:
                if 'Dividend' in i[1]:
                    print_log("[INFO] Passei a linha quebrada!")
                else:
                    date = i[0]
                    open = float(i[1])
                    high = float(i[2])
                    low = float(i[3])
                    close = float(i[4])
                    ad_close = float(i[5])
                    volume = float(i[6].replace(",", "." , 1).replace(",", ""))
                    df.loc[int(len(df) + 1)] = date, open, high, low, close, ad_close, volume
            except Exception as e:
                print_log(e)
                pass
        df.to_excel(path, index=False)

    def remove_data_broken(self, td):
            index_remove = []
            for i, value in enumerate(td):
                if 'Dividend' in value:
                    index_remove.extend([i, i-1])
            print(index_remove)
            for index in sorted(index_remove, reverse=True):
                del td[index]
