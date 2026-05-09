from django.urls import path, include
from rest_framework import routers
from .views import PerevalApiView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = routers.DefaultRouter()
router.register(r'submitData', PerevalApiView, basename='pereval')



urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
]