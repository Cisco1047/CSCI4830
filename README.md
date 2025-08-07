# CSCI4830 CarPal 

## Project Summary:

Our project is a vehicle maintenance assistant app designed to help everyday car owners perform basic repairs and upkeep themselves—saving time and money. Many simple tasks, like changing a light bulb or tire, seem intimidating without guidance. Our goal is to empower users by walking them through these tasks step-by-step.

The app will allow users to input their car’s year, make, model, or VIN to view a list of DIY repair and maintenance guides tailored to their vehicle.

We plan to implement the platform using a Django frontend with a Python backend supported by SQL and API calls.

Challenges include limited access to manufacturer repair data, development costs, and the overwhelming variety of vehicle types. Since many automakers restrict repair information, we may need to build our own database from scratch and initially focus on a select group of U.S. vehicles.

---
## Technology

- Python 3
- HTML
- Django
- Pillow

---

## How to use

- Install Django and Pillow.
- Host code on local machine.
- Generate secret key for settings.py
- In the terminal change directory to where the source code is saved ex. (C:\Users\Cisco\OneDrive\Documents\GitHub\CSCI4830\Carpal) please take note       that you must be inside the Carpal folder.
- Now if on windows type this command "py manage.py runserver"
- Now you can click on the generated link from the host server or you can go to "http://localhost:8000/" in your web browser. 

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

- Home page
- Login page
- Repair search page
- Results page

---

## Backend: 

- vehicle.py stores the vehicle information the users selects. 
- vinDecode.py decodes a VIN if the user enters the vin as a vehicle selection.

---

## Release Notes

Release 0.3 - In this release we have improved the UI for the home page and search page. We also added another page for choosing the repair option that the user wants to do. We also refined the ability to select the year,model,make or vin of the car you would like to search for. We connected the database to the frontend by querying the database for the make and model store in it and implemented JavaScript so make it so that the Make of the vehicle selected aligns with the model, not more Ford Accord. Additional we added more comprehensive test implementing Selenium test that work using pytest and focus on dropdown selection, specifically on the page where users pick Year>Make>Model. 

