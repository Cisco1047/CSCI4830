# CSCI4830 CarPal 

## Project Summary:

Our project is a vehicle maintenance assistant app designed to help everyday car owners perform basic repairs and upkeep themselves—saving time and money. Many simple tasks, like changing a light bulb or tire, seem intimidating without guidance. Our goal is to empower users by walking them through these tasks step-by-step.

The app will allow users to input their car’s year, make, model, or VIN to view a list of DIY repair and maintenance guides tailored to their vehicle.

We plan to implement the platform using a Django frontend with a Python backend supported by SQL and API calls.

Challenges include limited access to manufacturer repair data, development costs, and the overwhelming variety of vehicle types. Since many automakers restrict repair information, we may need to build our own database from scratch and initially focus on a select group of U.S. vehicles.

---
## Technology

- Python 3.12
- HTML, CSS
- Django 5.2
- Pillow
- SQLite
- pytest + Selenium

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


### Vehicle search
- Cascading **Year → Make → Model** (models filtered by selected make & year).
- **VIN** entry supported (17 chars; client-side uppercasing; excludes I/O/Q).
- **Client-side validation**: user must provide **VIN** _or_ complete **Year + Make + Model**.  
  Missing dropdowns glow red and submission is blocked.

### Repair options
- Shows available maintenance tasks for the chosen vehicle configuration.

### Task detail / Instructions
- Step-by-step instructions are stored in DB (JSON) and rendered cleanly.
- The view accepts multiple instruction shapes, including:
  - `[{ "step": 1, "title": "…", "instruction": "…" }, ...]`
  - `[{ "n": 1, "text": "…" }, ...]`
  - `["Turn off engine", "Open hood", ...]` (list of strings)
  - JSON string or plain newline-separated text
- Odd characters from copy/paste are normalized (e.g., en-dash, apostrophe).

### UI polish
- “Search” + “Add a Vehicle” buttons are side-by-side with spacing.
- Sticky footer on all screen sizes.
- Results page preserves the user’s query string when navigating back.

### Testing
- **pytest + Selenium** cover the selector flow (dropdown interactions, etc.).

---

## Backend: 

- vehicle.py stores the vehicle information the users selects. 
- vinDecode.py decodes a VIN if the user enters the vin as a vehicle selection.

---

## Release Notes

### 1.0 — Highlights

- **New:** Added a **Repair Options** page where users choose the task they want to perform after selecting a vehicle.
- **Improved UI:** Polished the **Home** and **Vehicle Search** pages (clearer layout, better button placement).
- **Refined vehicle selection:**
  - Cascading **Year → Make → Model** flow.
  - Optional **VIN** search.
  - Models are now fetched from the DB for the selected **make + year**, preventing mismatches (e.g., no more “Ford Accord”).
- **Data integration:** The frontend now queries the database for available **makes/models** rather than relying on static lists.
- **Testing:** Added more comprehensive **Selenium** tests (run via **pytest**) focused on the dropdown workflow on the Year → Make → Model page.


