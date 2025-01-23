import asyncio
import datetime
from pprint import pprint

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter, ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from bot import bot
from config import ADMIN_IDS
from db.util import add_user_to_db, update_user_credit, update_user_ipoteka, update_user_house, update_user_auto, \
    update_user_sdelki, update_user_pay_credit, update_user_debit, update_user_blocked, update_user_unblocked, \
    get_all_users_unblock, update_user_phone, get_all_users
from keyboard import create_kb, contact_keyboard, kb_button
from spread import get_sheet

router =Router()

#1
#2


class FSMFillForm(StatesGroup):
    get_phone = State()
    send = State()
    text_add_button = State()
    check_text_1 = State()
    check_text_2 = State()
    text_add_button_text = State()
    text_add_button_url = State()
    photo_add_button = State()
    check_photo_1 = State()
    check_photo_2 = State()
    photo_add_button_text = State()
    photo_add_button_url = State()
    video_add_button = State()
    check_video_1 = State()
    check_video_2 = State()
    video_add_button_text = State()
    video_add_button_url = State()
    check_video_note_1 = State()


async def scheduler(time):
    while True:
        await asyncio.sleep(10)
        print(datetime.datetime.now())
        try:
            sheet = await get_sheet()
            sheet.clear()
            user_list = get_all_users()
            sheet.append_rows(user_list)
            print(datetime.datetime.now())
        except Exception as e:
            await bot.send_message(1012882762, str(e))
        await asyncio.sleep(time)


@router.message(CommandStart())
async def process_start_user(message: Message):
    add_user_to_db(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        datetime.datetime.now()
    )
    # await message.answer_video_note('DQACAgIAAxkBAAICCmeOgtXtspSZ2nff7NBPKOadJYUYAALCXAACOT9QSEfiMEII4PH0NgQ')
    await asyncio.sleep(0.3)
    await message.answer(
        text="""
<b>Здравствуйте, это бот Руслана Авдеева</b>👋🏻

Здесь вы сможете, буквально, за 1 минуту онлайн проверить свою ситуацию <b>подходит ли она под списание долгов через банкротство.</b>

Чтобы начать проверку, жмите на кнопку👇🏻
        """,
        parse_mode=ParseMode.HTML,
        reply_markup=create_kb(1, step_1="✅Пройти проверку")
    )


@router.callback_query(F.data == 'step_1')
async def step_1(cb: CallbackQuery):
    await cb.message.answer(text="""
Отлично, начинаем онлайн-проверку на возможность списания долгов в вашем случае.  
  
✅ Занимает не более минуты и дает четкий ответ - поможет вам законное списание долгов или лучше отказаться от этой идеи.    
    """)
    await asyncio.sleep(0.3)
    await cb.message.answer(text="""
<b>Подскажите, какая у Вас общая сумма ВСЕХ кредитов и долгов?</b>🤔  
  
Нужно сложить вместе: кредиты, ипотеки, автокредиты, микрозаймы, налоги, ЖКХ, кредитные карты.  
  
Выберите подходящий вам вариант из списка ниже, нажав на него👇 
        """,
                            parse_mode=ParseMode.HTML,
                            reply_markup=create_kb(1,
                                                   step_2_no="Менее 300 тыс.",
                                                   step_2_1_yes="300-500 тыс.",
                                                   step_2_2_yes="500 тыс.- 1 млн.",
                                                   step_2_3_yes="Более 1 млн."
                                                   ))


@router.callback_query(F.data == 'step_2_no')
async def step_2_no(cb: CallbackQuery):
    await cb.message.answer(text="Правильно понимаю, что если суммировать все ваши долги, кредиты и займы с процентами, штрафами и пенями, то все равно будет <b>менее 300 тыс. рублей?</b>",
                            parse_mode=ParseMode.HTML,
                            reply_markup=create_kb(1,
                                                   step_2_2_no="Да, менее 300 тыс.",
                                                   step_2_4_yes="Более 300 тыс."
                                                   ))


