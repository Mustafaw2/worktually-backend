from django.urls import path
from .views import SendJobOfferView

urlpatterns = [
    path('send-job-offer/', SendJobOfferView.as_view(), name='send-job-offer'),
]
