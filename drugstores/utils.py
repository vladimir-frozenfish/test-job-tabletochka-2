from collections import defaultdict


def get_schedule_representation(schedule):

    if not schedule:
        return 'Расписание работы аптеки не указано'

    open_list = [day.start for day in schedule]
    close_list = [day.end for day in schedule]

    """проверка на круглосуточную работу аптеки"""
    open_set = set(open_list)
    close_set = set(close_list)
    if (
            len(open_set) == 1
            and len(close_set) == 1
            and open_set.pop() is None
            and close_set.pop().strftime('%H:%M') == '23:59'
    ):
        return 'круглосуточно'

    """проверка на одинаковую работу аптеки все дни"""
    open_set = set(open_list)
    close_set = set(close_list)
    if (
            len(open_set) == 1
            and len(close_set) == 1
    ):
        return (f'ежедневно '
                f'{open_set.pop().strftime("%H:%M")}'
                f'-{close_set.pop().strftime("%H:%M")}')

    """формирование расписания при разных режимах работы"""
    schedule_dict = defaultdict(list)
    for day in schedule:
        schedule_dict[f'{day.start.strftime("%H:%M")}-{day.end.strftime("%H:%M")}'].append(day.schedule.day_name)

    schedule_str = ''
    for key, value in schedule_dict.items():
        if len(value) > 2:
            schedule_str += f'{value[0]}-{value[-1]} {key} '
        else:
            schedule_str += f'{",".join(value)} {key} '

    return schedule_str.rstrip()
