from django.shortcuts import render, redirect
from .models import Appointment
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime
from datetime import timedelta
import stripe
from django.conf import settings
from django.http import JsonResponse

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request):
    YOUR_DOMAIN = "https://the-listening-ear-9b83df5f497d.herokuapp.com/"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Therapy Appointment",
                        },
                        "unit_amount": 1000,  # Amount in cents (1000 = $10)
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success/",
            cancel_url=YOUR_DOMAIN + "/cancel/",
        )
        return JsonResponse({"id": checkout_session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)})


def checkout(request):
    if request.method == "POST":
        try:
            # Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": "Appointment Booking",
                            },
                            "unit_amount": 1000,  # $10.00 in cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url="https://the-listening-ear-9b83df5f497d.herokuapp.com/success/",
                cancel_url="https://the-listening-ear-9b83df5f497d.herokuapp.com/payment-cancel/",
            )
            # Redirect to the Stripe-hosted checkout page
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            # Render an error page or show error in checkout template
            return render(request, "checkout.html", {"error": str(e)})

    # Render the checkout form if GET request
    return render(request, "checkout.html")


def success(request):
    return render(request, "success.html")


def payment_cancel(request):
    return render(
        request,
        "payment_cancel.html",
        {"message": "Your payment was canceled. Please try again or contact support."},
    )


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
        notes = request.POST.get("notes")

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
                        notes=notes,
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
