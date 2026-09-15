from django.db import models
from django.contrib.auth.models import User


class SportEvent(models.Model):
    event_name = models.CharField(max_length=100)
    sport = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    maximum_participants = models.IntegerField()
    registration_fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.event_name


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(SportEvent, on_delete=models.CASCADE)
    registered_date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Registered', 'Registered'),
        ('Cancelled', 'Cancelled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Registered'
    )

    def __str__(self):
        return f"{self.user.username} - {self.event.event_name}"
# Create your models here.
