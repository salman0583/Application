from django.urls import path
from django.views.generic.base import TemplateView
from .views import submit_form, get_forms

urlpatterns = [
    path('submit/', submit_form, name='submit_form'),
    path('forms/', get_forms, name='get_forms'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),  # Success page view
]
