from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:category>", views.category, name="category"),
    path("new/<str:new>", views.new, name="new"),
    path("news", views.news, name="news"),
    path("contact", views.contact, name="contact"),
]
