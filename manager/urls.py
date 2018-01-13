from django.urls import path
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

app_name = 'manager'
urlpatterns = [
    path('files/', views.viewfiles, name='viewfiles'),
    path('register/', CreateView.as_view(template_name='manager/register.html', form_class=UserCreationForm, success_url='/' ), name='register'),
]
