
# Create your views here.
# vehicles/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Make, CarModel
from .forms import VehicleForm, SearchForm


def searchView(request):
    form = SearchForm()
    context = {'form': form}
    return render(request, 'vehicles/searchForm.html', context)

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = VehicleForm()

    return render(request, 'vehicles/create_vehicle.html', {'form': form})


def get_models(request):
    make_id = request.GET.get('make_id')
    models = CarModel.objects.filter(make_id=make_id).order_by('name')
    model_list = [{'id': model.id, 'name': model.name} for model in models]
    return JsonResponse(model_list, safe=False)
