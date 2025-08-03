# vehicles/urls.py
from django.urls import path
from . import views

app_name = 'selectVehicle'

urlpatterns = [
    path('create/', views.create_vehicle, name='create_vehicle'),

    path('ajax/get-models/', views.get_models, name='get_models'),

    path('search/', views.searchView, name='search_view'),

]