@router.callback_query(F.data == 'step_2_2_no')
async def step_2_2_no(cb: CallbackQuery):
    update_user_credit(cb.from_user.id, 'менее 300 тыс.')
    await cb.message.answer(text="""
Ваша сумма задолженности слишком мала для прохождения судебной процедуры банкротства.  
  
Но в таком случае вы можете рассмотреть банкротство через МФЦ.    
    """)


@router.callback_query(F.data.in_({'step_2_1_yes', 'step_2_2_yes', 'step_2_3_yes', 'step_2_4_yes'}))
async def step_3(cb: CallbackQuery):
    if F.data == 'step_2_1_yes':
        update_user_credit(cb.from_user.id, '300-500 тыс.')
    elif F.data == 'step_2_2_yes':
        update_user_credit(cb.from_user.id, '500 тыс.- 1 млн.')
    elif F.data == 'step_2_3_yes':
        update_user_credit(cb.from_user.id, 'Более 1 млн.')
    else:
        update_user_credit(cb.from_user.id, 'Более 300 тыс.')
    await cb.message.answer(text="""
<b>Есть ли у Вас ипотека?</b>  
  
Или может быть Вы являетесь созаемщиком по ипотеке?  
    """,
                            parse_mode=ParseMode.HTML,
                            reply_markup=create_kb(1,
                                                   step_3_1="Нет ипотеки⛔️",
                                                   step_3_2="Есть ипотека✅",
                                                   step_3_3="Я созаемщик🙋🏻‍♂️",
                            ))


@router.callback_query(F.data.in_({'step_3_1', 'step_3_2', 'step_3_3'}))
async def step_4(cb: CallbackQuery):
    if F.data == 'step_3_1':
        update_user_ipoteka(cb.from_user.id, 'Нет ипотеки')
    elif F.data == 'step_3_2':
        update_user_ipoteka(cb.from_user.id, 'Есть ипотека')
    else:
        update_user_ipoteka(cb.from_user.id, 'Я созаемщик')
    await cb.message.answer(text="""
Теперь разберемся с вашим имуществом. Начнем с недвижимости🏠  
  
<b>Какое недвижимое имущество зарегистрировано на вас?</b>
    """,
                            parse_mode=ParseMode.HTML,
                            reply_markup=create_kb(1,
                                                   step_4_1="Нет недвижимости",
                                                   step_4_2="Единственное жилье",
                                                   step_4_many="Несколько объектов🏘",
                                                   ))


@router.callback_query(F.data == 'step_4_many')
async def step_4_no(cb: CallbackQuery):
    await cb.message.answer(text="Правильно понимаю, что у Вас несколько объектов недвижимости?",
                            parse_mode=ParseMode.HTML,
                            reply_markup=create_kb(1,
                                                   step_4_4_no="Да, несколько",
                                                   step_4_2="Только единственное жилье"
                                                   ))


@router.callback_query(F.data == 'step_4_4_no')
async def step_4_4_no(cb: CallbackQuery):
    update_user_house(cb.from_user.id, 'Несколько объектов недвижимости')
    await cb.message.answer(text="""
Если у вас действительно несколько объектов недвижимости, тогда банкротство будет вам не выгодно, потому что при банкротстве можно сохранить только единственное жилье.  
  
Другие объекты недвижимости будут проданы с торгов при банкротстве. 
  
Но если ваша ситуация индививдульная и вы хотели бы проконсультироваться лично, то пишите свой вопрос мне в личку.  
  
Мой личный телеграмм @urist_ruslanavdeev    
    """)


@router.callback_query(F.data.in_({'step_4_1', 'step_4_2'}))
async def step_5(cb: CallbackQuery):
    if F.data == 'step_4_1':
        update_user_house(cb.from_user.id, 'Нет недвижимости')
    else:
        update_user_house(cb.from_user.id, 'Единственное жилье')
    await cb.message.answer(text="""
Теперь к автомобилям...

<b>На вас зарегистрирован автомобиль?</b> Выберите подходящий ответ.
    """,
                            parse_mode=ParseMode.HTML,
                            reply_markup=create_kb(1,
                                                   step_5_1="Нет автомобиля",
                                                   step_5_2="Есть, стоимость менее 300 тыс.",
                                                   step_5_3="Есть, стоимость более 300 тыс.",
                                                   ))


