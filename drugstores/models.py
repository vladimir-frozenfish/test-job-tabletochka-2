import uuid
from django.db import models

from .utils import get_schedule_representation


class Drugstore(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата изменения'
    )
    drugstore_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, verbose_name='Идентификатор аптеки'
    )
    phone = models.CharField(
        max_length=20, verbose_name='Телефон'
    )
    geo = models.OneToOneField('Geo', on_delete=models.PROTECT, verbose_name='Гео', related_name='drugstore')
    schedule = models.ManyToManyField(
        'Schedule',
        through='ScheduleDrugstore',
        blank=False
    )

    def schedule_representation(self):
        return get_schedule_representation(self)

    schedule_representation.short_description = 'Время работы аптеки'

    class Meta:
        verbose_name_plural = 'Аптеки'
        verbose_name = 'Аптека'
        ordering = ['drugstore_id']

    def __str__(self):
        return str(self.drugstore_id)


class Schedule(models.Model):
    day = models.PositiveSmallIntegerField(primary_key=True)
    day_name = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = 'Дни недели'
        verbose_name = 'День недели'
        ordering = ['day']

    def __str__(self):
        return str(self.day_name)


class ScheduleDrugstore(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    drugstore = models.ForeignKey(Drugstore, on_delete=models.CASCADE)
    start = models.TimeField(blank=True, null=True, verbose_name='Время открытия')
    end = models.TimeField(verbose_name='Время закрытия')

    class Meta:
        verbose_name_plural = 'Расписания аптек'
        verbose_name = 'Расписание аптеки'
        ordering = ['drugstore', 'schedule']

        constraints = [
            models.UniqueConstraint(
                fields=['drugstore', 'schedule'],
                name="unique_drugstore_schedule"
            )
        ]

    def __str__(self):
        return (f'{self.schedule.day_name}: {self.start}-{self.end}')


class Geo(models.Model):
    address = models.CharField(max_length=200, verbose_name='Адрес аптеки')
    city_id = models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор города')
    city_name = models.CharField(max_length=200, verbose_name='Город аптеки')
    region_id = models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор региона')
    region_name = models.CharField(max_length=200, verbose_name='Регион аптеки')
    location = models.OneToOneField('Location', on_delete=models.PROTECT, verbose_name='Координтаты', related_name='geo')

    class Meta:
        verbose_name_plural = 'Местоположения аптек'
        verbose_name = 'Местоположеие аптеки'
        # ordering = ['drugstore_id']

    def __str__(self):
        return f'{self.region_name}, {self.city_name}, {self.address}'


class Location(models.Model):
    # drugstore = models.OneToOneField(
    #     Drugstore, on_delete=models.CASCADE, verbose_name='Аптека'
    # )
    lat = models.DecimalField(
        max_digits=8, decimal_places=6, verbose_name='Широта'
    )
    lon = models.DecimalField(
        max_digits=8, decimal_places=6, verbose_name='Долгота'
    )

    class Meta:
        verbose_name_plural = 'Координаты аптек'
        verbose_name = 'Координаты аптеки'
        # ordering = ['drugstore_id']

    def __str__(self):
        return f'{self.lat}, {self.lon}'








'''
class Region(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(
        max_length=100, verbose_name='Регион'
    )

    class Meta:
        verbose_name_plural = 'Регионы'
        verbose_name = 'Регион'
        ordering = ['name']

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE,
        related_name='cities', verbose_name='Регион города'
    )
    name = models.CharField(
        max_length=100, verbose_name='Город'
    )

    class Meta:
        verbose_name_plural = 'Города'
        verbose_name = 'Город'
        ordering = ['name']

    def __str__(self):
        return self.name





class Schedule(models.Model):
    drugstore = models.OneToOneField(
        Drugstore, on_delete=models.CASCADE,
        related_name='schedule', verbose_name='Аптека'
    )
    monday_open = models.TimeField(blank=True, null=True, verbose_name='Понедельник открытие')
    monday_close = models.TimeField(verbose_name='Понедельник закрытие')
    tuesday_open = models.TimeField(blank=True, null=True, verbose_name='Вторник открытие')
    tuesday_close = models.TimeField(verbose_name='Вторник закрытие')
    wednesday_open = models.TimeField(blank=True, null=True, verbose_name='Среда открытие')
    wednesday_close = models.TimeField(verbose_name='Среда закрытие')
    thursday_open = models.TimeField(blank=True, null=True, verbose_name='Четверг открытие')
    thursday_close = models.TimeField(verbose_name='Четверг закрытие')
    friday_open = models.TimeField(blank=True, null=True, verbose_name='Пятница открытие')
    friday_close = models.TimeField(verbose_name='Пятница закрытие')
    saturday_open = models.TimeField(blank=True, null=True, verbose_name='Суббота открытие')
    saturday_close = models.TimeField(verbose_name='Суббота закрытие')
    sunday_open = models.TimeField(blank=True, null=True, verbose_name='Воскресенье открытие')
    sunday_close = models.TimeField(verbose_name='Воскресенье закрытие')

    class Meta:
        verbose_name_plural = 'Расписание аптек'
        verbose_name = 'Расписание аптеки'
        ordering = ['drugstore']

    def __str__(self):
        return self.drugstore.drugstore_id


class Geo(models.Model):
    drugstore = models.OneToOneField(
        Drugstore, on_delete=models.CASCADE,
        related_name='geo', verbose_name='Аптека'
    )
    address = models.CharField(max_length=200, verbose_name='Адрес аптеки')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        related_name='drugstores', verbose_name='Город аптеки'
    )
    location_lat = models.DecimalField(
        max_digits=8, decimal_places=6, verbose_name='Широта'
    )
    location_lon = models.DecimalField(
        max_digits=8, decimal_places=6, verbose_name='Долгота'
    )

    class Meta:
        verbose_name_plural = 'Местоположения аптек'
        verbose_name = 'Местоположение аптеки'
        ordering = ['drugstore']

    def __str__(self):
        return f'{self.city.region}, {self.city}, {self.address}'
'''