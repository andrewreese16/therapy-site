from django.contrib import admin
from django.urls import include, path
from bookings import views
from bookings import views as bookings_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.landing_page, name="landing_page"),  # Root path for landing page
    path("about/", views.about_me, name="about_me"),  # About Me page
    path("bookings/", include("bookings.urls")),
    path("checkout/", bookings_views.checkout, name="checkout"),
    path("payment-cancel/", views.payment_cancel, name="payment_cancel"),
    path("success/", views.success, name="success"),  # Bookings app URLs
]
