from rest_framework import serializers


def format_time(time):
    """функция возвращает формат времени строкой с часами и минутами (без секунд)
    если объект - null, то возвращает пустую строку, так как по условиям задания
    необходимо чтобы в ответе JSON было утсновлено не None или Null, а пустая строка"""
    if time:
        return time.strftime('%H:%M')
    else:
        return ''


def format_schedule(schedule):
    """функция возвращает отформативаронные данные в виде словаря для
    создания новой заиси расписания для аптеки"""
    schedule_after_format = dict()
    day_dict = {
        1: 'monday',
        2: 'tuesday',
        3: 'wednesday',
        4: 'thursday',
        5: 'friday',
        6: 'saturday',
        7: 'sunday'
    }

    if schedule is None or len(schedule) != 7:
        raise serializers.ValidationError(
            {'message': 'В расписании должны быть указаны все дни недели'}
        )

    for day in schedule:
        if day['start'] != '':
            schedule_after_format[f'{day_dict[day["day"]]}_open'] = day['start']

        schedule_after_format[f'{day_dict[day["day"]]}_close'] = day['end']

    return schedule_after_format
