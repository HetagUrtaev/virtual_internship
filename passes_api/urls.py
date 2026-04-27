from django.urls import path, include
from rest_framework import routers
from .views import PerevalApiView

router = routers.DefaultRouter()
router.register(r'submitData', PerevalApiView, basename='pereval')

urlpatterns = [
    path('', include(router.urls)),
]
