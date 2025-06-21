from django.shortcuts import render
from .models import Announcement

# Create your views here.
def announcements_list(request):
    announcements = Announcement.objects.all().order_by('-date')
    return render(request, 'announcements/announcements_list.html', {'announcements': announcements})

def announcement_page(request, slug):
    announcement = Announcement.objects.get(slug=slug)
    return render(request, 'announcements/announcement_page.html', {'announcement': announcement})