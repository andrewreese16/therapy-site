from django.contrib import admin
from .models import Appointment


# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "appointment_date",
        "customer_email",
        "customer_phone",
        "created_at",
    )
    search_fields = ("customer_name", "customer_phone", "customer_email")
    list_filter = ("appointment_date",)