@router.callback_query(F.data.in_({'step_5_1', 'step_5_2', 'step_5_3'}))
async def step_6(cb: CallbackQuery):
    if F.data == 'step_5_1':
        update_user_auto(cb.from_user.id, 'Нет автомобиля')
    elif F.data == 'step_5_2':
        update_user_auto(cb.from_user.id, 'Есть, стоимость менее 300 тыс.')
    else:
        update_user_auto(cb.from_user.id, 'Есть, стоимость более 300 тыс.')
    await cb.message.answer(text="""
<b>За последние 3 года у вас были сделки с имуществом?</b>  
  
Например - покупка, продажа, дарение или наследование.
    """,
                            parse_mode=ParseMode.HTML,
                            reply_markup=create_kb(1,
                                                   step_6_1="Да, были сделки",
                                                   step_6_2="Не было сделок",
                                                   ))


@router.callback_query(F.data.in_({'step_6_1', 'step_6_2'}))
async def step_7(cb: CallbackQuery):
    if F.data == 'step_6_1':
        update_user_sdelki(cb.from_user.id, 'Да, были сделки')
    else:
        update_user_sdelki(cb.from_user.id, 'Не было сделок')
    await cb.message.answer(text="""
Какой у Вас ежемесячный платеж по всем кредитам, кредитным картам, микрозаймам и иным долгам?
    """,
                            parse_mode=ParseMode.HTML,
                            reply_markup=create_kb(1,
                                                   step_7_1="До 10 тыс. руб",
                                                   step_7_2="от 10 до 20 тыс. руб",
                                                   step_7_3="от 20 до 30 тыс. руб",
                                                   step_7_4="от 30 до 50 тыс. руб",
                                                   step_7_5="Более 50 тыс. руб"
                                                   ))


@router.callback_query(F.data.in_({'step_7_1', 'step_7_2', 'step_7_3', 'step_7_4', 'step_7_5'}))
async def step_8(cb: CallbackQuery):
    if F.data == 'step_7_1':
        update_user_pay_credit(cb.from_user.id, 'До 10 тыс. руб')
    elif F.data == 'step_7_2':
        update_user_pay_credit(cb.from_user.id, 'от 10 до 20 тыс. руб')
    elif F.data == 'step_7_3':
        update_user_pay_credit(cb.from_user.id, 'от 20 до 30 тыс. руб')
    elif F.data == 'step_7_4':
        update_user_pay_credit(cb.from_user.id, 'от 30 до 50 тыс. руб')
    else:
        update_user_pay_credit(cb.from_user.id, 'Более 50 тыс. руб')
    await cb.message.answer(text="""
<b>И заключительный вопрос!</b>  
Какой у Вас официальный доход?
    """,
                            parse_mode=ParseMode.HTML,
                            reply_markup=create_kb(1,
                                                   step_8_1="Нет официального дохода",
                                                   step_8_2="До 10 тыс. руб",
                                                   step_8_3="от 10 до 20 тыс. руб",
                                                   step_8_4="от 20 до 40 тыс. руб",
                                                   step_8_5="Более 40 тыс. руб"
                                                   ))


