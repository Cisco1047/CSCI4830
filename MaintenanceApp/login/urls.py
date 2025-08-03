from django.urls import path
from . import views

appname = 'login'

urlpatterns = [
    path('login/', views.vehicleSelectionPage, name='vehicle_selection'),
    path('login/search', views.searchPage, name='search'),
    path('login/results', views.resultsPage, name='results'),
    path('login/repair-options/', views.repair_options_view, name='repairOptions')

]