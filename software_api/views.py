from rest_framework import generics
from .models import Software
from .serializers import SoftwareSerializer

class SoftwareListAPIView(generics.ListAPIView):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer