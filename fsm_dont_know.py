import sqlite3

from openpyxl import load_workbook
import pandas
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import keyboards
import values
import work_with_excel
from config import BOT_API
from keyboards import spec_keyboard
from values import trainings, questions, prof_test_data
import re

# Регулярное выражение для проверки URL
url_regex = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

bot = Bot(BOT_API)
router = Router()

con = sqlite3.connect("db.db")
cur = con.cursor()

class DontKnowInterestStates(StatesGroup):
    ans_id = State()
    name   = State()
    age    = State()
    city   = State()
    resume = State()
    prof_t = State()
    spec   = State()
    mater  = State()
    spec_c = State()

@router.callback_query(F.data == "new_talent")
async def new_talent_btn_handler(query: CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.clear()
    await state.set_state(DontKnowInterestStates.name)
    await state.update_data(ans_id=query.message.message_id+1)
    await bot.send_message(query.message.chat.id,
    "Отлично, мы всегда рады новичкам!\n"
         "Пожалуйста напишите ваше имя и фамилию\n"
         "Если хотите прервать заполнение формы - нажмите кнопку ниже",
         reply_markup=keyboards.interrupt_keyboard()
    )


@router.message(DontKnowInterestStates.name)
async def choosing_name_new_handler(msg: Message, state: FSMContext):
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])
    await state.update_data(name=msg.text)
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.edit_message_text(chat_id=msg.chat.id,
                                message_id=ans_id,
                                text="Прекрасно, теперь напишите ваш возраст в виде числа",
                                reply_markup=keyboards.interrupt_keyboard()
                                )
    await state.update_data(name=msg.text)
    await state.set_state(DontKnowInterestStates.age)


@router.message(DontKnowInterestStates.age)
async def choosing_age_new_handler(msg: Message, state: FSMContext):
    await bot.delete_message(msg.chat.id, msg.message_id)
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])
    try:
        age = int(msg.text)
        if not 18 <= age <= 100:
            raise ValueError
    except ValueError:
        msg_wrong_num = "Возраст должен быть числом от 18 до 100.\nПовторите ввод."
        await bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=ans_id,
            text=msg_wrong_num,
            reply_markup=keyboards.interrupt_keyboard()
        ) if msg.text != msg_wrong_num else ...
        return
    await state.update_data(age=age)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text="Теперь укажите город проживания",
        reply_markup=keyboards.interrupt_keyboard()
    )
    await state.set_state(DontKnowInterestStates.city)


@router.message(DontKnowInterestStates.city)
async def choosing_city_new_handler(msg: Message, state: FSMContext):
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])
    await state.update_data(city=msg.text)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text="Расскажите немного о себе (кратко).",
        reply_markup=keyboards.interrupt_keyboard()
    )
    await bot.delete_message(
        msg.chat.id,
        msg.message_id
    )
    await state.set_state(DontKnowInterestStates.resume)


@router.message(DontKnowInterestStates.resume)
async def choosing_resume_new_handler(msg: Message, state: FSMContext):
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])

    # Проверка, является ли введенная строка URL
    if not re.match(url_regex, msg.text):
        await bot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=ans_id,
            text="Пожалуйста, предоставьте корректный URL."
        )
        return

    await state.update_data(resume=msg.text)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text="Пожалуйста отправьте url на ваше портфолио.",
        reply_markup=keyboards.interrupt_keyboard()
    )
    await bot.delete_message(
        msg.chat.id,
        msg.message_id
    )
    await state.set_state(DontKnowInterestStates.exp)

@router.message(DontKnowInterestStates.prof_t)
async def choosing_professional_type_new_handler(msg: Message, state: FSMContext):
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])
    q_t = "".join([i+"\n" for i in questions[0].values()])
    await state.update_data(prof_t=msg.text)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text=f"Теперь предлагаю пройти профорентационный тест!\n{q_t}",
        reply_markup=keyboards.prof_orient_keyboard()
    )
    await bot.delete_message(
        msg.chat.id,
        msg.message_id
    )
    await state.set_state(DontKnowInterestStates.spec)


@router.callback_query(DontKnowInterestStates.spec)
async def choosing_specialization_new_handler(callback: Message, state: FSMContext):
    data = await state.get_data()
    ans_id = int(data["ans_id"])
    if not ("spec" in data):
        res = {callback.data: 1}
    elif not (callback.data in data["spec"].keys()):
        data["spec"].update({callback.data: 1})
        res = data["spec"]
    else:
        data["spec"].update({callback.data: data["spec"][callback.data]+1})
        res = data["spec"]

    await state.update_data(spec=res)
    text = "\n".join(questions[len(res)-1].values())
    if callback.message.text == text:
        await state.set_state(DontKnowInterestStates.mater)
        return
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=ans_id,
        text=text,
        reply_markup=keyboards.prof_orient_keyboard()
    )


@router.callback_query(DontKnowInterestStates.mater)
async def end_handler(callback: Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.send_message(
        callback.message.chat.id,
        f"Ваша анкета завершена:\n"
        f"Имя: {user_data['name']}\n"
        f"Возраст: {user_data['age']}\n"
        f"Город: {user_data['city']}\n"
        f"Резюме: {user_data['resume']}\n"
        f"По результатам профориентации мы решили, что больше всего вам подходит {", ".join([trainings[v] for v in prof_test_data[max(user_data['spec'], key=user_data['spec'].get)]])}"
        f"\n\nОстался последний шаг! Выберите направление",
        reply_markup=spec_keyboard()
    )
    await bot.send_message(
        callback.message.chat.id,
        open("spec.txt", "r").read()
    )
    await bot.send_message(
        callback.message.chat.id,
        "Вы можете получить больше полезной информации по ссылке -> https://career.kode.ru/"
    )
    await state.set_state(DontKnowInterestStates.spec_c)

@router.callback_query(F.data.startswith("spec_"))
async def choice(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    spec = values.trainings[callback.data.replace("spec_", "")]
    await bot.send_message(callback.message.chat.id, "Поздравляем, заявка успешно отправлена!")
    work_with_excel.create_excel_from_dict_list([{"Имя": data["name"],
                                                  "Возраст": data["age"],
                                                  "Город": data['city'],
                                                  "Имя пользователя": callback.message.from_user.id,
                                                  "Резюме": data["resume"],
                                                  "Специальность": spec
                                                  }], output_filename="talents.xlsx", sheet_name="MainSheet")


@router.callback_query(F.data=="interrupt")
async def interrupt_form(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, "Заполение формы было отменено, вы можете вернуться к ней в любой момент")
    await state.clear()
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
