from django import forms
from selectVehicle.models import Make, CarModel, CarConfiguration, Vehicle

# class SearchForm(forms.Form):
#     make = forms.ModelChoiceField(queryset=CarConfiguration.objects.all(), required=True, label="Make")
#     carModel = forms.ModelChoiceField(queryset=CarConfiguration.objects.all(), required=True, label="Model")
#     year = forms.IntegerField(required=False, label="Year", min_value=1981, max_value=2025)


# class SearchForm(forms.Form):
#     # Use ModelChoiceField to select from Make and CarModel objects
#     make = forms.ModelChoiceField(
#         queryset=Make.objects.all().order_by('name'), # Order for better UX
#         required=False, # Make optional for broader searches
#         label="Make",
#         empty_label="-- Select Make --" # Optional: add a default empty option
#     )
#     carModel = forms.ModelChoiceField(
#         queryset=CarModel.objects.all().order_by('name'), # Order for better UX
#         required=False, # Make optional
#         label="Model",
#         empty_label="-- Select Model --" # Optional
#     )
#     year = forms.IntegerField(
#         required=False,
#         label="Year",
#         min_value=1981, # You can adjust this range
#         max_value=2025 # Or even dynamically get max(CarConfiguration.objects.values_list('year', flat=True))
#     )
#     # Add a field for VIN if you want to search by VIN directly
#     vin = forms.CharField(max_length=17, required=False, label="VIN Number")

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Dynamically filter model choices based on initial make, if any.
    #     # This is for initial form rendering, for dynamic filtering in the browser,
    #     # you'll need JavaScript (AJAX).
    #     if 'make' in self.initial and self.initial['make']:
    #         self.fields['carModel'].queryset = CarModel.objects.filter(
    #             make=self.initial['make']
    #         ).order_by('name')
    #     elif self.data and 'make' in self.data and self.data['make']:
    #         try:
    #             selected_make_id = int(self.data['make'])
    #             self.fields['carModel'].queryset = CarModel.objects.filter(
    #                 make_id=selected_make_id
    #             ).order_by('name')
    #         except (ValueError, TypeError):
    #             # Handle cases where make might not be a valid ID
    #             self.fields['carModel'].queryset = CarModel.objects.none()
    #     else:
    #         # If no make is selected or provided, initially show no models or all models.
    #         # Showing none is better for cascading dropdowns until a make is chosen.
    #         self.fields['carModel'].queryset = CarModel.objects.none()

class SearchForm(forms.Form):
    # Retrieve all distinct years from CarConfiguration or specify a range
    YEAR_CHOICES = []
    # If you want to get years dynamically from CarConfiguration:
    distinct_years = CarConfiguration.objects.values_list('year', flat=True).distinct().order_by('year')
    for year in distinct_years:
        YEAR_CHOICES.append((year, str(year)))

    # Add an empty option at the top for better UX
    YEAR_CHOICES.insert(0, ('', 'Year'))

    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False, # Make it optional for searching
        # widget=forms.Select(attrs={'id': 'id_year_input'}) # Ensure ID matches JS if you keep custom dropdown
    )

    # Use ModelChoiceField to get all Makes
    make = forms.ModelChoiceField(
        queryset=Make.objects.all().order_by('name'), # Get all makes, ordered by name
        empty_label="Make", # Display this as the first option
        required=False,
        # widget=forms.Select(attrs={'id': 'id_make_select'}) # Ensure ID matches JS if you keep custom dropdown
    )

    # Use ModelChoiceField to get all CarModels
    carModel = forms.ModelChoiceField(
        queryset=CarModel.objects.all().order_by('name'), # Get all models, ordered by name
        empty_label="Model", # Display this as the first option
        required=False,
        # widget=forms.Select(attrs={'id': 'id_carModel_select'}) # Ensure ID matches JS if you keep custom dropdown
    )

    vin = forms.CharField(
        max_length=17,
        required=False,
        label="Vin Number",
        # widget=forms.TextInput(attrs={'id': 'id_vin_input'}) # Ensure ID matches JS if you keep custom dropdown
    )

    # You can add custom validation if you need specific error messages
    # def clean(self):
    #     cleaned_data = super().clean()
    #     year = cleaned_data.get('year')
    #     make = cleaned_data.get('make')
    #     car_model = cleaned_data.get('carModel')
    #     vin = cleaned_data.get('vin')

    #     # Example: Ensure at least one search criterion is provided
    #     if not (year or make or car_model or vin):
    #         raise forms.ValidationError(
    #             "Please provide at least one search criterion (Year, Make, Model, or VIN)."
    #         )
        
    #     return cleaned_data