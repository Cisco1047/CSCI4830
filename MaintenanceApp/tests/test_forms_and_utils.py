import pytest
from django.urls import reverse
from django.db.models import Count
from selectVehicle.forms import VehicleForm
from selectVehicle.vin_utils import validate_vin, decode_vin_dict
from selectVehicle.models import Make, CarModel, CarConfiguration, Vehicle

@pytest.mark.django_db
def test_vehicle_form_valid_data():
    """Test that the VehicleForm is valid with correct data."""
    form_data = {
        'vin': '1234567890ABCDEFG',
        'make': 'Toyota',
        'model': 'Camry',
        'year': 2020
    }
    form = VehicleForm(data=form_data)
    assert form.is_valid()
    vehicle = form.save()
    assert Vehicle.objects.filter(vin='1234567890ABCDEFG').exists()

@pytest.mark.django_db
def test_vehicle_form_creates_new_instances():
    """Test that the form correctly creates new Make, CarModel, and CarConfiguration instances."""
    initial_make_count = Make.objects.count()
    initial_model_count = CarModel.objects.count()
    initial_config_count = CarConfiguration.objects.count()

    form_data = {
        'vin': '1ABCDE2345FG67890',
        'make': 'Ford',
        'model': 'Escape',
        'year': 2021
    }
    form = VehicleForm(data=form_data)
    form.is_valid()
    form.save()

    assert Make.objects.count() == initial_make_count + 1
    assert CarModel.objects.count() == initial_model_count + 1
    assert CarConfiguration.objects.count() == initial_config_count + 1

@pytest.mark.parametrize("vin_code, expected", [
    ('1ABCDE2345FG67890', True),
    ('1abcde2345fg67890', True),
    ('1A B C D E 2345FG67890', False),
    ('1ABCDE2345FG6789', False),
    ('1ABCDE2345FG6789O', False),
    ('1ABCDE2345FG6789I', False),
])
def test_validate_vin(vin_code, expected):
    """Test the VIN validation utility function."""
    assert validate_vin(vin_code) == expected

def test_decode_vin_dict_valid_vin(mocker):
    """Test the VIN decoding utility with a mocked external library."""
    mock_vin_obj = mocker.Mock()
    mock_vin_obj.model_year = 2022
    mock_vin_obj.manufacturer = 'Honda'
    mock_vin_obj.model = 'Civic'
    mocker.patch('selectVehicle.vin_utils.VIN', return_value=mock_vin_obj)

    decoded = decode_vin_dict('19XPC2A1X3G123456')
    assert decoded['year'] == 2022
    assert decoded['make'] == 'Honda'
    assert decoded['model'] == 'Civic'