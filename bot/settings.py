import logging, os

URLS = {'meta': 'https://finance.yahoo.com/quote/META/history?p=META',
        'amazon': 'https://finance.yahoo.com/quote/AMZO34.SA/history?p=AMZO34.SA',
        'netflix':'https://finance.yahoo.com/quote/NFLX/history?p=NFLX',
        'google': 'https://finance.yahoo.com/quote/GOOG/history?p=GOOG',
        'apple': 'https://finance.yahoo.com/quote/AAPL/history?p=AAPL',}

C= ['Date',	
    'Open',	
    'High',	
    'Low',
    'Close*',
    'Adj Close**',
    'Volume']

COLS= {'cols': C}

def print_log(msg):
    print(msg)
    logging.info(msg)  


def setup_log():
    s = os.path.join(os.getcwd())
    path = os.path.join(s, 'Crawler_yahoo.log')
    logging.basicConfig(
    filename = path,
    level = logging.INFO, 
    filemode='w', 
    format = "%(asctime)s :: %(message)s",
    datefmt = '%d-%m-%Y %H:%M:%S')