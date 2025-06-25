from vin import VIN
from vehicle import Vehicle

# For the vehicles since 1980
def decode_vin(vin_code):
    try:
        vin = VIN(vin_code)

        return Vehicle(
            vin=vin_code,
            year=vin.model_year,
            make=vin.manufacturer,
            model=vin.model
        )
    except Exception as e:
        print(f"Failed to decode VIN: {e}")
        return None
