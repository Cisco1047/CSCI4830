import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from selectVehicle.models import Make, CarModel, MaintenanceTask, CarConfiguration, TaskForConfiguration
from vinDecoder import decode_vin

# Create your views here.


def searchPage(request):
    return render(request, 'login/search.html')

def resultsPage(request):
    """
    Handles the search query from the index page by vehicle configuration
    and renders the repair options with the filtered tasks.
    """
    VIN_RE = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$', re.I)
    vin = (request.GET.get('vin') or '').strip().upper()
    make_id = request.GET.get('make_id')
    year = request.GET.get('year')
    model_id = request.GET.get('model_id')

    vin = (request.GET.get('vin') or '').strip().upper()
    if vin and not VIN_RE.fullmatch(vin):
        messages.error(request, "VIN must be 17 characters and cannot contain I, O, or Q.")
        return redirect(reverse("selectVehicle:vehicle_selection"))

    found_car_config = None

    # --- VIN path ---
    if vin:
        if not VIN_RE.fullmatch(vin):
            messages.error(request, "VIN must be 17 characters and cannot contain I, O, or Q.")
            return redirect(reverse("selectVehicle:vehicle_selection"))

        decoded = decode_vin(vin)  # returns your Vehicle helper (vin, year, make, model)
        if not decoded:
            messages.error(request, "We couldn't decode that VIN. Try again or use Year/Make/Model.")
            return redirect(reverse("selectVehicle:vehicle_selection"))

        # Map decoded make/model to DB (case-insensitive)
        make = Make.objects.filter(name__iexact=(decoded.make or "")).first()
        model = None
        if make:
            model = CarModel.objects.filter(make=make, name__iexact=(decoded.model or "")).first()

        if not (make and model and decoded.year):
            messages.warning(
                request,
                f"Decoded VIN as {decoded.year} {decoded.make} {decoded.model}, "
                "but we don’t have an exact match in the database yet. Please select Year/Make/Model."
            )
            return redirect(reverse("selectVehicle:vehicle_selection"))

        # Locate the configuration; field on CarConfiguration is 'model' (model_id), per your current code
        found_car_config = (
            CarConfiguration.objects
            .filter(year=int(decoded.year), make_id=make.id, model_id=model.id)
            .first()
        )

        if not found_car_config:
            messages.warning(
                request,
                f"We decoded your VIN as {decoded.year} {decoded.make} {decoded.model}, "
                "but don't have that configuration yet."
            )
            return render(request, 'login/repairOptions.html', {
                'task_for_configs': [],
                'search_query': "for your vehicle",
                'cfg': None,
                'qs': request.META.get("QUERY_STRING", ""),
            })

    # --- Year/Make/Model path (original behavior) ---
    elif make_id and year and model_id:
        found_car_config = CarConfiguration.objects.filter(
            make_id=make_id, year=year, model_id=model_id
        ).first()
    # --- No valid input ---
    else:
        messages.error(request, "Please select a Year, Make, and Model, or enter a valid VIN.")
        return redirect(reverse("selectVehicle:vehicle_selection"))

    # Fetch tasks for that configuration (your existing relation)
    task_for_configs = []
    if found_car_config:
        task_for_configs = (
            TaskForConfiguration.objects
            .filter(configuration=found_car_config)
            .select_related('task')
            .order_by('task__name')
        )

    context = {
        'task_for_configs': task_for_configs,
        'search_query': (
            f"for {found_car_config.year} {found_car_config.make.name} {found_car_config.model.name}"
            if found_car_config else "for your vehicle"
        ),
        'cfg': found_car_config,
        'qs': request.META.get("QUERY_STRING", ""),  # preserve selection for back-links
    }

    return render(request, 'login/repairOptions.html', context)

def repair_options_view(request):
    # This view can be used for other purposes if needed.
    return render(request, 'login/repairOptions.html')


def get_models_by_make(request):
    """
    Returns a JSON list of vehicle models for a given make_id and year.
    This is used by the fetch call in index.html to populate the dropdown.
    """
    from django.http import JsonResponse
    make_id = request.GET.get('make_id')
    year = request.GET.get('year')

    if not make_id or not year:
        return JsonResponse([], safe=False)

    try:
        model_ids = (
            CarConfiguration.objects
            .filter(make_id=make_id, year=year)
            .values_list('model_id', flat=True)
            .distinct()
        )
        models = (
            CarModel.objects
            .filter(id__in=model_ids)
            .order_by('name')
            .values('id', 'name')
        )
        return JsonResponse(list(models), safe=False)
    except Exception as e:
        print(f"Error fetching models: {e}")
        return JsonResponse([], safe=False)
    

def task_detail(request, task_id):
    # Use get_object_or_404 to get the task or raise a 404 error if it doesn't exist
    task = get_object_or_404(MaintenanceTask, pk=task_id)
    context = {
        'task': task
    }
    return render(request, 'login/task_detail.html', {'task': task})