from rest_framework import serializers

from drugstores.models import (
    Drugstore,
    Location,
    Geo,
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
                    'start': day.start or '',
                    'end': day.end
                }
            )
        return schedule_list


class DrugstoreCreateSerializer(serializers.ModelSerializer):
    geo = GeoSerializer()

    class Meta:
        fields = (
            'drugstore_id',
            'geo',
            'phone',
         )
        model = Drugstore

    def to_representation(self, instance):
        return {
            'drugstore_id': instance.drugstore_id
        }

    def create(self, validated_data):
        geo = validated_data.pop('geo')
        location = geo.pop('location')

        location_obj = Location.objects.create(**location)
        geo_obj = Geo.objects.create(location=location_obj, **geo)

        drugstore = Drugstore.objects.create(geo=geo_obj, **validated_data)

        return drugstore
