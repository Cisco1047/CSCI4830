# vehicles/urls.py
from django.urls import path
from . import views

app_name = 'selectVehicle'

urlpatterns = [
    path('', views.vehicle_selection_view, name='vehicle_selection'),
    path('create/', views.create_vehicle, name='create_vehicle'),
    path('get-models/', views.get_models, name='get_models'),
    path("repair/task/<int:tfc_id>/", views.task_detail, name="task_detail"),


]
