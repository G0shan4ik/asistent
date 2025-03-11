from random import choice

from aiogram.utils.markdown import hbold

from PIL import ImageFont, ImageDraw, Image


# Functions (work with pretty text)
def count_length(text: str) -> str:
    font = ImageFont.truetype("/usr/share/fonts/truetype/arial.ttf", 14)

    image = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(image)

    bbox1 = draw.textbbox((0, 0), 'Банк покупает  ', font=font)
    width1 = bbox1[2] - bbox1[0]

    bbox2 = draw.textbbox((0, 0), text, font=font)
    width2 = bbox2[2] - bbox2[0]
    return int((width1 - width2) / 4) * ' ' + '  '


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
