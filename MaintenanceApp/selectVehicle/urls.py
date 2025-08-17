# vehicles/urls.py
from django.urls import path
from . import views

app_name = 'selectVehicle'

urlpatterns = [
    path('create/', views.create_vehicle, name='create_vehicle'),
    # path('select/', views.vehicle_selection_view, name='vehicle_selection'),
    path('', views.vehicle_selection_view, name='vehicle_selection'),
    path('get-models/', views.get_models, name='get_models'),
    # path('ajax/get-models/', views.get_models, name='get_models'),
    path('vehicle-selection/', views.vehicle_selection_view, name='vehicle_selection'),
    path("repair/select/", views.select_vehicle, name="repair_select_vehicle"),
    path("repair/options/", views.repair_options, name="repair_options")
]
