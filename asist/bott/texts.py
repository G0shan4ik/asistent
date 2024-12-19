from random import choice
from aiogram.utils.markdown import hbold


# GLOBAL
rand_animal_emoji = lambda : choice(['🦅', '🐝', '🐥', '🐨', '🦁', '🐰', '🦊', '🐼', '🐷', '🐸', '🐙', '🦖', '🦐', '🐳', '🐬', '🐊', '🦧', '🐉', '🐁', '🦥', '🦩', '🦜', '🦤'])


#GREET
GREET_TEXT = ["What's up bro ✋", f'Я готов к работе {rand_animal_emoji()}']


#FINANCES
pretty_courses_test = lambda d_r_ru, d_r_by, eu_ru_by, r_ru_by: \
    f'''
{hbold("USD")} 💵
——————————————
Банк покупает  Банк продает
{hbold(d_r_by[0])}{' '*(25-len(str(d_r_by[0])))}{hbold(d_r_by[-1])}
——————————————

{hbold("EUR")} 💶
——————————————
Банк покупает  Банк продает
{hbold(eu_ru_by[0])}{' '*(25-len(str(eu_ru_by[0])))}{hbold(eu_ru_by[-1])}
——————————————

{hbold("USD / RUB")} 💰 
——————————————
Банк покупает  Банк продает
{hbold(d_r_ru[0])}{' '*(23-len(str(d_r_ru[0])))}{hbold(d_r_ru[-1])}
——————————————


{hbold("RUB / BUN")} 💸
——————————————
Банк покупает  Банк продает
{hbold(r_ru_by[0])}{' '*(25-len(str(r_ru_by[0])))}{hbold(r_ru_by[-1])}
——————————————
    '''