@router.callback_query(F.data.in_({'step_8_1', 'step_8_2', 'step_8_3', 'step_8_4', 'step_8_5'}), StateFilter(default_state))
async def step_9(cb: CallbackQuery, state: FSMContext):
    if F.data == 'step_8_1':
        update_user_debit(cb.from_user.id, 'Нет официального дохода')
    elif F.data == 'step_8_2':
        update_user_debit(cb.from_user.id, 'До 10 тыс. руб')
    elif F.data == 'step_8_3':
        update_user_debit(cb.from_user.id, 'от 10 до 20 тыс. руб')
    elif F.data == 'step_8_4':
        update_user_debit(cb.from_user.id, 'от 20 до 40 тыс. руб')
    else:
        update_user_debit(cb.from_user.id, 'Более 40 тыс. руб')
    await cb.message.answer('Проверяем Ваши ответы...')
    await asyncio.sleep(2)
    #await cb.message.answer_video_note()
    await cb.message.answer(text="""
<b>Поздравляю🔥 Вы прошли тест!</b> 
  
В вашем случае с вероятностью 99% можно списать долги ✅  
  
Почему вы получили это сообщение? 
  
Этот мини-тест устроен таким образом, что анализирует ваши ответы и только 30% людей доходят до этого этапа и получают сообщение о том, что им подходит списание долгов!
    """,
                            parse_mode=ParseMode.HTML)
    await cb.message.answer(text="""
<b>Предлагаю записаться на мою телефонную бесплатную консультацию.</b>  
  
На консультации я ЛИЧНО до конца проанализирую Ваше дело и смогу дать уже 100% гарантию списания долгов и главное смогу предложить Вам конкретные способы списания долгов, которые помогут именно в вашем случае.  
  
Для записи на консультацию напишите Ваш контактный номер телефона с +7 или с 8 ответным сообщением ⬇️
        """,
                            parse_mode=ParseMode.HTML,
                            reply_markup=await contact_keyboard())
    await state.set_state(FSMFillForm.get_phone)


@router.message(F.text, StateFilter(FSMFillForm.get_phone))
async def get_phone_text(message: types.Message, state: FSMContext):
    phone = str(message.text)
    update_user_phone(message.from_user.id, phone)
    await message.answer(text="""
<b>Спасибо!</b>  
  
Скоро я напишу вам на WhatsApp и договоримся об удобном для вас времени консультации🤝  
  
Запишите, пожалуйста, мой номер, чтобы я мог с вами связаться 7777777777
            """,
                         parse_mode=ParseMode.HTML)
    await state.set_state(default_state)


@router.message(F.contact, StateFilter(FSMFillForm.get_phone))
async def get_phone_contact(message: types.Message, state: FSMContext):
    phone = str(message.contact.phone_number)
    update_user_phone(message.from_user.id, phone)
    await message.answer(text="""
<b>Спасибо!</b>  

Скоро я напишу вам на WhatsApp и договоримся об удобном для вас времени консультации🤝  

Запишите, пожалуйста, мой номер, чтобы я мог с вами связаться 77777777777
            """,
                         parse_mode=ParseMode.HTML)
    await state.set_state(default_state)


#Команда для рассылки


@router.message(F.text == 'Send', StateFilter(default_state), F.from_user.id.in_(ADMIN_IDS))
async def send_to_all(message: types.Message, state: FSMContext):
    await message.answer(text='Сейчас мы подготовим сообщение для рассылки по юзерам!\n'
                              'Отправьте пжл текстовое сообщение или картинку(можно с текстом) или видео(можно с текстом) или видео-кружок')
    await state.set_state(FSMFillForm.send)


#Создание текстового сообщения


