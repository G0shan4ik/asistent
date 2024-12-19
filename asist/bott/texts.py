from random import choice
from aiogram.utils.markdown import hbold


# GLOBAL
rand_animal_emoji = lambda : choice(['🦅', '🐝', '🐥', '🐨', '🦁', '🐰', '🦊', '🐼', '🐷', '🐸', '🐙', '🦖', '🦐', '🐳', '🐬', '🐊', '🦧', '🐉', '🐁', '🦥', '🦩', '🦜', '🦤'])


#GREET
GREET_TEXT = ["What's up bro ✋", f'Я готов к работе {rand_animal_emoji()}']


#FINANCES
pretty_courses_test = lambda d_r_ru, d_r_by, r_ru_by: \
    f'''
{hbold("USD")} 💵
————————
Сдать  Купить
{d_r_by[0]}   {d_r_by[-1]}
————————


{hbold("USD / RUB")} 💰 
————————
Сдать  Купить
{d_r_ru[0]}     {d_r_ru[-1]}
————————


{hbold("RUB / BUN")} 💸
————————
Сдать  Купить
{r_ru_by[0]}   {r_ru_by[-1]}
————————
    '''
