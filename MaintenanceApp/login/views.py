from django.shortcuts import render

# Create your views here.


def searchPage(request):
    return render(request, 'login/search.html')


def resultsPage(request):
    return render(request, 'login/results.html')


def repair_options_view(request):
    return render(request, 'login/repairOptions.html')


