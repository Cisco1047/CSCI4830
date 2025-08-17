
# Create your views here.
# vehicles/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Make, CarModel, Vehicle, TaskForConfiguration
from .forms import VehicleForm
from django.contrib import messages
from django.urls import reverse

# Fix odd characters that appear in your stored JSON
REPLACEMENTS = {
    "û": "–",   # en dash
    "Æ": "’",   # apostrophe
    "╛": "¼",   # fraction (or change to 'quarter')
}


def _clean_text(s: str) -> str:
    if not isinstance(s, str):
        return s
    for bad, good in REPLACEMENTS.items():
        s = s.replace(bad, good)
    return s


def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            form = VehicleForm() 
    else:
        form = VehicleForm()
    
    makes = Make.objects.all().order_by('name')
    context = {
        'form': form,
        'makes': makes,
    }
    return render(request, 'vehicles/create_vehicle.html', context)


def get_models(request):
    make_id = request.GET.get('make_id')
    year = request.GET.get('year')

    if not make_id or not year:
        return JsonResponse([], safe=False)

    models_qs = (
        CarModel.objects
        .filter(carconfiguration__make_id=make_id,
                carconfiguration__year=year)
        .distinct()
        .order_by('name')
    )

    model_list = [{"id": m.id, "name": m.name} for m in models_qs]
    return JsonResponse(model_list, safe=False)


def vehicle_selection_view(request):
    years = list(range(2026, 1999, -1))
    makes = Make.objects.all().order_by('name')
    return render(request, 'login/index.html', {'years': years, 'makes': makes})


def get_instructions_panel(request, tfc_id: int):
    tfc = get_object_or_404(TaskForConfiguration, pk=tfc_id)

    raw = tfc.instructions or []

    steps = []
    if isinstance(raw, list):
        for item in raw:
            steps.append({
                "n": item.get("step"),
                "title": _clean_text(item.get("title", "")),
                "text": _clean_text(item.get("instruction", "")),
            })
    else:
        steps = []

    context = {
        "tfc": tfc,
        "task_name": getattr(getattr(tfc, "maintenance_task", None), "name", "Task"),
        "steps": steps,
    }
    return render(request, "repair/_instructions_panel.html", context)


def task_detail(request, tfc_id: int):
    tfc = get_object_or_404(TaskForConfiguration, pk=tfc_id)
    task = getattr(tfc, "task", None) or getattr(tfc, "maintenance_task", None)

    raw = tfc.instructions or []
    steps = []
    if isinstance(raw, list):
        for item in raw:
            steps.append({
                "n": item.get("step"),
                "title": _clean_text(item.get("title", "")),
                "text": _clean_text(item.get("instruction", "")),
            })

    qs = request.META.get("QUERY_STRING", "")
    if qs:
        back_url = f"{reverse('login:results')}?{qs}"
    else:
        cfg = getattr(tfc, "car_configuration", None)
        if cfg:
            back_url = (
                f"{reverse('login:results')}"
                f"?year={cfg.year}&make_id={cfg.make_id}&model_id={cfg.car_model_id}"
            )
        else:
            back_url = reverse('login:results')

    return render(request, "login/task_detail.html", {
        "task": task,
        "steps": steps,
        "back_url": back_url,
    })
