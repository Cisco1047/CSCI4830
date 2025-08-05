from vin import VIN
from vehicle import Vehicle

# For the vehicles since 1980
def decode_vin(vin_code):
    try:
        vin = VIN(vin_code)
        return vin.model_year, vin.manufacturer, vin.model
    
    except Exception as e:
        print(f"Failed to decode VIN: {e}")
        return None

if __name__ == "__main__":
    vin_code = "JTJBT20X460101850"  # Example VIN
    year, make, model = decode_vin(vin_code)
    if year and make and model:
        print(f"Year: {year}, Make: {make}, Model: {model}")
    else:
        print("Invalid VIN or unable to decode.")