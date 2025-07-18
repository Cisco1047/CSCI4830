from django.shortcuts import render

# Create your views here.

def vehicleSelectionPage(request):
    return render(request, 'login/index.html')

def searchPage(request):
    return render(request, 'login/search.html')

def resultsPage(request):
    return render(request, 'login/results.html')

