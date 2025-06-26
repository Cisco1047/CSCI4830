from django.shortcuts import render

# Create your views here.
def loginPage(request):
    return render(request, 'login/signin.html')

def searchPage(request):
    return render(request, 'login/search.html')

def resultsPage(request):
    return render(request, 'login/results.html')