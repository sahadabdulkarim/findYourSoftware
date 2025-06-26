from django.urls import path
from .views import SoftwareListAPIView

urlpatterns = [
    path('software/', SoftwareListAPIView.as_view(), name='software-list'),
]
