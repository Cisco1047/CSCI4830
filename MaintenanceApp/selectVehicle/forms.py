from django import forms
from .models import Make, CarModel, CarConfiguration, Vehicle


class VehicleForm(forms.ModelForm):
    make = forms.CharField(label="Make", max_length=100)
    model = forms.CharField(label="Model", max_length=100)
    year = forms.IntegerField(label="Year", min_value=1981, max_value=2025)

    class Meta:
        model = Vehicle
        fields = ['vin', 'make', 'model', 'year']
        widgets = {'vin': forms.TextInput(attrs={'required': False})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vin'].required = False

        # Set up a text input with a datalist for make
        self.fields['make'].widget = forms.TextInput(attrs={'list': 'make-list'})
        
        # Set up a text input with a datalist for model
        self.fields['model'].widget = forms.TextInput(attrs={'list': 'model-list'})
        
    def clean(self):
        cleaned_data = super().clean()

        make_name = cleaned_data.get('make')
        model_name = cleaned_data.get('model')
        year = cleaned_data.get('year')

        if not all([make_name, model_name, year]):
            return cleaned_data

        # Find or create the Make instance
        make, created = Make.objects.get_or_create(name__iexact=make_name, defaults={'name': make_name})
        cleaned_data['make_instance'] = make

        # Find or create the CarModel instance
        model, created = CarModel.objects.get_or_create(make=make, name__iexact=model_name, defaults={'name': model_name})
        cleaned_data['model_instance'] = model

        # Find or create the CarConfiguration instance
        config, created = CarConfiguration.objects.get_or_create(
            make=make, model=model, year=year
        )
        cleaned_data['configuration'] = config
        return cleaned_data

    def save(self, commit=True):
        vehicle = super().save(commit=False)
        vehicle.configuration = self.cleaned_data['configuration']
        if commit:
            vehicle.save()
        return vehicle



        

# class SearchForm(forms.Form):
#     make = forms.ModelChoiceField(queryset=CarConfiguration.objects.all(), required=True, label="Make")
#     carModel = forms.ModelChoiceField(queryset=CarConfiguration.objects.all(), required=True, label="Model")
#     year = forms.IntegerField(required=False, label="Year", min_value=1981, max_value=2025)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['make'].queryset = Make.objects.all()
#         self.fields['carModel'].queryset = CarModel.objects.all()

#         # if 'make' in self.data and self.data.get('make'):
#         #     try:
#         #         make_id = int(self.data.get('make'))
#         #         self.fields['model'].queryset = CarModel.objects.filter(make_id=make_id).order_by('name')
#         #     except (ValueError, TypeError):
#         #         self.fields['model'].queryset = CarModel.objects.none()
#         # else:
#         #     self.fields['model'].queryset = CarModel.objects.none()



class SearchForm(forms.Form):
    make = forms.ModelChoiceField(
        queryset=Make.objects.filter(
            id__in=CarConfiguration.objects.values_list('make', flat=True).distinct()
        ),
        required=True,
        label="Make"
    )
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.none(),
        required=True,
        label="Model"
    )
    year = forms.IntegerField(required=False, label="Year", min_value=1981, max_value=2025)

    class VehicleSelectForm(forms.Form):
        vehicle = forms.ModelChoiceField(
            queryset=Vehicle.objects.none(),
            empty_label="— Select your vehicle —",
            widget=forms.Select(attrs={"class": "form-select"})  # optional styling
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'make' in self.data:
            try:
                make_id = int(self.data.get('make'))
                self.fields['model'].queryset = CarModel.objects.filter(
                    make_id=make_id,
                    id__in=CarConfiguration.objects.filter(make_id=make_id).values_list('model', flat=True).distinct()
                ).order_by('name')
            except (ValueError, TypeError):
                self.fields['model'].queryset = CarModel.objects.none()
        elif self.initial.get('make'):
            make_id = self.initial.get('make').id if hasattr(self.initial.get('make'), 'id') else self.initial.get('make')
            self.fields['model'].queryset = CarModel.objects.filter(
                make_id=make_id,
                id__in=CarConfiguration.objects.filter(make_id=make_id).values_list('model', flat=True).distinct()
            ).order_by('name')
        else:
            self.fields['model'].queryset = CarModel.objects.none()
