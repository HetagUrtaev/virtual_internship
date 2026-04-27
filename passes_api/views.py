from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import PerevalSerializer
from .models import Pereval


class PerevalApiView(viewsets.ModelViewSet):
    queryset =Pereval.objects.all()
    serializer_class = PerevalSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'status': 400,
                    'message': 'Bad Request (при нехватке полей)',
                    'id': None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pereval = serializer.save()

            return Response(
                {
                    'status': 200,
                    'message': None,
                    'id': pereval.id
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status': 500,
                    'message': str(e),
                    'id': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )