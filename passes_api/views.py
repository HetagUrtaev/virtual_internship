from rest_framework import viewsets
from .serializers import PerevalSerializer
from .models import Pereval


class PerevalApiView(viewsets.ModelViewSet):
    queryset =Pereval.objects.all()
    serializer_class = PerevalSerializer
    http_method_names = ['get', 'post']

# как у ментора:
'''
from rest_framework import viewsets
from .services import PerevalSerializer, CoordSerializer, LevelSerializer, UsersSerializer, ImagesSerializer
from .models import Pereval, Coords, Level, Users, Images


class PerevalApiView(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    http_method_names = ['get', 'post', 'patch']


class CoordsApiView(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordSerializer


class LevelApiView(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class UsersApiView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class ImagesApiView(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
'''