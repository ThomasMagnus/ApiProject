import os
from datetime import date

SECRET_KEY = 'django-insecure-+ra1z#)b_^t-us#v(j-71+qu_17tnfsp#c)nt7#@$_gf3rt)u8'

CREDENTIALS_FILE = os.getcwd() + '/creds.json'
SPREAD_SHEET_ID = '1ujBFRRNDkuEounQoW3BlY9W5t1gFukTBJiX0GMQRRTw'
EMAIL_ADDR = ['project@testproject-363918.iam.gserviceaccount.com', 'emmagomedov@gmail.com']
TRACKED_SHEET_NAME = 'OrderList'
SCOPED = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CBR_API_URL = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.today().strftime("%d/%m/%Y")}'

START_COLUMN = 'A'
END_COLUMN = 'D'

CHANGES_CONFIG = {
    'start_page_config': None
}

CBR_INTERVAL_POLLING = 1
SHEETS_INTERVAL_POLLING = 5
