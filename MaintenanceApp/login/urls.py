from django.urls import path
from . import views

appname = 'login'

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('login/search.html', views.searchPage, name='search'),
    path('login/results.html', views.resultsPage, name='results')
]