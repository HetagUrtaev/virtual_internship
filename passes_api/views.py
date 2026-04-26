from rest_framework import viewsets
from .serializers import PerevalSerializer
from .models import Pereval


class PerevalApiView(viewsets.ModelViewSet):
    queryset =Pereval.objects.all()
    serializer_class = PerevalSerializer
    http_method_names = ['get', 'post']

