from django.urls import path
from . import views as login_views
from selectVehicle import views as vehicle_views


appname = 'login'

urlpatterns = [
    path('login/search', login_views.searchPage, name='search'),
    path('login/results', login_views.resultsPage, name='results'),
    path('login/repair-options/', login_views.repair_options_view, name='repairOptions'),
    path('vehicles/', vehicle_views.vehicle_selection_view, name='vehicle_selection')

]
