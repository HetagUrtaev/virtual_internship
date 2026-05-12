from django.test import TestCase, Client
from django.urls import reverse
import json

class APITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.pereval_data = {
             "beauty_title": "перевал",
             "title": "Пхия",
             "other_titles": "Триев",
             "connect": "",
             "add_time": "2021-09-22T13:18:13Z",
             "user": {
               "email": "mail@mail.ru",
               "fam": "Иванов",
               "name": "Иван",
               "otc": "Иванович",
               "phone": "+7 555 55 55"
             },
             "coords": {
               "latitude": 45.3842,
               "longitude": 7.1525,
               "height": 1200
             },
             "level": {
               "id": 3,
               "winter": "",
               "spring": "",
               "summer": "1А",
               "autumn": "1А"
             },
             "status": "new",
             "images": [
               {
                 "data": "картинка№1",
                 "title": "Седловина"
               },
               {
                 "data": "картинка№2",
                 "title": "Подъём"
               }
             ]
           }

    def test_create_pereval(self):
        # тест на создание объекта (POST)
        response = self.client.post(
            reverse('pereval-list'),
            data=json.dumps(self.pereval_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertIn('id', response_data)

    def test_get_pereval_by_id(self):
        # тест на получение объекта (GET)
        create_response = self.client.post(
            reverse('pereval-list'),
            data=json.dumps(self.pereval_data),
            content_type='application/json'
        )

        pereval_id = create_response.json()['id']

        get_response = self.client.get(
            reverse('pereval-detail', kwargs={'pk': pereval_id})
        )

        self.assertEqual(get_response.status_code, 200)

        data = get_response.json()
        self.assertEqual(data['title'], 'Пхия')
        self.assertEqual(data['user']['email'], 'mail@mail.ru')
        self.assertEqual(len(data['images']), 2)