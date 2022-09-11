import time

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from drugstores.models import (
    Drugstore,
    Location,
    Geo,
    Schedule,
    ScheduleDrugstore
)


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'lat',
            'lon'
        )
        model = Location


class GeoSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        fields = (
            'address',
            'city_id',
            'city_name',
            'region_id',
            'region_name',
            'location'
        )
        model = Geo


class DrugstoreSerializer(serializers.ModelSerializer):
    geo = GeoSerializer()
    schedule = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'created_at',
            'updated_at',
            'drugstore_id',
            'geo',
            'phone',
            'schedule_representation',
            'schedule'
         )
        model = Drugstore

    def get_schedule(self, obj):
        schedule = ScheduleDrugstore.objects.filter(drugstore=obj.drugstore_id)
        schedule_list = []
        for day in schedule:
            schedule_list.append(
                {
                    'day': day.schedule.day,
                    'day_name': day.schedule.day_name,
                    'start': '' if day.start is None else day.start.strftime('%H:%M'),
                    'end': day.end.strftime('%H:%M')
                }
            )
        return schedule_list

    def list_for_schedule(self, drugstore, schedule):
        """возвращает список дней для создания аптеки"""
        return [ScheduleDrugstore(
            drugstore=drugstore,
            schedule=get_object_or_404(Schedule, day=day['day']),
            start=day['start'],
            end=day['end'],
        ) for day in schedule]

    def update(self, instance, validated_data):

        """получение нового расписания, удаление старного раписания"""
        schedule = self.initial_data.get('schedule')

        """получение нового гео, location"""
        geo = validated_data.get('geo')
        location = geo.pop('location')

        """сохранение основной информации о аптеке"""
        if validated_data.get('drugstore_id') == instance.drugstore_id:
            instance.drugstore_id = validated_data.get('drugstore_id', instance.drugstore_id)
            instance.phone = validated_data.get('phone', instance.phone)
            instance.geo.address = geo.get('address', instance.geo.address)
            instance.geo.city_id = geo.get('city_id', instance.geo.city_id)
            instance.geo.city_name = geo.get('city_name', instance.geo.city_name)
            instance.geo.region_id = geo.get('region_id', instance.geo.region_id)
            instance.geo.region_name = geo.get('region_name', instance.geo.region_name)
            instance.geo.location.lat = location.get('lat', instance.geo.location.lat)
            instance.geo.location.lon = location.get('lon', instance.geo.location.lon)
            instance.save()
        else:
            location_obj = Location.objects.create(**location)
            geo_obj = Geo.objects.create(location=location_obj, **geo)
            instance.drugstore_id = validated_data.get('drugstore_id', instance.drugstore_id)
            instance.phone = validated_data.get('phone', instance.phone)
            instance.geo = geo_obj
            instance.save()

        drugstore = Drugstore.objects.get(drugstore_id=instance.drugstore_id)

        """сохранение нового расписания"""
        ScheduleDrugstore.objects.filter(drugstore=drugstore).delete()
        ScheduleDrugstore.objects.bulk_create(
            self.list_for_schedule(drugstore, schedule)
        )

        return instance


class ScheduleJSONField(serializers.Field):

    def to_internal_value(self, data):
        """валидация расписания"""

        """дней недели должно быть 7"""
        if len(data) != 7:
            raise serializers.ValidationError({'message': 'Дней недели в раписание должно быть 7'})

        """дни недели должны быть последовательеы - 1-7"""
        if len({i['day'] for i in data}) != 7:
            raise serializers.ValidationError({'message': 'Проверьте правильность указания дней в расписании'})

        """правильность указания времени"""
        for day in data:
            try:
                if day['start'] != '':
                    time.strptime(day['start'], '%H:%M')
                time.strptime(day['end'], '%H:%M')
            except ValueError:
                raise serializers.ValidationError({'message': 'Проверьте правильность указания времени в расписании'})

            """правильность указания круглосуточной работы аптеки"""
            if (
                    day['start'] == '' and day['end'] != '23:59' or
                    day['start'] != '' and day['end'] == '23:59'
            ):
                raise serializers.ValidationError({'message': ('Проверьте правильность указания времени в раписании.'
                                                               ' Если вы указываете круглосуточную работу аптеки, '
                                                               'то необходимо начало работы не указывать, а окончание '
                                                               'работы указать - 23:59')})
            if day['start'] == '':
                day['start'] = None

        return data


class DrugstoreCreateSerializer(serializers.ModelSerializer):
    geo = GeoSerializer()
    schedule = ScheduleJSONField()

    class Meta:
        fields = (
            'drugstore_id',
            'geo',
            'phone',
            'schedule'
         )
        model = Drugstore

    def to_representation(self, instance):
        return {
            'drugstore_id': instance.drugstore_id
        }

    def list_for_schedule(self, drugstore, schedule):
        """возвращает список дней для создания аптеки"""
        return [ScheduleDrugstore(
            drugstore=drugstore,
            schedule=get_object_or_404(Schedule, day=day['day']),
            start=day['start'],
            end=day['end'],
        ) for day in schedule]

    def create(self, validated_data):
        geo = validated_data.pop('geo')
        location = geo.pop('location')
        schedule = validated_data.pop('schedule')

        location_obj = Location.objects.create(**location)
        geo_obj = Geo.objects.create(location=location_obj, **geo)

        drugstore = Drugstore.objects.create(geo=geo_obj, **validated_data)

        ScheduleDrugstore.objects.bulk_create(
            self.list_for_schedule(drugstore, schedule)
        )

        return drugstore
