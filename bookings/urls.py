from django.urls import path
from . import views

urlpatterns = [
    path("book/", views.book_appointment, name="book_appointment"),
    path("cancel/", views.cancel_appointment, name="cancel_appointment"),
]
