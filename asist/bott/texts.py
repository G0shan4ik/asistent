from random import choice

from aiogram.utils.markdown import hbold

import datetime
import locale
import re


def count_length(text: str) -> str:
    reference_text = "Банк покупает  "
    space_per_char = 1.5  # Количество пробелов на символ (подбирается эмпирически)

    diff = len(reference_text) - len(text)
    spaces = int(diff * space_per_char)

    return ' ' * max(spaces, 0) + '  ' + '  '

# GLOBAL
rand_animal_emoji = lambda : choice(['🦅', '🐝', '🐥', '🐨', '🦁', '🐰', '🦊', '🐼', '🐷', '🐸', '🐙', '🦖', '🐳', '🐬', '🐊', '🦧', '🐉', '🐁', '🦥', '🦩', '🦜', '🦤'])


#GREET
GREET_TEXT = [hbold("What's up bro ✋"), f'Я готов к работе {rand_animal_emoji()}']


#FINANCES
pretty_courses_test = lambda data: \
f'''
USD 💵
——————————————
Банк покупает  Банк продает
{data["USD_in"]}{count_length(str(data["USD_in"]))}{data["USD_out"]}
——————————————

EUR 💶
——————————————
Банк покупает  Банк продает
{data["EUR_in"]}{count_length(str(data["EUR_in"]))}{data["EUR_out"]}
——————————————


RUB / BUN 💸
——————————————
Банк покупает  Банк продает
{data["RUB_in"]}{count_length(str(data["RUB_in"]))}{data["RUB_out"]}
——————————————


USD -> RUB (конверсия) 💰
——————————————
Банк покупает  Банк продает
{data["USD_RUB_in"]}{count_length(str(data["USD_RUB_in"]))}{data["USD_RUB_out"]}
——————————————

RUB -> EUR (конверсия) 💰
——————————————
Банк покупает  Банк продает
{data["RUB_EUR_in"]}{count_length(str(data["RUB_EUR_in"]))}{data["RUB_EUR_out"]}
——————————————
'''


# ERROR Texts
WRONG_TEXT = "Что-то пошло не так🥲 ..."


# Currency text
CALCULATE_MENU = hbold('Выберите нужную валюту)')
CURRENCY_TEXT = lambda curr: f'Вы выбрали {hbold(curr)}\n\nВыберите дальнейшие действия:'
CURRENCY_TEXT2 = lambda curr_name, action, curr_value: (f'Вы выбрали {hbold(curr_name)} \n'
                                                f'({hbold(action)} по курсу = {hbold(curr_value)})\n\n'
                                                        f'Введите число...')
currency_dict = {
    'USD_in': '$',
    'USD_out': 'Br',

    'EUR_in': '€',
    'EUR_out': 'Br',

    'RUB_in': '₽',
    'RUB_out': 'Br',

    'USD_RUB_in': '$',
    'USD_RUB_out': '₽',

    'RUB_EUR_in': '₽',
    'RUB_EUR_out': '€',
}


#Check_in text
START_CHECK_IN_TEXT = lambda res: "Вот все ваши 'check_in':" if res else "У вас нет 'check_in', создайте его (нажмите на кнопку 'Создать check_in')"


# Debts text
NO_DEBTS_TEXT = f'{hbold("У вас нет долгов, поздравляю!!!")}\n\nУрааа 🎉🎉🎉🎉'
YES_DEBTS_TEXT = f'{hbold("Вот список ваших долгов :(  ⬇️")}'
DELETE_DEBT_TEXT = lambda bl: hbold("Долг успешно удален!") if bl else hbold("Возникла ошибка при удалении долга ❗️")
ERROR_SAVE_DEBT_TEXT = f"Вы {hbold('НЕ ЗАПОЛНИЛИ')} все обязательные поля для заполнения ('Название' и 'Сумма')❗️"
START_CREATE_DEBTS_TEXT = f'''
{hbold('-  Правила  СОЗДАНИЕ / ОФОРМЛЕНИЕ  долга:')}


1) {hbold("Обязательные поля для заполнения: ")} 'Название' и 'Сумма';

2) {hbold("Поля заполняются поочереди!")}

3) После того как вы заполнили какое либо поле, будет добавляться смайлик "✅" перед названием заполненного поля;

4) Если вы {hbold("НЕПРАВИЛЬНО заполнили поле")}, тогда нажмите на поле снова и заполните его заново;

5) Если вы {hbold("ПЕРЕДУМАЛИ 'создавать' долг")}, то просто нажмите на кнопку "Назад ↩️";
'''
UPDATE_DEBTS_TEXT = f'''
{hbold("Правила  ОБНОВЛЕНИЯ  долга:")}


1) {hbold("Поля заполняются поочереди!")} (можно заполнить любое количество полей);

2) После того как вы заполнили какое либо поле, будет добавляться смайлик "✅" перед названием заполненного поля;

3) Если вы {hbold("НЕПРАВИЛЬНО заполнили поле")}, тогда нажмите на поле снова и заполните его заново;

4) Если вы {hbold("ПЕРЕДУМАЛИ 'обновлять' долг")}, то просто нажмите на кнопку "Назад ↩️";
'''

