from django.shortcuts import render, redirect
from .models import Appointment
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime
from datetime import timedelta

# Create your views here.


def book_appointment(request):
    # Generate a list of 30-minute intervals for the day
    time_slots = []
    for hour in range(24):  # Loop through 24 hours
        for minute in ["00", "30"]:  # Add 30-minute intervals
            time_str = f"{hour:02}:{minute}"
            # Convert time to 12-hour format (with AM/PM)
            time_obj = datetime.strptime(time_str, "%H:%M")
            time_formatted = time_obj.strftime("%I:%M %p")  # %I is 12-hour, %p is AM/PM
            time_slots.append(time_formatted)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        date = request.POST.get("date")  # Date selected
        time = request.POST.get("time")  # Time selected
        email = request.POST.get("email")

        # Combine date and time into a single datetime object
        try:
            if date and time and name and phone and email:
                # Combine date and time into a single string
                # Format example: '2024-12-10 10:30 AM'
                datetime_str = f"{date} {time}"
                appointment_date = datetime.strptime(datetime_str, "%Y-%m-%d %I:%M %p")

                # Make it aware to handle timezone correctly
                appointment_date = make_aware(appointment_date)

                # Check if this time is available
                if Appointment.objects.filter(
                    appointment_date=appointment_date
                ).exists():
                    messages.error(request, "This time slot is already taken.")
                else:
                    Appointment.objects.create(
                        customer_name=name,
                        customer_phone=phone,
                        customer_email=email,
                        appointment_date=appointment_date,
                    )
                    messages.success(request, "Appointment booked successfully!")
                    return redirect("/")  # Redirect to the landing page after booking
            else:
                messages.error(request, "Please fill in all fields.")
        except ValueError:
            messages.error(request, "Invalid date or time format. Please try again.")

    return render(request, "bookings/book.html", {"time_slots": time_slots})


def cancel_appointment(request):
    if request.method == "POST":
        if "appointment_id" in request.POST:
            # Handle selected appointment for cancellation
            appointment_id = request.POST.get("appointment_id")
            appointment = Appointment.objects.filter(id=appointment_id).first()
            if appointment:
                appointment.delete()
                messages.success(
                    request, "Your appointment has been canceled successfully!"
                )
                return redirect("/")
            else:
                messages.error(request, "The selected appointment could not be found.")
        else:
            # Handle initial cancellation request
            name = request.POST.get("name")
            phone = request.POST.get("phone")

            appointments = Appointment.objects.filter(
                customer_name=name, customer_phone=phone
            )

            if appointments.exists():
                if len(appointments) > 1:
                    return render(
                        request,
                        "bookings/select_appointment.html",
                        {"appointments": appointments},
                    )

                appointment = appointments.first()
                appointment.delete()
                messages.success(
                    request, "Your appointment has been canceled successfully!"
                )
                return redirect("/")
            else:
                messages.error(
                    request, "No appointment found with the provided details."
                )
    return render(request, "bookings/cancel.html")


def landing_page(request):
    return render(request, "base.html")


def about_me(request):
    return render(request, "bookings/about_me.html")
