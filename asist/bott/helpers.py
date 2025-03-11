import datetime
import asyncio
from typing import Optional
from calendar import monthcalendar

from .include import hbold, CurrencyMixin


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class TimeManager:
    def __init__(self, input_time: str):
        self.input_time: str = input_time

    def time_difference(self) -> str:
        minsk_timezone = datetime.timezone(datetime.timedelta(hours=3))

        current_datetime = datetime.datetime.now(minsk_timezone)
        current_time = current_datetime.strftime('%H:%M')

        current_hours, current_minutes = map(int, current_time.split(':'))
        input_hours, input_minutes = map(int, self.input_time.split(':'))

        current_time_in_minutes = current_hours * 60 + current_minutes
        input_time_in_minutes = input_hours * 60 + input_minutes

        difference_in_minutes = (input_time_in_minutes - current_time_in_minutes) % (24 * 60)

        difference_hours = difference_in_minutes // 60
        difference_minutes = difference_in_minutes % 60

        return f"{difference_hours:02d}:{difference_minutes:02d}"

    @staticmethod
    def time_to_text(time_str: str) -> str:
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

    def run_time_difference(self) -> str:
        return self.time_to_text(self.time_difference())

    @staticmethod
    def get_belarus_time_string() -> str:
        minsk_utc_offset = 3

        current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=minsk_utc_offset)
        return current_time.strftime("%H:%M %d.%m.%Y")


async def update_currency() -> None:
    while True:
        async with CurrencyMixin() as client:
            await client.get_or_create_currency()

        await asyncio.sleep(40420)


def get_chunk_buttons(data: Optional[list[dict]]) -> list[list[dict]]:
    if data:
        return [item for item in chunks(data, 6)] if len(data) > 8 else [data]
    return []


def get_month_calendar(year: int, month: str, check_in_dates: list) -> str:
    month_names = {
        "январь": 1, "февраль": 2, "март": 3, "апрель": 4, "май": 5, "июнь": 6,
        "июль": 7, "август": 8, "сентябрь": 9, "октябрь": 10, "ноябрь": 11, "декабрь": 12
    }
    month_number = month_names.get(month.lower())

    cal = monthcalendar(year, month_number)
    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

    check_in_dates = set(map(int, check_in_dates))

    result = f"{month.capitalize()} {year}\n" + " | ".join(week_days) + "\n"
    result += "-" * 37 + "\n"

    for week in cal:
        formatted_week = []
        for day in week:
            if day == 0:
                formatted_week.append("  ")
            elif day in check_in_dates:
                formatted_week.append("✅")
            else:
                formatted_week.append(f"{day:2}")
        result += " | ".join(formatted_week) + "\n"

    return f"<pre>{result.strip()}</pre>"

def get_year_month(third_arg: dict) -> list:
    y_m = get_current_year_month()

    arg: list = third_arg.get(f"{y_m[0]}#{y_m[-1]}", [])
    return [y_m[0], y_m[-1], arg]

def get_today_date() -> int:
    now = datetime.datetime.now()
    return int(now.strftime('%d'))

def get_current_year_month() -> list:
    months = [
        "январь", "февраль", "март", "апрель", "май", "июнь",
        "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
    ]
    now = datetime.datetime.now()
    return [now.strftime('%Y'), months[now.month - 1]]


def get_month_btn(dct: dict, year: int, month: str, _check_in_id: int) -> dict:
    btn = {
        'Удалить🗑': f'delete_check_in#{_check_in_id}'
    }
    y_m = get_current_year_month()
    if year == y_m[0] and month == y_m[-1]:
        btn = {
            '✅': f'_check_in_True#{_check_in_id}#{year}#{month}',
            'Убрать галочку': f'_check_in_False#{_check_in_id}#{year}#{month}',
            **btn
        }
    len_dct: int = len(dct)
    idx: int = list(dct.keys()).index(f'{year}#{month}')

    if len_dct > 1:
        if idx - 1 >= 0 and idx + 2 > len_dct:
            btn = {
                '«': f"skip#{list(dct.keys())[idx - 1]}#{_check_in_id}",
                **btn
            }
        elif idx - 1 >= 0 and idx + 1 <= len_dct:
            btn = {
                '«': f"skip#{list(dct.keys())[idx - 1]}#{_check_in_id}",
                '»': f"skip#{list(dct.keys())[idx + 1]}#{_check_in_id}",
                **btn
            }
        elif idx - 1 < 0 and idx + 1 <= len_dct:
            btn = {
                '»': f"skip#{list(dct.keys())[idx + 1]}#{_check_in_id}",
                **btn
            }


    return btn