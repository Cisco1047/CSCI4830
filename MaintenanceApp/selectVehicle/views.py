
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
    else:
        form = VehicleForm()

    return render(request, 'vehicles/create_vehicle.html', {'form': form})


def get_models(request):
    make_id = request.GET.get('make_id')
    if make_id:
        models = CarModel.objects.filter(make_id=make_id).order_by('name')
        print(f"Requested make_id: {make_id}, Found models: {[m.name for m in models]}")
        model_list = [{'id': m.id, 'name': m.name} for m in models]
        return JsonResponse(model_list, safe=False)
    print(f"No make_id provided. make_id={make_id}")
    return JsonResponse([], safe=False)


def vehicle_selection_view(request):
    makes = Make.objects.all().order_by('name')
    return render(request, 'vehicles/index.html', {'makes': makes})
