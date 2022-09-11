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
        schedule = ScheduleDrugstore.objects.filter(drugstore=self)
        return get_schedule_representation(schedule)

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



