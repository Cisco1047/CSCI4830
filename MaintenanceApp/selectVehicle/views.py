
# Create your views here.
# vehicles/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Make, CarModel
from .forms import VehicleForm

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            form = VehicleForm() 
    else:
        form = VehicleForm()
    
    makes = Make.objects.all().order_by('name')
    context = {
        'form': form,
        'makes': makes,
    }
    return render(request, 'vehicles/create_vehicle.html', context)

def get_models(request):
    make_name = request.GET.get('make_name')
    model_list = []
    if make_name:
        try:
            make = Make.objects.get(name__iexact=make_name)
            models = CarModel.objects.filter(make=make).order_by('name')
            model_list = [{'name': m.name} for m in models]
        except Make.DoesNotExist:
            pass
    return JsonResponse(model_list, safe=False)

def vehicle_selection_view(request):
    years = list(range(2026, 1999, -1))
    makes = Make.objects.all().order_by('name')
    return render(request, 'login/index.html', {'years': years,'makes': makes})