# MINI DEBTS HELPERS FUNCTIONS
def convert_utc_to_belarus_local(utc_time_str: str) -> str:
    utc_dt = datetime.datetime.fromisoformat(utc_time_str).replace(tzinfo=datetime.timezone.utc)

    belarus_offset = datetime.timezone(datetime.timedelta(hours=3))

    local_dt = utc_dt.astimezone(belarus_offset)

    return local_dt.strftime("%Y-%m-%d / %H:%M:%S")


def subtract_datetimes(time1: str) -> str:
    try:
        dt1 = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
        dt2 = datetime.datetime.now()

        delta: datetime.timedelta = dt1 - dt2

        if delta.total_seconds() < 0:
            return "0 дней; 0 часов, 0 минут, 0 секунд;"

        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        return f"{days} дней; {hours} часов, {minutes} минут, {secs} секунд;"

    except Exception:
        return "0 дней; 0 часов, 0 минут, 0 секунд;"

# /MINI DEBTS HELPERS FUNCTIONS

priority_color = {
    'low': '🟢',
    'average': '🟡',
    'high': '🔴',
}

def DEBT_SETTINGS_TEXT(data: dict) -> str:
    string = f'{hbold("Название долга")}:  {data["title"]}\n'
    string += f'{hbold("ДАТА/ВРЕМЯ создания:")}  {convert_utc_to_belarus_local(data["created_at"])}\n\n'
    if data["due_date"]:
        string += f'- {hbold("Срок выплаты долга:")}  до {data["due_date"]};\n- {hbold("Осталось времени до конца срока: /")}\n      {subtract_datetimes(data["due_date"])}\n\n'
    else:
        string += f'- {hbold("Срок выплаты долга:")}  Не указан\n\n'
    string += f'- {hbold("Сумма долга:")}  {data["amount"]}\n\n'
    string += f'- {hbold("Приоритет:")}  {data["priority"]} ({priority_color.get(data["priority"] )})\n\n'
    if data["paid"]:
        string += f'- {hbold("Уже заплачено:")}  {data["paid"]} {data["amount"].split()[-1]}; {hbold("Остаток:")} {int(data["amount"].split()[0]) - int(data["paid"])} {data["amount"].split()[-1]}\n\n'
    else:
        string += f'- {hbold("Уже заплачено:")}  0; {hbold("Остаток:")}  {data["amount"]}\n\n'
    string += f'- {hbold("Примечание:")}  {data["notes"] if data["notes"] else "Не указано"}\n\n'

    return string

def CONSTRUCTOR_DEBT_INPUT_VALUE_TEXT(value_name: str) -> str:
    if value_name == 'title':
        return f'''{hbold('- Введите "Название" долга')}\n\nФормат ввода данных: любой'''
    elif value_name == 'amount':
        return f'''{hbold('- Введите "Сумму" долга')}\n\nФормат ввода данных (Сумма Валюта(BYN; USD; EUR; RUB)): \n1) 'Сумма' долга должно быть положительным числом\n2) Пример: 1000 USD'''
    elif value_name == 'paid':
        return f'''{hbold('- Введите "Сумма погашения" долга')}\n\nФормат ввода данных: \n1) 'Сумма' долга должно быть положительным числом; Пример: 15'''
    elif value_name == 'priority':
        return f'''{hbold('- Выберите "Приоритет" долга')}\n\nВыберите возможный из приоритетов на клавиатуре снизу ⬇️'''
    elif value_name == 'due_date':
        return \
            f'''{hbold('- Введите "Дату погашения" долга')}\n\nФормат ввода данных: 
1) день месяц; Пример: 1 марта
2) конкретный срок в днях; Пример: через 3 дня
'''
    elif value_name == 'is_closed':
        return f'''{hbold('- "Погашение долга"')}\n\nНажмите на кнопку 'ДА' ⬇️, чтобы погасить долг;'''
    elif value_name == 'notes':
        return f'''{hbold('- Выберите "Примечание" для долга')}\n\nФормат ввода данных: любой'''