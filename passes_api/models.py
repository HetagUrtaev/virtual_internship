from django.db import models


# данные о каждом пользователе
class Users(models.Model):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    fam = models.CharField(max_length=50, verbose_name="фамилия")
    name = models.CharField(max_length=50, verbose_name="имя")
    otc = models.CharField(max_length=50, blank=True, null=True, verbose_name="отчество")
    phone = models.CharField(max_length=50, verbose_name="мобильный телефон")

    def __str__(self):
        return f"{self.fam} {self.name}"


# координаты
class Coords(models.Model):
    latitude = models.FloatField(verbose_name="широта")
    longitude = models.FloatField(verbose_name="долгота")
    height = models.IntegerField(verbose_name="высота")

    def __str__(self):
        return f"({self.latitude}, {self.longitude}) - {self.height}м"

# уровни сложности
class Level(models.Model):
    winter = models.CharField(max_length=50, blank=True, null=True, verbose_name="уровень сложности зимой")
    spring = models.CharField(max_length=50, blank=True, null=True, verbose_name="уровень сложности весной")
    summer = models.CharField(max_length=50, blank=True, null=True, verbose_name="уровень сложности летом")
    autumn = models.CharField(max_length=50, blank=True, null=True, verbose_name="уровень сложности осенью")

# перевалы
class Pereval(models.Model):

    MODERATION_STATUS = [
        ('new', 'Новый'),
        ('pending', 'Ожидает'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    ]

    beauty_title = models.CharField(max_length=250, blank=True, null=True, verbose_name="красивое название")
    title = models.CharField(max_length=250, verbose_name="основное название")
    other_titles = models.CharField(max_length=250, blank=True, null=True, verbose_name="другие названия")
    connect = models.CharField(max_length=250, verbose_name="информация о соединениях")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="время добавления") # время добавления - приходит от клиента, не автоматом
    user = models.ForeignKey(Users, on_delete=models.CASCADE) # ссылка на пользователя // ForeignKey - Users
    coord = models.ForeignKey(Coords, on_delete=models.CASCADE) # ссылка на координаты // ForeignKey - Coords
    level = models.ForeignKey(Level, on_delete=models.CASCADE) # ссылка на уровни // ForeignKey - Level
    status = models.CharField(max_length=10, choices=MODERATION_STATUS, default='new', verbose_name="статус модерации")

    def __str__(self):
        return self.title


class Images(models.Model):
    data =  models.TextField(verbose_name="данные изображения")
    title = models.CharField(max_length=50, verbose_name="название изображения")
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE) # ForeignKey обратная связь (через related_name) с моделью Pereval

    def __str__(self):
        return self.title


