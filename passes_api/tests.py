import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from passes_api.models import Pereval, Users, Coords, Level, Images
from passes_api.serializers import PerevalSerializer


class PerevalTestCase(APITestCase):
    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            beauty_title="beauty_title_1",
            title="title_1",
            other_titles="other_titles_1",
            connect="connect_1",
            add_time="2021-09-22T13:18:13Z",
            user=Users.objects.create(
                email="email1@email.ru",
                fam="fam_1",
                name="name_1",
                otc="otc_1",
                phone="890000001",
            ),
            coords=Coords.objects.create(
                latitude=123.00,
                longitude=456.00,
                height=1001,
            ),
            level=Level.objects.create(
                winter="1A",
                summer="1A",
                autumn="1A",
                spring="",
            )
        )

        self.image_1_1 = Images.objects.create(
            title="title_image_1_1",
            data="data_image_1_1",
            pereval=self.pereval_1
        )
        self.image_1_2 = Images.objects.create(
            title="title_image_1_2",
            data="data_image_1_2",
            pereval=self.pereval_1
        )

        self.pereval_2 = Pereval.objects.create(
            beauty_title="beauty_title_2",
            title="title_2",
            other_titles="other_titles_2",
            connect="connect_2",
            add_time="2021-09-22T13:18:13Z",
            user=Users.objects.create(
                email="email2@email.ru",
                fam="fam_2",
                name="name_2",
                otc="otc_2",
                phone="890000002",
            ),
            coords=Coords.objects.create(
                latitude=123.02,
                longitude=456.02,
                height=1002,
            ),
            level=Level.objects.create(
                winter="1B",
                summer="1B",
                autumn="1B",
                spring="1C",
            )
        )

        self.image_2_1 = Images.objects.create(
            title="title_image_2_1 ",
            data="data_image_2_1 ",
            pereval=self.pereval_2
        )
        self.image_2_2 = Images.objects.create(
            title="title_image_2_2",
            data="data_image_2_2",
            pereval=self.pereval_2
        )

    def test_get_list(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.pereval_1.__str__(), self.pereval_1.title)

        self.assertEqual(self.pereval_1.user.__str__(), f"{self.pereval_1.user.fam} {self.pereval_1.user.name}")

        self.assertEqual(self.pereval_1.coords.__str__(), f"({self.pereval_1.coords.latitude}, {self.pereval_1.coords.longitude}) - {self.pereval_1.coords.height}м")

        self.assertEqual(self.image_1_1.__str__(), self.image_1_1.title)

        self.assertEqual(2, len(serializer_data))

    def test_get_detail(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_1.pk})
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_post_pereval(self):
        url = reverse('pereval-list')
        data = {
            "beauty_title": "ПЕРЕВАЛ-ТЕСТ",
            "title": "ПЕРЕВАЛ-ТЕСТ",
            "other_titles": "ПЕРЕВАЛ-ТЕСТ",
            "connect": "",

            "add_time": "2021-09-22 13:18:13",
            "user": {"email": "test@test.com",
                     "fam": "ПОЛЬЗОВАТЕЛЬ",
                     "name": "ПОЛЬЗОВАТЕЛЬ",
                     "otc": "ПОЛЬЗОВАТЕЛЬ",
                     "phone": "890000003"},

            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200"},

            "level": {"winter": "1B",
                      "summer": "1B",
                      "autumn": "1B",
                      "spring": "1B"},

            "images": [
                {"data": "КАРТИНКА1", "title": "ЗАГОЛОВОК1"},
                {"data": "КАРТИНКА2", "title": "ЗАГОЛОВОК2"}
            ]
        }

        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pereval.objects.all().count(), 3)

    def test_patch_pereval(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_1.pk})
        response = self.client.get(url)
        data = {
            "beauty_title": "beauty_title_new",
            "title": "title_new",
            "other_titles": "other_titles_new",
            "connect": "connect_new",
            "add_time": "2021-09-22T13:18:13Z",
            "user": {
                "email": "email1@email.ru",
                "fam": "fam_1",
                "name": "name_1",
                "otc": "otc_1",
                "phone": "890000001"
            },
            "coords": {
                "latitude": 444.00,
                "longitude": 555.00,
                "height": 1001
            },
            "level": {
                "winter": "1A",
                "summer": "1A",
                "autumn": "1A",
                "spring": "1B"
            },
            "images": [
                {
                    "title": "title_image_1_1",
                    "data": "data_image_1_1"
                },
                {
                    "title": "title_image_1_2",
                    "data": "data_image_1_2"
                }
            ]

        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.pereval_1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.pereval_1.beauty_title, "beauty_title_new")
        self.assertEqual(self.pereval_1.title, "title_new")
        self.assertEqual(self.pereval_1.coords.latitude, 444.00)
        self.assertEqual(self.pereval_1.coords.longitude, 555.00)
        self.assertEqual(self.pereval_1.level.spring, "1B")