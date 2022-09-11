import time

from rest_framework import serializers


def validate_schedule(data):
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
