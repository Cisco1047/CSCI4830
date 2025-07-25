from django.urls import path
from . import views

appname = 'login'

urlpatterns = [
    path('login/', views.vehicleSelectionPage, name='vehicle_selection'),
    path('login/search.html', views.searchPage, name='search'),
    path('login/results.html', views.resultsPage, name='results')
]