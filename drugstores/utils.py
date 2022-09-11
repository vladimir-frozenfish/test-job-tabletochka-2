from collections import defaultdict

def get_schedule_representation(data):
    # open_list = [
    #     data.schedule.monday_open,
    #     data.schedule.tuesday_open,
    #     data.schedule.wednesday_open,
    #     data.schedule.thursday_open,
    #     data.schedule.friday_open,
    #     data.schedule.saturday_open,
    #     data.schedule.sunday_open
    # ]
    # close_list = [
    #     data.schedule.monday_close,
    #     data.schedule.tuesday_close,
    #     data.schedule.wednesday_close,
    #     data.schedule.thursday_close,
    #     data.schedule.friday_close,
    #     data.schedule.saturday_close,
    #     data.schedule.sunday_close
    # ]
    #
    # """проверка на круглосуточную работу аптеки"""
    # open_set = set(open_list)
    # close_set = set(close_list)
    # if (
    #         len(open_set) == 1
    #         and len(close_set) == 1
    #         and open_set.pop() is None
    #         and close_set.pop().strftime('%H:%M') == '23:59'
    # ):
    #     return 'круглосуточно'
    #
    # """проверка на одинаковую работу аптеки все дни"""
    # open_set = set(open_list)
    # close_set = set(close_list)
    # if (
    #         len(open_set) == 1
    #         and len(close_set) == 1
    # ):
    #     return (f'ежедневно '
    #             f'{open_set.pop().strftime("%H:%M")}'
    #             f'-{close_set.pop().strftime("%H:%M")}')
    #
    # """формирование расписания при разных режимах работы"""
    # schedule_dict = defaultdict(list)
    # schedule_dict[f'{data.schedule.monday_open.strftime("%H:%M")}-{data.schedule.monday_close.strftime("%H:%M")}'].append('пн')
    # schedule_dict[f'{data.schedule.tuesday_open.strftime("%H:%M")}-{data.schedule.tuesday_close.strftime("%H:%M")}'].append('вт')
    # schedule_dict[f'{data.schedule.wednesday_open.strftime("%H:%M")}-{data.schedule.wednesday_close.strftime("%H:%M")}'].append('ср')
    # schedule_dict[f'{data.schedule.thursday_open.strftime("%H:%M")}-{data.schedule.thursday_close.strftime("%H:%M")}'].append('чт')
    # schedule_dict[f'{data.schedule.friday_open.strftime("%H:%M")}-{data.schedule.friday_close.strftime("%H:%M")}'].append('пт')
    # schedule_dict[f'{data.schedule.saturday_open.strftime("%H:%M")}-{data.schedule.saturday_close.strftime("%H:%M")}'].append('сб')
    # schedule_dict[f'{data.schedule.sunday_open.strftime("%H:%M")}-{data.schedule.sunday_close.strftime("%H:%M")}'].append('вс')
    #
    # schedule_str = ''
    # for key, value in schedule_dict.items():
    #     if len(value) > 2:
    #         schedule_str += f'{value[0]}-{value[-1]} {key} '
    #     else:
    #         schedule_str += f'{",".join(value)} {key} '
    #
    # return schedule_str.rstrip()
    return 'Пока нет'
