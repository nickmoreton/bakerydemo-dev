from django.urls import path
from .views import show_templates_view

urlpatterns = [
    path('', show_templates_view, name='show_templates'),
]
