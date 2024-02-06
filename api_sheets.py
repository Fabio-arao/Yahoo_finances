import pandas as pd
from bot.settings import *
import gspread, os
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from dotenv import load_dotenv
load_dotenv()



class Api_sheets():
    def __init__(self, key) -> None:
        print_log(f"[INFO] Iniciando a subida da planilha {key} para google sheets")
        scopes = ['https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive']

        credentials = Credentials.from_service_account_file(os.path.join('key_yahoo.json'), scopes=scopes)
        gc = gspread.authorize(credentials)
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)

        gs = gc.open_by_key(self.get_key(key))
        worksheet1 = gs.worksheet('Sheet1')

        sheets = os.path.join(os.getcwd(), 'sheets')
        path = os.path.join(sheets, f'tabela_{key}.xlsx')
        df = pd.read_excel(path)

        worksheet1.clear()
        set_with_dataframe(worksheet=worksheet1, dataframe=df, include_index=False,
        include_column_header=True, resize=True)
        print_log(f"[INFO] Planilha {key} upada para google sheets")
    
    def get_key(self, key):
        if key == 'amazon':
            return os.environ['SHEET_AMAZON']
        elif key == 'apple':
            return os.environ['SHEET_APPLE']
        elif key == 'meta':
             return os.environ['SHEET_META']
        elif key == 'netflix':
            return os.environ['SHEET_NETFLIX']
        else:
            return os.environ['SHEET_GOOGLE']
       
       
       