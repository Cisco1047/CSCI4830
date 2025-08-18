# selectVehicle/vin_utils.py
import re
from vin import VIN

VIN_RE = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$', re.I)  # no I/O/Q

def validate_vin(vin_code: str) -> bool:
    return bool(VIN_RE.fullmatch((vin_code or "").strip()))

def decode_vin_dict(vin_code: str) -> dict | None:
    """
    Return a dict with {vin, year, make, model} using the 'vin' package,
    or None if decoding fails.
    """
    try:
        v = VIN(vin_code.strip().upper())
        return {
            "vin": vin_code.strip().upper(),
            "year": v.model_year,
            "make": (v.manufacturer or "").strip(),
            "model": (getattr(v, "model", "") or "").strip(),
        }
    except Exception:
        return None
