from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    # Paths for your main app pages
    path('search/', views.searchPage, name='search'),
    path('results/', views.resultsPage, name='results'),
    path('repair-options/', views.repair_options_view, name='repair_options'),
    
    # Path for the AJAX call to get models based on make and year
    path('vehicles/get-models/', views.get_models_by_make, name='get_models_by_make'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]