from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from selectVehicle.models import Make, CarModel, MaintenanceTask, CarConfiguration, TaskForConfiguration

# Create your views here.


def searchPage(request):
    return render(request, 'login/search.html')

def resultsPage(request):
    """
    Handles the search query from the index page by vehicle configuration
    and renders the repair options with the filtered tasks.
    """
    make_id = request.GET.get('make_id')
    year = request.GET.get('year')
    model_id = request.GET.get('model_id')
    vin = request.GET.get('vin')
    
    task_for_configs = []
    found_car_config = None

    try:
        if vin:
            found_car_config = CarConfiguration.objects.get(vin=vin)
        elif make_id and year and model_id:
            found_car_config = CarConfiguration.objects.get(make_id=make_id, year=year, model_id=model_id)
    except CarConfiguration.DoesNotExist:
        pass
    except Exception as e:
        print(f"Error finding car configuration: {e}")

    if found_car_config:
        # Get the TaskForConfiguration objects, which contain the ID for the link
        task_for_configs = TaskForConfiguration.objects.filter(configuration=found_car_config).order_by('task__name')

    context = {
        'task_for_configs': task_for_configs,
        'search_query': f"for {found_car_config.year} {found_car_config.make.name} {found_car_config.model.name}" if found_car_config else "for your vehicle"
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
    make_id = request.GET.get('make_id')
    year = request.GET.get('year')
    
    # Debug print statement to see what values are being received
    print(f"Received make_id: {make_id}, year: {year}")

    if not make_id or not year:
        # Return an empty list if either parameter is missing
        return JsonResponse([], safe=False)

    try:
        model_ids = CarConfiguration.objects.filter(make_id=make_id, year=year).values_list('model_id', flat=True).distinct()
        # Step 2: Get the actual CarModel objects using the IDs
        models = CarModel.objects.filter(id__in=model_ids).order_by('name').values('id', 'name')
        # Filter VehicleModel objects by make_id and check if the year is contained in the 'years' field
        # models = CarModel.objects.filter(make_id=make_id).order_by('name').values('id', 'name')
        return JsonResponse(list(models), safe=False)
    except Exception as e:
        # Catch any exceptions during the database query and return an empty list
        print(f"Error fetching models: {e}")
        return JsonResponse([], safe=False)
    

def task_detail(request, task_id):
    # Use get_object_or_404 to get the task or raise a 404 error if it doesn't exist
    task = get_object_or_404(MaintenanceTask, pk=task_id)
    context = {
        'task': task
    }
    return render(request, 'login/task_detail.html', context)