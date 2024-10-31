from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import keyboards
from config import BOT_API
from values import trainings

bot = Bot(BOT_API)
router = Router()

class DontKnowInterestStates(StatesGroup):
    ans_id = State()
    name   = State()
    age    = State()
    city   = State()
    resume = State()
    prof_t = State()
    spec   = State()
    mater  = State()

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
         reply_markup=keyboards.interupt_keyboard()
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
                                reply_markup=keyboards.interupt_keyboard()
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
        reply_markup=keyboards.interupt_keyboard()
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
    await state.update_data(resume=msg.text)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text="Пожалуйста, отправьте ссылку на свое резюме",
        reply_markup=keyboards.interupt_keyboard()
    )
    await bot.delete_message(
        msg.chat.id,
        msg.message_id
    )
    await state.set_state(DontKnowInterestStates.prof_t)


@router.message(DontKnowInterestStates.prof_t)
async def choosing_professional_type_new_handler(msg: Message, state: FSMContext):
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])
    await state.update_data(prof_t=msg.text)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text="ПрофОриентТест",
        reply_markup=keyboards.interupt_keyboard()
    )
    await bot.delete_message(
        msg.chat.id,
        msg.message_id
    )
    await state.set_state(DontKnowInterestStates.spec)


@router.message(DontKnowInterestStates.spec)
async def choosing_specialization_new_handler(msg: Message, state: FSMContext):
    ans_id = await state.get_data()
    ans_id = int(ans_id["ans_id"])
    await state.update_data(spec=msg.text)
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=ans_id,
        text=open("cpec_info.txt", "r").read(),
        reply_markup=keyboards.spec_keyboard()
    )
    await bot.delete_message(
        msg.chat.id,
        msg.message_id
    )
    await state.set_state(DontKnowInterestStates.mater)


@router.callback_query(DontKnowInterestStates.mater)
async def end_handler(callback: Message, state: FSMContext):
    await state.update_data(spec=callback.data)
    user_data = await state.get_data()
    await bot.send_message(
        callback.message.chat.id,
        f"Ваша анкета завершена:\n"
        f"Имя: {user_data['name']}\n"
        f"Возраст: {user_data['age']}\n"
        f"Город: {user_data['city']}\n"
        f"Резюме: {user_data['resume']}\n"
        f"Профориентационный тест: {user_data['prof_t']}\n"
        f"Специальность: {trainings[user_data['spec']]}"
    )
    await state.clear()


@router.callback_query(F.data=="interrupt")
async def interrupt_form(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.message.chat.id, "Заполение формы было отменено, вы можете вернуться к ней в любой момент")
    await state.clear()
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
