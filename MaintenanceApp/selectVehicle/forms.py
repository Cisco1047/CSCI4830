from django import forms
from .models import Make, CarModel, CarConfiguration, Vehicle


class VehicleForm(forms.ModelForm):
    make = forms.ModelChoiceField(queryset=Make.objects.all(), label="Make")
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.none(), label="Model")
    year = forms.IntegerField(label="Year", min_value=1981, max_value=2025)

    class Meta:
        model = Vehicle
        fields = ['vin', 'make', 'model', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['make'].initial = self.instance.configuration.make
            self.fields['model'].initial = self.instance.configuration.model
            self.fields['year'].initial = self.instance.configuration.year
            self.fields['model'].queryset = CarModel.objects.filter(
                make=self.instance.configuration.make)

        elif 'make' in self.data:
            try:
                make_id = int(self.data.get('make'))
                self.fields['model'].queryset = CarModel.objects.filter(
                    make_id=make_id).order_by('name')
            except (ValueError, TypeError):
                pass
        else:
            self.fields['model'].queryset = CarModel.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        make = cleaned_data.get('make')
        model = cleaned_data.get('model')
        year = cleaned_data.get('year')

        if not all([make, model, year]):
            return cleaned_data

        if model and make and model.make != make:
            self.add_error(
                'model', 'Selected model does not belong to the chosen make.')

        try:
            config = CarConfiguration.objects.get(
                make=make, model=model, year=year)
        except CarConfiguration.DoesNotExist:
            config = CarConfiguration.objects.create(
                make=make, model=model, year=year)

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
