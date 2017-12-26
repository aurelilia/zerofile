from django.urls import path
from . import views

app_name = "manager"
urlpatterns = [
    path('files/', views.viewfiles, name='viewfiles'),
    path('register/', views.register, name='register')
]
