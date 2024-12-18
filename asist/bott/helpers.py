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

    current_hours, current_minutes = map(int, current_time.split(':'))
    input_hours, input_minutes = map(int, input_time.split(':'))

    current_time_in_minutes = current_hours * 60 + current_minutes
    input_time_in_minutes = input_hours * 60 + input_minutes

    difference_in_minutes = (input_time_in_minutes - current_time_in_minutes) % (24 * 60)

    difference_hours = difference_in_minutes // 60
    difference_minutes = difference_in_minutes % 60

    return f"{difference_hours:02d}:{difference_minutes:02d}"

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