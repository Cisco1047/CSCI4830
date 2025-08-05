from django.shortcuts import render, redirect
from .forms import SearchForm
from django.http import JsonResponse # Import JsonResponse
from selectVehicle.models import Make, CarModel, CarConfiguration, Vehicle, MaintenanceTask,  TaskForConfiguration# Ensure all relevant models are imported
from django.db.models import Q # For complex queries in search_car_configurations
from django.http import HttpResponseRedirect
from vinDecoder import decode_vin

# Create your views here.

# def vehicleSelectionPage(request):
#     form = SearchForm()
#     context = {'form': form}
#     return render(request, 'login/index.html', context)

def searchPage(request):
    return render(request, 'login/search.html')

def resultsPage(request):
    return render(request, 'login/results.html')


def vehicleSelectionPage(request):
    # The form is submitted via GET, so we check request.GET
    form = SearchForm(request.GET or None) # Initialize with GET data or as unbound form

    results = CarConfiguration.objects.none() # Initialize results as empty
    vin_vehicle = None # To hold the Vehicle object if searched by VIN

    if form.is_valid():
        with open('search_log.txt', 'a') as log_file:
            log_file.write(f"Form data: {form.cleaned_data}\n")
        # Cleaned data is available if the form is valid
        make = form.cleaned_data.get('make') # This will be a Make object
        car_model = form.cleaned_data.get('carModel') # This will be a CarModel object
        year = form.cleaned_data.get('year') # This will be an integer or None
        vin = form.cleaned_data.get('vin') # This will be a string or None

        # Build query conditions for CarConfiguration
        query_conditions = Q()

        # if vin:
        #     # If VIN is provided, search by VIN, which should lead to a specific CarConfiguration
        #     try:
        #         vinYear, vinMake, vinModel = decode_vin(vin) # Decode VIN to get year, make, model
        #         make = Make.objects.filter(name=vinMake).first() # Get Make object by name
        #         car_model = CarModel.objects.filter(name=vinModel, make=make).first()
        #         if make and car_model:
        #             # If make and model are found, filter CarConfiguration
        #             results = CarConfiguration.objects.filter(make=make, model=car_model, year=vinYear)
        #         # Find the Vehicle associated with the VIN
        #         vin_vehicle = Vehicle.objects.get(vin=vin)
        #         # Filter CarConfiguration based on the found Vehicle's configuration
        #         # Assuming Vehicle has a ForeignKey to CarConfiguration named 'configuration'
        #         results = CarConfiguration.objects.filter(id=vin_vehicle.configuration.id)
        #     except Vehicle.DoesNotExist:
        #         # If VIN does not exist, no results
        #         results = CarConfiguration.objects.none()
        #         # You might want to add a message here for the user, e.g.:
        #         # from django.contrib import messages
        #         # messages.error(request, "No vehicle found with the provided VIN.")
        # else:
            # If no VIN, filter based on make, model, year for CarConfiguration
        if make:
            # Filter by Make object (ForeignKey)
            query_conditions &= Q(make=make)
        if car_model:
            # Filter by CarModel object (ForeignKey)
            query_conditions &= Q(model=car_model) # Assuming field is 'model' not 'carModel' on CarConfiguration
        if year:
            # Filter by year (integer field)
            query_conditions &= Q(year=year)

        # Apply filters to CarConfiguration
        if query_conditions:
            results = CarConfiguration.objects.filter(query_conditions).values('id')
            if results.exists():
                with open('success_log.txt', 'a') as log_file:
                    log_file.write(f"Results found: {results} {results.count()} for {form.cleaned_data}\n")
                    return redirect('car_config_detail', config_id=results.first()['id'])
                    return render(request, 'login/results.html', {'results': results, 'form': form})
        else:
            # If no VIN and no other criteria, return no results
            results = CarConfiguration.objects.none()
            # from django.contrib import messages
            # messages.info(request, "Please enter search criteria.")

    # Render the template with the form and results
    context = {
        'form': form,
        'results': results,
        'vin_vehicle': vin_vehicle # Pass this if you display VIN details
    }
    # You are rendering the same page, so no redirect needed if results are on the same page.
    # If results are on a separate page (e.g., /results/), you'd redirect.
    # But current template shows results on the same page.
    return render(request, 'login/index.html', context)

def carConfigResultsView(request, config_id):
    try:
        car_config = CarConfiguration.objects.get(id=config_id)
        tasks = TaskForConfiguration.objects.filter(configuration_id=config_id).select_related('task_id') .values('instructions', 'task_id')
        with open('car_config_log.txt', 'a') as log_file:
            log_file.write(f"Car configuration details: {car_config} with tasks {tasks}\n")

        return render(request, 'login/car_config_detail.html', {'car_config': car_config})
    except CarConfiguration.DoesNotExist:
        return render(request, 'login/error.html', {'message': 'Car configuration not found.'})
