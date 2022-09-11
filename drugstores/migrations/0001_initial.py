# Generated by Django 4.1.1 on 2022-09-11 08:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drugstore',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('drugstore_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Идентификатор аптеки')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Аптека',
                'verbose_name_plural': 'Аптеки',
                'ordering': ['drugstore_id'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Широта')),
                ('lon', models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Координаты аптеки',
                'verbose_name_plural': 'Координаты аптек',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('day', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('day_name', models.CharField(max_length=2)),
            ],
            options={
                'verbose_name': 'День недели',
                'verbose_name_plural': 'Дни недели',
                'ordering': ['day'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleDrugstore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField(blank=True, null=True, verbose_name='Время открытия')),
                ('end', models.TimeField(verbose_name='Время закрытия')),
                ('drugstore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugstores.drugstore')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugstores.schedule')),
            ],
            options={
                'verbose_name': 'Расписание аптеки',
                'verbose_name_plural': 'Расписания аптек',
                'ordering': ['drugstore', 'schedule'],
            },
        ),
        migrations.CreateModel(
            name='Geo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес аптеки')),
                ('city_id', models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор города')),
                ('city_name', models.CharField(max_length=200, verbose_name='Город аптеки')),
                ('region_id', models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор региона')),
                ('region_name', models.CharField(max_length=200, verbose_name='Регион аптеки')),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='geo', to='drugstores.location', verbose_name='Координтаты')),
            ],
            options={
                'verbose_name': 'Местоположеие аптеки',
                'verbose_name_plural': 'Местоположения аптек',
            },
        ),
        migrations.AddField(
            model_name='drugstore',
            name='geo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='drugstore', to='drugstores.geo', verbose_name='Гео'),
        ),
        migrations.AddField(
            model_name='drugstore',
            name='schedule',
            field=models.ManyToManyField(through='drugstores.ScheduleDrugstore', to='drugstores.schedule'),
        ),
        migrations.AddConstraint(
            model_name='scheduledrugstore',
            constraint=models.UniqueConstraint(fields=('drugstore', 'schedule'), name='unique_drugstore_schedule'),
        ),
    ]
