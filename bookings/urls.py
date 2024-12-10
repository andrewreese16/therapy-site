from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path(
        "create-checkout-session/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    path("book/", views.book_appointment, name="book_appointment"),
    path("cancel/", views.cancel_appointment, name="cancel_appointment"),
    path('success/', views.success, name='success'),  # Add success and cancel views
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
]
