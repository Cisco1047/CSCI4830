# CSCI4830 CarPal 

## Project Summary:

Our project is a vehicle maintenance assistant app designed to help everyday car owners perform basic repairs and upkeep themselves—saving time and money. Many simple tasks, like changing a light bulb or tire, seem intimidating without guidance. Our goal is to empower users by walking them through these tasks step-by-step.

The app will allow users to input their car’s year, make, model, or VIN to view a list of DIY repair and maintenance guides tailored to their vehicle.

We plan to implement the platform using a Django frontend with a Python backend supported by SQL and API calls.

Challenges include limited access to manufacturer repair data, development costs, and the overwhelming variety of vehicle types. Since many automakers restrict repair information, we may need to build our own database from scratch and initially focus on a select group of U.S. vehicles.

### note summary from chatgpt taken from project proposal will rewrite later in my own words - Cisco

---

## Features:

- Accepts a 17-character VIN string
- Validates the VIN using the `vin` Python library
- Extracts:
  - Year
  - Manufacturer (Make)
  - Model
- Returns results in a structured `Vehicle` object
- Easily convertible to JSON for frontend/API use

---

## Frontend:




---

## Backend: 

- vehicle.py stores the vehicle information the users selects. 
- vinDecode.py decodes a VIN if the user enters the vin as a vehicle selection. 


