from asist.database import Users
from datetime import datetime

from .include import hbold


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_user(id_user):
    user, _ = Users.get_or_create(
        user_id=id_user,
    )
    return user


def time_difference(input_time):
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    input_datetime = datetime.strptime(input_time, "%H:%M")
    current_datetime = datetime.strptime(current_time, "%H:%M")

    time_delta = input_datetime - current_datetime

    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "Время уже прошло" if time_delta.days < 0 else f"{hours:02d}:{minutes:02d}"

def time_to_text(time_str):
    res_str = ''
    data_hours = {
        'час': [1, 21],
        'часа': [2, 3, 4, 22, 23, 24],
        'часов': [int(i) for i in range(5, 21)] + [0]
    }
    data_minutes = {
        'минута': [1, 21],
        'минуты': [2, 3, 4, 22, 23, 24],
        'минут': [int(i) for i in range(5, 21)] + [0] +
                 [int(i) for i in range(25, 31)] +
                 [int(i) for i in range(35, 41)] +
                 [int(i) for i in range(45, 51)] +
                 [int(i) for i in range(45, 61)]
    }
    hours, minutes = map(int, f'{time_str[1:] if time_str.startswith("0") else time_str}'.split(':'))
    res_str += f"{[f'{hbold(item)} {s}' for s, mass in data_hours.items() for item in mass if item == hours][0]},  "
    res_str += [f'{hbold(item)} {s}' for s, mass in data_minutes.items() for item in mass if item == minutes][0]
    return res_str