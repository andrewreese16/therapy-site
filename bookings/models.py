from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Appointment(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField(max_length=254, null=True, blank=True)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.appointment_date}"
