from django.test import TestCase
from passes_api.models import Users, Coords, Level, Pereval, Images
from django.core.exceptions import ValidationError



class UsersTest(TestCase):
    def setUp(self):
        self.user = Users.objects.create(
            email='test_mail@mail.ru',
            fam='Иванов',
            name='Иван',
            otc='Иванович',
            phone='+7 555 55 55'
        )

    # проверяем создание пользователя
    def test_user_creation(self):
        self.assertEqual(Users.objects.count(), 1)
        self.assertEqual(self.user.email, 'test_mail@mail.ru')
        self.assertEqual(self.user.fam, 'Иванов')
        self.assertEqual(self.user.name, 'Иван')
        self.assertEqual(self.user.otc, 'Иванович')
        self.assertEqual(self.user.phone, '+7 555 55 55')

    # Проверяем blank=True, null=True в столбца otc
    def test_user_otc_can_be_blank(self):
        user_without_otc = Users.objects.create(
            email='test_mail2@mail.ru',
            fam='Иванов',
            name='Иван',
            phone='+7 555 55 55'
        )
        self.assertIsNone(user_without_otc.otc)


class CoordsTest(TestCase):
    def setUp(self):
        self.coords = Coords.objects.create(
            latitude = 45.3842,
            longitude = 7.1525,
            height = 1200
        )

    def test_coords_creation(self):
        self.assertEqual(Coords.objects.count(), 1)
        self.assertEqual(self.coords.latitude, 45.3842)
        self.assertEqual(self.coords.longitude, 7.1525)
        self.assertEqual(self.coords.height, 1200)


class LevelTest(TestCase):
    def setUp(self):
        self.level = Level.objects.create(
            winter='1А',
            spring='1А',
            summer='1А',
            autumn='1А'
        )


    # проверяем blank=True, null=True
    def test_level_fields_can_be_blank(self):
        empty_level = Level.objects.create()
        self.assertIsNone(empty_level.winter)
        self.assertIsNone(empty_level.spring)
        self.assertIsNone(empty_level.summer)
        self.assertIsNone(empty_level.autumn)

    # проверяем ограничение max_length=50
    def test_level_field_length_limit(self):
        long_value = 'a' * 51
        with self.assertRaises(ValidationError):
            long_level = Level(winter=long_value)
            long_level.full_clean()




class PerevalTest(TestCase):
    def setUp(self):
        self.user = Users.objects.create(
            email='mail@mail.ru',
            fam='Иванов',
            name='Иван',
            phone='+7 555 55 55'
        )
        self.coords = Coords.objects.create(
            latitude=45.0,
            longitude=40.0,
            height=2000
        )
        self.level = Level.objects.create(summer='hard')
        self.pereval = Pereval.objects.create(
            title='Пхия',
            beauty_title='перевал',
            add_time='2021-09-22T13:18:13Z',
            user=self.user,
            coords=self.coords,
            level=self.level,
            status='new'
        )

    def test_pereval_creation(self):
        self.assertEqual(Pereval.objects.count(), 1)
        self.assertEqual(self.pereval.title, 'Пхия')
        self.assertEqual(self.pereval.status, 'new')
        self.assertEqual(self.pereval.user, self.user)
        self.assertEqual(self.pereval.coords, self.coords)
        self.assertEqual(self.pereval.level, self.level)


class ImagesTest(TestCase):
    def setUp(self):
        self.user = Users.objects.create(
            email='mail@mail.ru',
            fam='Иванов',
            name='Иван',
            phone='+7 555 55 55'
        )
        self.coords = Coords.objects.create(
            latitude=60.0,
            longitude=30.0,
            height=500
        )
        self.level = Level.objects.create(summer='medium')
        self.pereval = Pereval.objects.create(
            title='Пхия',
            beauty_title='перевал',
            add_time='2021-09-22T13:18:13Z',
            user=self.user,
            coords=self.coords,
            level=self.level,
            status='new'
        )

    def test_image_creation(self):
        image = Images.objects.create(
            data='картинка№1',
            title='Седловина',
            pereval=self.pereval
        )
        self.assertEqual(Images.objects.count(), 1)
        self.assertEqual(image.title, 'Седловина')
        self.assertEqual(image.pereval, self.pereval)
        self.assertEqual(image.data, 'картинка№1')

    # Проверка возможности добавить несколько изображений к одному перевалу
    def test_multiple_images_for_pereval(self):
        image1 = Images.objects.create(
            data='картинка№1',
            title='Седловина',
            pereval=self.pereval
        )
        image2 = Images.objects.create(
            data='картинка№2',
            title='Седловина',
            pereval=self.pereval
        )
        self.assertEqual(Images.objects.count(), 2)
        self.assertEqual(self.pereval.images.count(), 2)
        self.assertIn(image1, self.pereval.images.all())
        self.assertIn(image2, self.pereval.images.all())