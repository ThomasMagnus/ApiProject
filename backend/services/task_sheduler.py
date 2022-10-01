import asyncio
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from orderList.classes import Sheets, CBRData
import config

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.db import connection


def connect_base():
    sheets = Sheets('/creds.json')
    sheets_values = sheets.get_values()
    usd_course = CBRData(config.CBR_API_URL).converter()

    if sheets.check_changes():
        for x in range(1, len(sheets_values)):
            order_num = int(sheets_values[x][1])
            cost_usd = int(sheets_values[x][2])
            delivery_date = str(sheets_values[x][3])
            sheet_num = int(sheets_values[x][0])
            cost_rub = round((cost_usd * usd_course), 2)
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT upsert_orders({order_num}, {cost_usd}, {cost_rub}, '{delivery_date}', {sheet_num})")
                cursor.fetchall()
        print('База успешно обновлена!')


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(connect_base, 'interval', minutes=config.SHEETS_INTERVAL_POLLING)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        asyncio.get_event_loop().stop()
