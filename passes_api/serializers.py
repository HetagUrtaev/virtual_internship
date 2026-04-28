from rest_framework import serializers
from .models import Pereval, Users, Coords, Level, Images


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'fam', 'name', 'otc', 'phone', ]

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height',]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['data', 'title']


class PerevalSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Pereval
        fields = [
            'beauty_title', 'title', 'other_titles',
            'connect', 'add_time', 'user', 'coords', 'level', 'images'
        ]

    def create(self, validated_data):
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images', [])
        user_data = validated_data.pop('user')


        coords = Coords.objects.create(**coords_data)
        level = Level.objects.create(**level_data)
        user, _ = Users.objects.get_or_create(**user_data)


        pereval = Pereval.objects.create(
            user=user,
            coords=coords,
            level=level,
            **validated_data
        )


        for image_data in images_data:
            Images.objects.create(pereval=pereval, **image_data)

        return pereval