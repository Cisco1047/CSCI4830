from django.shortcuts import render

# Create your views here.

def vehicleSelectionPage(request):
    years = list(range(2026, 1999, -1))
    return render(request, 'login/index.html', {'years': years})

def searchPage(request):
    return render(request, 'login/search.html')

def resultsPage(request):
    return render(request, 'login/results.html')

def repair_options_view(request):
    return render(request, 'login/repairOptions.html')


