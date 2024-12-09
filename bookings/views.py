from django.shortcuts import render, redirect
from .models import Appointment
from django.contrib import messages

# Create your views here.


def book_appointment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        email = request.POST.get("email")  # Capture the email input from the form

        if (
            name and phone and date and email
        ):  # Ensure the email is included in the form
            Appointment.objects.create(
                customer_name=name,
                customer_phone=phone,
                appointment_date=date,
                customer_email=email,  # Save the email to the Appointment model
            )
            messages.success(request, "Appointment booked successfully!")
            return redirect("/")  # Redirect to the landing page after booking
        else:
            messages.error(request, "Please fill in all fields.")
    return render(request, "bookings/book.html")


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
