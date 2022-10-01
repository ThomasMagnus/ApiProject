from .models import Delivery

from pprint import pprint
from django.http import HttpResponse
from django.shortcuts import render
from orderList.classes import Sheets


def connect(request):
    return render(request=request, template_name='index.html')


def sheets_work(request):
    sheets = Sheets('/services/creds.json')
    values = sheets.get_values()
    pprint(values)
    return HttpResponse("Запрос успешно отработан")


def check_changes(request):
    sheets = Sheets('/creds.json')
    print(sheets.check_changes())
    return HttpResponse("Запрос успешно отработан")