@router.message(F.text, StateFilter(FSMFillForm.send), F.from_user.id.in_(ADMIN_IDS))
async def text_add_button(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(text='Добавим кнопку-ссылку?', reply_markup=create_kb(2, yes='Да', no='Нет'))
    await state.set_state(FSMFillForm.text_add_button)


@router.callback_query(F.data == 'no', StateFilter(FSMFillForm.text_add_button), F.from_user.id.in_(ADMIN_IDS))
async def text_add_button_no(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    await cb.message.answer(text='Проверьте ваше сообщение для отправки')
    await cb.message.answer(text=dct['text'])
    await cb.message.answer(text='Отправляем?', reply_markup=create_kb(2, yes='Да', no='Нет'))
    await state.set_state(FSMFillForm.check_text_1)


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.check_text_1), F.from_user.id.in_(ADMIN_IDS))
async def check_text_yes_1(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    users = get_all_users_unblock()
    count = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text=dct['text'])
            count += 1
        except Exception as e:
            await bot.send_message(1012882762, str(e))
            await bot.send_message(1012882762, str(user_id))
    await cb.message.answer(text=f'Сообщение отправлено {count} юзерам')
    await state.set_state(default_state)
    await state.clear()


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.text_add_button), F.from_user.id.in_(ADMIN_IDS))
async def text_add_button_yes_1(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer(text='Введите текст кнопки-ссылки')
    await state.set_state(FSMFillForm.text_add_button_text)


@router.message(F.text, StateFilter(FSMFillForm.text_add_button_text), F.from_user.id.in_(ADMIN_IDS))
async def text_add_button_yes_2(message: types.Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    await message.answer(text='Теперь введите корректный url(ссылка на сайт, телеграмм)')
    await state.set_state(FSMFillForm.text_add_button_url)


@router.message(F.text, StateFilter(FSMFillForm.text_add_button_url), F.from_user.id.in_(ADMIN_IDS))
async def text_add_button_yes_3(message: types.Message, state: FSMContext):
    await state.update_data(button_url=message.text)
    dct = await state.get_data()
    try:
        await message.answer(text='Проверьте ваше сообщение для отправки')
        await message.answer(text=dct['text'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
        await message.answer(text='Отправляем?', reply_markup=create_kb(2, yes='Да', no='Нет'))
        await state.set_state(FSMFillForm.check_text_2)
    except Exception:
        await message.answer(text='Скорее всего вы ввели не корректный url. Направьте корректный url')
        await state.set_state(FSMFillForm.text_add_button_url)


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.check_text_2), F.from_user.id.in_(ADMIN_IDS))
async def check_text_yes_2(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    users = get_all_users_unblock()
    count = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text=dct['text'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
            count += 1
        except Exception as e:
            await bot.send_message(1012882762, str(e))
            await bot.send_message(1012882762, str(user_id))
    await cb.message.answer(text=f'Сообщение отправлено {count} юзерам')
    await state.set_state(default_state)
    await state.clear()


@router.callback_query(F.data == 'no', StateFilter(FSMFillForm.check_text_1, FSMFillForm.check_text_2), F.from_user.id.in_(ADMIN_IDS))
async def check_message_no(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer(text=f'Сообщение не отправлено')
    await state.set_state(default_state)
    await state.clear()


#Создание фото-сообщения


@router.message(F.photo, StateFilter(FSMFillForm.send), F.from_user.id.in_(ADMIN_IDS))
async def photo_add_button(message: types.Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    try:
        await state.update_data(caption=message.caption)
    except Exception:
        pass
    await message.answer(text='Добавим кнопку-ссылку?', reply_markup=create_kb(2, yes='Да', no='Нет'))
    await state.set_state(FSMFillForm.photo_add_button)


@router.callback_query(F.data == 'no', StateFilter(FSMFillForm.photo_add_button), F.from_user.id.in_(ADMIN_IDS))
async def text_add_button_no(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    pprint(dct)
    await cb.message.answer(text='Проверьте ваше сообщение для отправки')
    if dct.get('caption'):
        await cb.message.answer_photo(photo=dct['photo_id'], caption=dct['caption'])
    else:
        await cb.message.answer_photo(photo=dct['photo_id'])
    await cb.message.answer(text='Отправляем?', reply_markup=create_kb(2, yes='Да', no='Нет'))
    await state.set_state(FSMFillForm.check_photo_1)


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.check_photo_1), F.from_user.id.in_(ADMIN_IDS))
async def check_photo_yes_1(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    users = get_all_users_unblock()
    count = 0
    for user_id in users:
        try:
            if dct.get('caption'):
                await bot.send_photo(user_id, photo=dct['photo_id'], caption=dct['caption'])
            else:
                await bot.send_photo(user_id, photo=dct['photo_id'])
            count += 1
        except Exception as e:
            await bot.send_message(1012882762, str(e))
            await bot.send_message(1012882762, str(user_id))
    await cb.message.answer(text=f'Сообщение отправлено {count} юзерам')
    await state.set_state(default_state)
    await state.clear()


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.photo_add_button), F.from_user.id.in_(ADMIN_IDS))
async def photo_add_button_yes_1(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer(text='Введите текст кнопки-ссылки')
    await state.set_state(FSMFillForm.photo_add_button_text)


@router.message(F.text, StateFilter(FSMFillForm.photo_add_button_text), F.from_user.id.in_(ADMIN_IDS))
async def photo_add_button_yes_2(message: types.Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    await message.answer(text='Теперь введите корректный url(ссылка на сайт, телеграмм)')
    await state.set_state(FSMFillForm.photo_add_button_url)


@router.message(F.text, StateFilter(FSMFillForm.photo_add_button_url), F.from_user.id.in_(ADMIN_IDS))
async def photo_add_button_yes_3(message: types.Message, state: FSMContext):
    await state.update_data(button_url=message.text)
    dct = await state.get_data()
    try:
        await message.answer(text='Проверьте ваше сообщение для отправки')
        if dct.get('caption'):
            await message.answer_photo(photo=dct['photo_id'], caption=dct['caption'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
        else:
            await message.answer_photo(photo=dct['photo_id'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
        await message.answer(text='Отправляем?', reply_markup=create_kb(2, yes='Да', no='Нет'))
        await state.set_state(FSMFillForm.check_photo_2)
    except Exception as e:
        print(e)
        await message.answer(text='Скорее всего вы ввели не корректный url. Направьте корректный url')
        await state.set_state(FSMFillForm.photo_add_button_url)


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.check_photo_2), F.from_user.id.in_(ADMIN_IDS))
async def check_photo_yes_2(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    users = get_all_users_unblock()
    count = 0
    for user_id in users:
        try:
            if dct.get('caption'):
                    await bot.send_photo(user_id, photo=dct['photo_id'], caption=dct['caption'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
            else:
                await bot.send_photo(user_id, photo=dct['photo_id'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
            count += 1
        except Exception as e:
            await bot.send_message(1012882762, str(e))
            await bot.send_message(1012882762, str(user_id))
    await cb.message.answer(text=f'Сообщение отправлено {count} юзерам')
    await state.set_state(default_state)
    await state.clear()


@router.callback_query(F.data == 'no', StateFilter(FSMFillForm.check_text_1, FSMFillForm.check_text_2,
            FSMFillForm.check_photo_1, FSMFillForm.check_photo_2), F.from_user.id.in_(ADMIN_IDS))
async def check_message_no(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer(text=f'Сообщение не отправлено')
    await state.set_state(default_state)
    await state.clear()


#Создание видео-сообщения


@router.message(F.video, StateFilter(FSMFillForm.send), F.from_user.id.in_(ADMIN_IDS))
async def video_add_button(message: types.Message, state: FSMContext):
    await state.update_data(video_id=message.video.file_id)
    try:
        await state.update_data(caption=message.caption)
    except Exception:
        pass
    await message.answer(text='Добавим кнопку-ссылку?', reply_markup=create_kb(2, yes='Да', no='Нет'))
    await state.set_state(FSMFillForm.video_add_button)


@router.callback_query(F.data == 'no', StateFilter(FSMFillForm.video_add_button), F.from_user.id.in_(ADMIN_IDS))
async def video_add_button_no(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    pprint(dct)
    await cb.message.answer(text='Проверьте ваше сообщение для отправки')
    if dct.get('caption'):
        await cb.message.answer_video(video=dct['video_id'], caption=dct['caption'])
    else:
        await cb.message.answer_video(video=dct['video_id'])
    await cb.message.answer(text='Отправляем?', reply_markup=create_kb(2, yes='Да', no='Нет'))
    await state.set_state(FSMFillForm.check_video_1)


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.check_video_1), F.from_user.id.in_(ADMIN_IDS))
async def check_video_yes_1(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    users = get_all_users_unblock()
    count = 0
    for user_id in users:
        try:
            if dct.get('caption'):
                await bot.send_video(user_id, video=dct['video_id'], caption=dct['caption'])
            else:
                await bot.send_video(user_id, video=dct['video_id'])
            count += 1
        except Exception as e:
            await bot.send_message(1012882762, str(e))
            await bot.send_message(1012882762, str(user_id))
    await cb.message.answer(text=f'Сообщение отправлено {count} юзерам')
    await state.set_state(default_state)
    await state.clear()


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.video_add_button), F.from_user.id.in_(ADMIN_IDS))
async def video_add_button_yes_1(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer(text='Введите текст кнопки-ссылки')
    await state.set_state(FSMFillForm.video_add_button_text)


@router.message(F.text, StateFilter(FSMFillForm.video_add_button_text), F.from_user.id.in_(ADMIN_IDS))
async def video_add_button_yes_2(message: types.Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    await message.answer(text='Теперь введите корректный url(ссылка на сайт, телеграмм)')
    await state.set_state(FSMFillForm.video_add_button_url)


@router.message(F.text, StateFilter(FSMFillForm.video_add_button_url), F.from_user.id.in_(ADMIN_IDS))
async def video_add_button_yes_3(message: types.Message, state: FSMContext):
    await state.update_data(button_url=message.text)
    dct = await state.get_data()
    try:
        await message.answer(text='Проверьте ваше сообщение для отправки')
        if dct.get('caption'):
            await message.answer_video(video=dct['video_id'], caption=dct['caption'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
        else:
            await message.answer_video(video=dct['video_id'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
        await message.answer(text='Отправляем?', reply_markup=create_kb(2, yes='Да', no='Нет'))
        await state.set_state(FSMFillForm.check_video_2)
    except Exception as e:
        print(e)
        await message.answer(text='Скорее всего вы ввели не корректный url. Направьте корректный url')
        await state.set_state(FSMFillForm.video_add_button_url)


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.check_video_2), F.from_user.id.in_(ADMIN_IDS))
async def check_video_yes_2(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    users = get_all_users_unblock()
    count = 0
    for user_id in users:
        try:
            if dct.get('caption'):
                await bot.send_video(user_id, video=dct['video_id'], caption=dct['caption'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
            else:
                await bot.send_video(user_id, photo=dct['video_id'], reply_markup=kb_button(dct['button_text'], dct['button_url']))
            count += 1
        except Exception as e:
            await bot.send_message(1012882762, str(e))
            await bot.send_message(1012882762, str(user_id))
    await cb.message.answer(text=f'Сообщение отправлено {count} юзерам')
    await state.set_state(default_state)
    await state.clear()


#Создание видео-кружка


@router.message(F.video_note, StateFilter(FSMFillForm.send), F.from_user.id.in_(ADMIN_IDS))
async def video_note_check(message: types.Message, state: FSMContext):
    await state.update_data(video_note_id=message.video_note.file_id)
    await message.answer(text='Проверьте вашу запись в кружке для отправки')
    await message.answer(text='Отправляем?', reply_markup=create_kb(2, yes='Да', no='Нет'))
    await state.set_state(FSMFillForm.check_video_note_1)


@router.callback_query(F.data == 'yes', StateFilter(FSMFillForm.check_video_note_1), F.from_user.id.in_(ADMIN_IDS))
async def check_video_note_yes_1(cb: types.CallbackQuery, state: FSMContext):
    dct = await state.get_data()
    users = get_all_users_unblock()
    count = 0
    for user_id in users:
        try:
            await bot.send_video_note(user_id, video_note=dct['video_note_id'])
        except Exception as e:
            await bot.send_message(1012882762, str(e))
            await bot.send_message(1012882762, str(user_id))
    await cb.message.answer(text=f'Сообщение отправлено {count} юзерам')
    await state.set_state(default_state)
    await state.clear()


# Выход из рассылки без отправки


@router.callback_query(F.data == 'no', StateFilter(FSMFillForm.check_text_1, FSMFillForm.check_text_2,
                       FSMFillForm.check_photo_1, FSMFillForm.check_photo_2, FSMFillForm.check_video_1,
                       FSMFillForm.check_video_2, FSMFillForm.check_video_note_1), F.from_user.id.in_(ADMIN_IDS))
async def check_message_no(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer(text=f'Сообщение не отправлено')
    await state.set_state(default_state)
    await state.clear()


#Ручки на блокировку/разблокировку


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    update_user_blocked(event.from_user.id)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated):
    update_user_unblocked(event.from_user.id)


@router.message(F.video_note, F.from_user.id.in_(ADMIN_IDS))
async def get_note(message: types.Message):
    print(message.video_note.file_id)
