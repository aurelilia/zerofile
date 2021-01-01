from django.urls import path

from . import views

app_name = 'streamer'
urlpatterns = [
    path('', views.stream, name='stream'),
    path('<stream_id>/', views.receive, name='receive'),
]
