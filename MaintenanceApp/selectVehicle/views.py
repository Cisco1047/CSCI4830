
# Create your views here.
# vehicles/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Make, CarModel, Vehicle, TaskForConfiguration
from .forms import VehicleForm
from django.contrib import messages
from django.urls import reverse

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
    years = list(range(2026, 1999, -1))
    makes = Make.objects.all().order_by('name')
    return render(request, 'login/index.html', {'years': years,'makes': makes})

def select_vehicle(request):
    if request.method == "POST":
        form = VehicleSelectForm(request.POST, user=request.user)
        if form.is_valid():
            vehicle = form.cleaned_data["vehicle"]
            # Redirect carrying the chosen vehicle id
            url = f"{reverse('repair_options')}?vehicle={vehicle.id}"
            return redirect(url)
        else:
            messages.error(request, "Please select a valid vehicle.")
    else:
        form = VehicleSelectForm(user=request.user)

    return render(request, "repairs/select_vehicle.html", {"form": form})


def _get_vehicle_secure(request):
    """
    Pull vehicle id from querystring and validate that it exists.
    If you have per-user vehicles, also ensure ownership here.
    """
    vid = request.GET.get("vehicle")
    if not vid:
        return None
    try:
        v = Vehicle.objects.select_related(
            "car_configuration",
            "car_configuration__make",
            "car_configuration__car_model",
        ).get(pk=vid)
        # Enforce ownership if your model has an owner/user field:
        if hasattr(Vehicle, "owner"):
            if not request.user.is_authenticated or v.owner_id != request.user.id:
                return None
        return v
    except Vehicle.DoesNotExist:
        return None


def repair_options(request):
    vehicle = _get_vehicle_secure(request)
    if vehicle is None:
        messages.error(request, "Select a vehicle before continuing.")
        return redirect("repair_select_vehicle")

    # Example: filter tasks for this vehicle's configuration
    cfg = vehicle.car_configuration
    tasks = TaskForConfiguration.objects.select_related("task").filter(
        car_configuration=cfg
    ).order_by("task__name")

    # Handle POST from this page (choosing a task, etc.) later
    return render(request, "repairs/repair_options.html", {
        "vehicle": vehicle,
        "tasks": tasks,
    })
