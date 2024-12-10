from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from datetime import timedelta


class Appointment(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField(max_length=254, null=True, blank=True)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)  # Notes field for the admin

    def __str__(self):
        return f"{self.customer_name} - {self.appointment_date}"

    def clean(self):
        """
        Custom validation to ensure no overlapping appointments and block times that have already been taken.
        """
        # Ensure no appointments are scheduled at the same time or overlapping
        conflicting_appointments = Appointment.objects.filter(
            appointment_date__gte=self.appointment_date,
            appointment_date__lt=self.appointment_date
            + timedelta(minutes=30),  # Add timedelta to DateTime
        )
        if conflicting_appointments.exists():
            raise ValidationError(f"The selected time slot is already taken.")

    def save(self, *args, **kwargs):
        # Run the validation before saving
        self.clean()
        super().save(*args, **kwargs)
