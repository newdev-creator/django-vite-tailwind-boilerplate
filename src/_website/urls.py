from django.urls import path
from . import views

app_name = "_website"

urlpatterns = [
    path('', views.index, name="website__index"),
]