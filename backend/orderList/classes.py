import os
from pprint import pprint

import httplib2

from services import config

import requests
import xml.etree.ElementTree as ET
from rest_framework.response import Response
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


# Конвертируем полученные данные в XML
class XMLConverter:
    def __init__(self, data):
        self.data = data

    def convert_xml(self):
        xml_data = ET.XML(self.data)
        return xml_data


# Получаем текуций курс доллара
class CBRData:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        get_data = requests.get(self.url).content
        return get_data

    # Возвращаем текущий курс доллара
    def converter(self):
        data = XMLConverter(self.get_data()).convert_xml().findall('./Valute')
        for item in data:
            if item.find('CharCode').text == 'USD':
                return float(item.find('Value').text.replace(',', '.'))


class Sheets:
    def __init__(self, creds_json):
        self._creds_json = os.getcwd() + creds_json
        self._creds_service = ServiceAccountCredentials.from_json_keyfile_name(self._creds_json, config.SCOPED)
        self._http_auth = self._creds_service.authorize(httplib2.Http())
        self._drive_build = build('drive', 'v3', self._http_auth)
        self._sheets_build = build('sheets', 'v4', self._http_auth)

    # Получаем данные из таблицы
    def get_values(self):
        values = self._sheets_build.spreadsheets().values().get(
            spreadsheetId=config.SPREAD_SHEET_ID,
            range=f'{config.START_COLUMN}:{config.END_COLUMN}',
            majorDimension='ROWS'
        ).execute()
        return values.get('values', False)

    # Отлавливаем изменения в таблице
    def check_changes(self, start_change_id=None):
        if config.CHANGES_CONFIG['start_page_config'] is None:
            config.CHANGES_CONFIG['start_page_config'] = self._drive_build.changes().getStartPageToken().execute() \
                .get('startPageToken')
        start_page_token = config.CHANGES_CONFIG['start_page_config']
        write_changes = False
        print(f'Now change token: {start_page_token}')

        while True:
            try:
                param = dict()
                if start_change_id:
                    param['startChangeId'] = start_change_id
                if start_page_token:
                    param['pageToken'] = start_page_token
                changes = self._drive_build.changes().list(**param).execute()

                for change in changes.get('changes'):
                    if change.get('fileId') == config.SPREAD_SHEET_ID:
                        pprint(f'Changes: {change}')
                        print(f'Next change token: {start_page_token}')
                        config.CHANGES_CONFIG['start_page_config'] = changes.get('newStartPageToken')

                next_page_token = changes.get('nextPageToken')

                if not next_page_token:
                    break
            except Exception as error:
                print('An error occurred: %s' % repr(error))
                break

        if config.CHANGES_CONFIG['start_page_config'] != start_page_token:
            write_changes = True

        return write_changes
