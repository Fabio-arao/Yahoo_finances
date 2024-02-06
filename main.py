from bot.settings import *
from bot.bot import Yahoo
from selenium.webdriver import Chrome
from tools.tools import Config



class Aplication():
    def __init__(self, ini=1, max=10) -> None:
        self.ini = ini
        self.max = max
        self.run_bot()
        
    def execute_bot(self):
        self.config = Config()
        self.webdriver = Chrome(service=self.config.s, options=self.config.opt)
        self.url = URLS.get("META")
        self.bot = Yahoo(self.webdriver, self.url) 
        
    def run_bot(self):
        try:
            print_log(f'[INFO] Executando bot pela {self.ini}° vez!')
            while self.ini < self.max:
                self.execute_bot()
                self.bot.collect() 
                break
        except:    
            self.webdriver.quit()      
            self.ini += 1
            if self.ini <= self.max:                
                self.run_bot()
            else:                
                print_log("[EXCEPT] Houve um erro no Bot")
                # ENVIAR EMAIL PARA NOTIFICAR

if __name__ == "__main__":
    setup_log()
    Aplication()
    exit()