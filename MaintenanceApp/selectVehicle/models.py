from django.db import models

# Create your models here.


class Make(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('make', 'name')

    def __str__(self):
        return self.name


class CarConfiguration(models.Model):
    """
    Represents a unique make, model, and year combination.
    This is the central point for tasks.
    """
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('make', 'model', 'year')
        ordering = ['make__name', 'model__name', 'year']

    def __str__(self):
        return f"{self.year} {self.make.name} {self.model.name}"


class Vehicle(models.Model):
    vin = models.CharField(max_length=17, unique=True)
    configuration = models.ForeignKey(
        CarConfiguration, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.configuration} ({self.vin})"


class MaintenanceTask(models.Model):
    """
    Represents a type of task that can be performed (e.g., Oil Change, Wiper Change).
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TaskForConfiguration(models.Model):
    """
    Links a MaintenanceTask to a specific CarConfiguration.
    Instructions are now a list.
    """
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE)
    configuration = models.ForeignKey(
        CarConfiguration, on_delete=models.CASCADE)

    instructions = models.JSONField(
        help_text="A list of detailed steps for this specific car.")

    class Meta:
        unique_together = ('task', 'configuration')
        verbose_name_plural = "Tasks for Configurations"

    def __str__(self):
        return f"{self.task.name} for {self.configuration}"


class ServiceRecord(models.Model):
    """
    Tracks when a specific task was performed on a specific vehicle.
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    task = models.ForeignKey(TaskForConfiguration, on_delete=models.CASCADE)
    date_performed = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.task.task.name} on {self.vehicle}"
