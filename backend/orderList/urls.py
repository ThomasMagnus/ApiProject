from django.urls import path
from . import views

urlpatterns = [
    path('', views.connect),
    path('sheetsWork/', views.sheets_work),
    path('checkChanges/', views.check_changes),
]
