from django.contrib import admin
from .models import Make, CarModel, CarConfiguration, Vehicle, MaintenanceTask, TaskForConfiguration, ServiceRecord

admin.site.register(Make)
admin.site.register(CarModel)
admin.site.register(CarConfiguration)
admin.site.register(Vehicle)
admin.site.register(MaintenanceTask)
admin.site.register(TaskForConfiguration)
admin.site.register(ServiceRecord)
