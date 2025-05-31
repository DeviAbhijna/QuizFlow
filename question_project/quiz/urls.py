from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('questions/', views.show_questions, name='show_questions'),
    path('mod-history/', views.modification_history, name='modification_history'),
]
