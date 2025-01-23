import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Данные для доступа к Google Таблице
SERVICE_ACCOUNT_FILE = 'creds.json'
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = '1Xxf3oXGmUoTYYM1aLr1h7G8qAZPzdInoxzOSy6NNLvw'

# Функция для авторизации в Google Таблицах
async def get_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    return sheet


