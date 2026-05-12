from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import PerevalSerializer
from .models import Pereval


class PerevalApiView(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    http_method_names = ['get', 'post', 'patch']

    '''
    Переопределяем метод create() для изменения ответов json
    при создании, или попытке создания объекта
    '''

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'state': 400,
                    'message': 'Bad Request (при нехватке полей)',
                    'id': None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pereval = serializer.save()

            return Response(
                {
                    'state': 200,
                    'message': None,
                    'id': pereval.id
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    'state': 500,
                    'message': str(e),
                    'id': None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    '''
    Переопределяем метод partial_update() для добавления кастомной логике 
    при изменении существующего объекта. 
    1. Запрет на изменение объекта если он не в статусе 'new' 
    (также данный запрет присутствует в serializers.py)
    2. Редактировать можно все поля, кроме тех, что 
    содержат в себе ФИО, адрес почты и номер телефона.
    3. Запрещено удалять users в целом. 
    '''

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        pereval_data = request.data

        # instance - имеющиеся данные в БД
        # request - новые данные, обновляют БД

        # Проверяем статус объекта
        if instance.status != 'new':
            return Response({
                'state': 0,
                'message': f'''Редактирование запрещено: объект имеет статус {instance.status}''',
            })

        # Проверяем поля, которые нельзя менять
        user_data = pereval_data.get('user')
        user_dict = model_to_dict(instance.user)
        user_dict.pop('id')
        if user_data and user_dict != user_data:
            return Response({
                'state': 0,
                'message': 'Нельзя редактировать пользователя',
            })

        # устанавливаем запрет на редактирование статуса
        pereval_status = request.data.get('status')
        if pereval_status and pereval_status != instance.status:
            return Response({
                'state': 0,
                'message': 'Нельзя редактировать статус',
            })

        kwargs['partial'] = True
        serializer = self.get_serializer(instance, data=pereval_data, partial=True)

        if not serializer.is_valid():
            return Response({
                'state': 0,
                'message': 'Ошибка валидации данных',
                'errors': serializer.errors,
            })

        try:
            self.perform_update(serializer)  # сохранение данных
            return Response({
                'state': 1,
                'message': 'Данные успешно обновлены',
            })
        except Exception as e:
            return Response({
                'state': 0,
                'message': str(e),
            })

    '''
    Переопределяем list() для получения всех объектов, 
    либо для получения объектов которые пользовались 
    определенной почтой. В зависимости от тела запроса
    '''

    def list(self, request, *args, **kwargs):
        email = request.query_params.get('user__email')
        queryset = self.filter_queryset(self.get_queryset())

        if email:
            queryset = queryset.filter(user__email=email)
            message = f'Найдено {queryset.count()} объектов для email: {email}'
        else:
            message = 'Возвращены все объекты'

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'state': 1,
            'message': message,
            'data': serializer.data
        }, status=status.HTTP_200_OK)