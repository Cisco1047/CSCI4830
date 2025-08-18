from vin import VIN
from vehicle import Vehicle

# For the vehicles since 1980

MAKE_MAP = {
    "Ford Motor Company": "Ford",
    "General Motors LLC": "Chevrolet",
    "Toyota Motor Corporation": "Toyota",
    "Honda Motor Co., Ltd.": "Honda",
    "Volkswagen De Mexico Sa De Cv": "Volkswagen",
    "Toyota Motor Corporation": "Toyota",
    "Lexus": "Lexus",
    "Toyota Motor Mfg Canada Inc": "Toyota",
    "Toyota Motor Mfg USA Inc": "Toyota",
    "Toyota": "Toyota",
    "Nissan Motor Co., Ltd.": "Nissan",
    "Nissan": "Nissan",
    "American Honda Motor Co., Inc.": "Honda",
    "Honda Motor Co., Ltd.": "Honda",
    "Honda": "Honda",
    "General Motors LLC": "GMC",
    "GMC Truck Division": "GMC",
    "GMC": "GMC",
}


def _normalize_make(make: str | None) -> str | None:
    if not make:
        return None
    make = make.strip()
    # exact map first, then fallback to first word (e.g. "Ford Motor Company" -> "Ford")
    return MAKE_MAP.get(make, make.split()[0])

def decode_vin(vin_code: str) -> Vehicle | None:
    vin_code = (vin_code or "").strip().upper()
    try:
        v = VIN(vin_code)
        year_val = getattr(v, "model_year", None)
        model_val = getattr(v, "model", None)
        manuf_val = getattr(v, "manufacturer", None)

        make_clean = _normalize_make(manuf_val)

        return Vehicle(
            vin=vin_code,
            year=year_val,
            make=make_clean,
            model=model_val,
        )
    except Exception as e:
        # keep quiet in production if you prefer; this helps while debugging
        print(f"Failed to decode VIN '{vin_code}': {e}")
        return None
