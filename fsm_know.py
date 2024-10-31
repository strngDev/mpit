from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import keyboards
from config import BOT_API
from keyboards import interupt_keyboard

bot = Bot(BOT_API)
router = Router()

class KnowInterestStates(StatesGroup):
    ans_id = State()
    name   = State()
    age    = State()
    city   = State()
    resume = State()
    exp    = State()


@router.callback_query(F.data == "pro_talent")
async def pro_talent_handler(callback: CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await state.clear()
    await state.update_data(ans_id=callback.message.message_id+1)
    await state.set_state(KnowInterestStates.name)
    await bot.send_message(callback.message.chat.id, "Отлично! Пожалуйста напишите вашу фамилию и имя", reply_markup=interupt_keyboard())

@router.message(KnowInterestStates.name)
async def name_pro_talent_handler(msg: Message, state: FSMContext):
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])
    await state.update_data(name=msg.text)
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=ans_id, text="Хорошо, теперь отправьте свой возраст числом")
    await state.set_state(KnowInterestStates.age)
    await bot.delete_message(msg.chat.id, msg.message_id)


@router.message(KnowInterestStates.age)
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
            reply_markup=keyboards.interupt_keyboard()
        ) if msg.text != msg_wrong_num else ...
        return
    await state.update_data(age=age)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text="Теперь укажите город проживания",
        reply_markup=keyboards.interupt_keyboard()
    )
    await state.set_state(KnowInterestStates.city)


@router.message(KnowInterestStates.city)
async def city_pro_talent_handler(msg: Message, state: FSMContext):

    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])

    await state.update_data(city=msg.text)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text="Отправьте краткое резюме о себе."
    )
    await bot.delete_message(msg.chat.id, msg.message_id)
    await state.set_state(KnowInterestStates.resume)


@router.message(KnowInterestStates.resume)
async def resume_pro_talent_handler(msg: Message, state: FSMContext):
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])

    await state.update_data(resume=msg.text)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text="Расскажите, пожалуйста, о вашем опыте работы."
    )
    await state.set_state()


@router.message(KnowInterestStates.exp)
async def exp_pro_talent_handler(msg: Message, state: FSMContext):
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])

    await state.update_data(exp=msg.text)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text="Спасибо за предоставленную информацию!"
    )
    user_data = await state.get_data()
    await bot.send_message(
        msg.chat.id,
        f"Ваша анкета завершена:\n"
        f"Имя: {user_data['name']}\n"
        f"Возраст: {user_data['age']}\n"
        f"Город: {user_data['city']}\n"
        f"Резюме: {user_data['resume']}\n"
        f"Опыт: {user_data['exp']}"
    )
    await msg.answer(
        "Перед тем как мы продолжим, необходимо ваше согласие с политикой обработки и хранения персональных данных", reply_markup=keyboards.personal_data_agreement_keyboard()
    )
    await state.clear()

@router.callback_query(F.data=="interrupt")
async def interrupt_form(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, "Форма была прервана, вы можете заполнить ее снова в любой момент")
    await state.clear()
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)