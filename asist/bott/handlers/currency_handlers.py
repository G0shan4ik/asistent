from asist.bott.core import router, bot_
from asist.bott.mixins.currency_mixin import CurrencyMixin
from asist.bott.include import (
    FSMContext, CallbackQuery,
    CALCULATE_MENU, CURRENCY_TEXT, CURRENCY_TEXT2
)
from asist.bott.keyboards import constructor_kb
from .states.currency_state import CountMoneyState


@router.callback_query(lambda query: query.data.startswith('calculate'))
async def return_calculate_menu(query: CallbackQuery):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=CALCULATE_MENU,
        reply_markup=constructor_kb(
            data={
                "USD 💵": "Calculate#USD#USD_in-USD_out",
                "EUR 💶": "Calculate#EUR#EUR_in-EUR_out",
                "RUB / BUN 💸": "Calculate#RUB / BUN#RUB_in-RUB_out",
                "USD -> RUB (конверсия) 💰": "Calculate#USD -> RUB (конверсия)#USD_RUB_in-USD_RUB_out",
                "RUB -> EUR (конверсия) 💰": "Calculate#RUB -> EUR (конверсия)#RUB_EUR_in-RUB_EUR_out",
            },
            join=False,
            num=3,
            cancel=True,
            prefix_cancel='currency'
        )
    )


@router.callback_query(lambda query: query.data.startswith('Calculate#'))
async def start_calculate(query: CallbackQuery, state: FSMContext):
    await state.clear()

    async with CurrencyMixin() as session:
        data: dict = await session.select_currency()
    query_data: list[str] = query.data.split('#')[-1].split('-')
    __currency: [dict] = [data[query_data[0]], data[query_data[-1]]]
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=CURRENCY_TEXT(query.data.split('#')[1]),
        reply_markup=constructor_kb(
            data={
                "Сдать": f"transaction#{__currency[0]}#{query.data.split('#')[1]}#{query_data[0]}",
                "Купить": f"transaction#{__currency[-1]}#{query.data.split('#')[1]}#{query_data[-1]}",
            },
            join=False,
            num=2,
            cancel=True,
            prefix_cancel='calculate'
        )
    )

@router.callback_query(lambda query: query.data.startswith('transaction#'))
async def wait_num(query: CallbackQuery, state: FSMContext):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    query_data = query.data.split("#")[2:]
    txt = f'{query_data[-1]}-{query_data[-1].replace("in", "out")}' if "_in" in query_data[-1] else\
        f'{query_data[-1].replace("out", "in")}-{query_data[-1]}'

    __msg = await bot_.send_message(
        chat_id=query.message.chat.id,
        text=CURRENCY_TEXT2(
            curr_name=query.data.split("#")[2],
            action='Сдать' if 'in' in query_data[-1] else 'Купить',
            curr_value=query.data.split('#')[1]
        ),
        reply_markup=constructor_kb(
            cancel=True,
            prefix_cancel=f'Calculate#{query.data.split("#")[2]}#{txt}'
        )
    )

    await state.set_data(
        {
            'id': __msg.message_id,
            'rate': float(query.data.split('#')[1]),
            'action': query_data[-1],
            'currency': query.data.split('#')[-1],
            'main_text': CURRENCY_TEXT2(
                curr_name=query.data.split("#")[2],
                action='Сдать' if 'in' in query_data[-1] else 'Купить',
                curr_value=query.data.split('#')[1]
            ).replace('</b>', '').replace('<b>', ''),
            'kb_text': f'Calculate#{query.data.split("#")[2]}#{txt}'
        }
    )

    await state.set_state(CountMoneyState.wait_number)
