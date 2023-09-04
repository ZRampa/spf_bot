import io
import xlsxwriter
import pandas as pd
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
import asyncio
from telebot import types, asyncio_filters
from sql_lib import *

bot = AsyncTeleBot("6676953977:AAE2URAYE47h7wHEllefx_Yx7y1wommYv-w", state_storage=StateMemoryStorage())


class States_reg(StatesGroup):
    reg_1 = State()
    reg_2 = State()
    reg_3 = State()
    reg_4 = State()


class States_admin_menu(StatesGroup):
    send_all_nots = State()


class States_anon_mes(StatesGroup):
    anon_mes_1 = State()


@bot.message_handler(state=States_reg.reg_1)
async def reg_1(message):
    if len(message.text) > 100:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await too_many_in_reg(message)
        return

    if message.text == "/start":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await start_in_reg(message)
        return

    await bot.send_message(message.chat.id, 'Ваш тег телеграм:')
    await bot.set_state(message.from_user.id, States_reg.reg_2, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['reg_1'] = message.text


@bot.message_handler(state=States_reg.reg_2)
async def reg_2(message):
    if len(message.text) > 100:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await too_many_in_reg(message)
        return

    if message.text == "/start":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await start_in_reg(message)
        return

    await bot.send_message(message.chat.id, 'Ваш номер телефону:')
    await bot.set_state(message.from_user.id, States_reg.reg_3, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['reg_2'] = message.text


@bot.message_handler(state=States_reg.reg_3)
async def reg_3(message):
    if len(message.text) > 100:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await too_many_in_reg(message)
        return

    if message.text == "/start":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await start_in_reg(message)
        return

    await bot.send_message(message.chat.id, 'Ваш курс:')
    await bot.set_state(message.from_user.id, States_reg.reg_4, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['reg_3'] = message.text


@bot.message_handler(state=States_reg.reg_4)
async def reg_4(message):
    if len(message.text) > 100:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await too_many_in_reg(message)
        return

    if message.text == "/start":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await start_in_reg(message)
        return

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        sql_query(query_ins_active(message.from_user.id, data['reg_1'], data['reg_2'], data['reg_3'], message.text))

    m_text = "Привіт!\nДякуємо за реєстрацію!\nТримай всю потрібну інформацію про студентський парламент факультету"
    await bot.send_message(message.chat.id, m_text, reply_markup=create_menu())
    await bot.delete_state(message.from_user.id, message.chat.id)


async def start_in_reg(message):
    await bot.send_message(message.chat.id, "Помилка регистрації, пройдіть регистрацію повторно")
    await bot.send_message(message.chat.id, "Ваш ПІБ:")
    await bot.set_state(message.from_user.id, States_reg.reg_1, message.chat.id)


async def too_many_in_reg(message):
    await bot.send_message(message.chat.id, "Ви ввели дуже багато символів, пройдіть регистрацію повторно")
    await bot.send_message(message.chat.id, "Ваш ПІБ:")
    await bot.set_state(message.from_user.id, States_reg.reg_1, message.chat.id)


@bot.message_handler(state=States_anon_mes.anon_mes_1)
async def anon_mes_1(message):
    if message.text == "Вихід":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await bot.send_message(message.chat.id, "Меню", reply_markup=create_menu())
        return

    sql_query(query_ins_anon_mes(message.text))
    await bot.send_message(message.chat.id, "Звернення збережено", reply_markup=create_menu())
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=States_admin_menu.send_all_nots, content_types=['document', 'audio', 'text', 'photo', 'video_note', 'voice', 'video', 'caption'])
async def send_all(message):
    if message.text == "Вихід":
        await bot.delete_state(message.from_user.id, message.chat.id)
        await bot.send_message(message.chat.id, "Меню", reply_markup=create_menu())
        return

    if message.content_type == "photo":

        photo_id = message.photo[-1].file_id
        for i in sel_all_id():
            await bot.send_photo(i[0], photo_id, caption=message.caption)

    elif message.content_type == "audio":

        file_info = await bot.get_file(message.audio.file_id)
        file_path = file_info.file_path
        audio_bytes = await bot.download_file(file_path)

        for i in sel_all_id():
            await bot.send_audio(i[0], audio_bytes, caption=message.caption)

    elif message.content_type == "text":
        for i in sel_all_id():
            await bot.send_message(i[0], message.text)

    elif message.content_type == "video_note":
        for i in sel_all_id():
            await bot.send_video_note(i[0], message.video_note.file_id)

    elif message.content_type == "document":
        for i in sel_all_id():
            await bot.send_document(i[0], message.document.file_id, caption=message.caption)

    elif message.content_type == "voice":
        for i in sel_all_id():
            await bot.send_voice(i[0], message.voice.file_id, caption=message.caption)

    elif message.content_type == "video":
        for i in sel_all_id():
            await bot.send_video(i[0], message.video.file_id, caption=message.caption)

    else:
        await bot.delete_state(message.from_user.id, message.chat.id)
        await bot.send_message(message.chat.id, "Не підтримується такий вид файлу", reply_markup=create_menu())
        return

    await bot.send_message(message.chat.id, "Повідомлення відправлено всім користувачам!", reply_markup=create_menu())


@bot.message_handler(commands=['start'])
async def send_welcome(message):

    is_a, ans = name_db(message.from_user.id)

    if not is_a:
        await bot.send_message(message.chat.id, "Ваш ПІБ:")
        await bot.set_state(message.from_user.id, States_reg.reg_1, message.chat.id)

    else:
        m_text = "Привіт, тримай всю потрібну інформацію про студентський парламент факультету"
        await bot.send_message(message.chat.id, m_text, reply_markup=create_menu())
        return


def create_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Канали СПФ")
    item2 = types.KeyboardButton("Склад СПФ")
    item3 = types.KeyboardButton("Що таке СПФ/ОСС")
    item5 = types.KeyboardButton("Анонімне звернення/пропозиція")
    item6 = types.KeyboardButton("Інше")
    markup.add(item1, item2, item3, item5, item6)
    return markup


async def something_else(message):
    pass


async def anon_mes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вихід")
    markup.add(item1)

    await bot.send_message(message.chat.id, "Ваше звернення буде повністю анонімне\n"
                                            "Дані про відправника не зберігаються і не обробляються\n"
                                            "Введіть ваше звернення:", reply_markup=markup)

    await bot.set_state(message.from_user.id, States_anon_mes.anon_mes_1, message.chat.id)


async def export_exel(message):
    df1 = sql_query('SELECT * FROM students')

    output = io.BytesIO()

    # Создание DataFrame из полученных данных
    df1 = pd.DataFrame(df1,
                       columns=['ПІБ', 'Телеграм', 'Телефон', 'Курс', 'Юзур_ід'])


    # Создание нового Excel-файла с помощью XlsxWriter
    workbook = xlsxwriter.Workbook(output)

    # Создание нового листа
    worksheet1 = workbook.add_worksheet('Інформація про студентів')  # Создание листа для первой таблицы


    # Запись данных из DataFrame в лист
    worksheet1.write_row(0, 0, df1.columns)  # Запись заголовков столбцов для первой таблицы
    for i, row in enumerate(df1.values, start=1):  # Запись данных из каждой строки DataFrame для первой таблицы
        worksheet1.write_row(i, 0, row)

    # Закрытие книги
    workbook.close()

    # Перевод буфера в режим чтения
    output.seek(0)

    buffer = output
    await bot.send_document(message.chat.id, buffer, visible_file_name='Base.xlsx')


async def chanel_spf(message):
    await bot.send_message(message.chat.id, """
    🔹Калан СП ФРЕКС — основне джерело новин. На каналі  публікується вся необхідна інформація про засідання СП, нарахування додаткових балів, студентських заходів тощо.
👉 @sp_frecs


🔹Усі документи, які стосуються діяльності Студпарламенту — як-то розпорядження, протоколи, кошториси — публікуються в каналі документообігу СП ФРЕКС
👉 @dok_obig_frecs""")
#  +


async def members_spf(message):
    await bot.send_message(message.chat.id, """
    Склад Студентського Парламенту ФРЕКС 

🔹Голова СП ФРЕКС: Марія Довгаль
@violetperson

🔹Заступник Голови СП ФРЕКС: Євген Лазоренко 
@zRAMPAz

Голови департаментів:
🔹 Дизайну: 
Іван Капуста @crayzeeeeone

🔹Івентів:
Юліана Пономаренко @iulianaponomarenko

🔹 Інформаційного:
Артем Каменець @Artem_Kamenets

🔹 Освітнього:
Дмитро Зозуля @f42mediaaa""")
#  +


async def what_is_spf(message):
    await bot.send_message(message.chat.id, """Студентський Парламент Факультету— це Орган Студентського Самоврядування університету в межах структурного підрозділу. 

Хто, як не студенти найкраще знають власні потреби? 

СПФ відіграє важливу роль у представництві та захисті інтересів студентів.

Проте Студентський Парламент не обмежується взаємодію з адміністрацією факультету/університету — саме він займається організацією студентських ініціатив, заходів та вечірок, і звісно ж, нарахуванням додаткових балів за наукову, громадську та спортивну діяльність 😉""")


@bot.message_handler(content_types=['text'])
async def menu(message):
    if message.chat.type == 'private':
        is_a, _ = name_db(message.from_user.id)
        if is_a:
            if message.text == "Канали СПФ":  # +
                await chanel_spf(message)

            elif message.text == "Склад СПФ":  # +
                await members_spf(message)

            elif message.text == "Що таке СПФ/ОСС":
                await what_is_spf(message)

            elif message.text == "Анонімне звернення/пропозиція":  # +
                await anon_mes(message)

            elif message.text == "Інше":  # +
                await something_else(message)

            elif message.text == "panel.admin.checker.1357999675":  # +
                await export_exel(message)

            elif message.text == "panel.admin.to_all.mes.55553334":  # +
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Вихід")
                markup.add(item1)

                await bot.send_message(message.chat.id, "Введіть текст: ", reply_markup=markup)
                await bot.set_state(message.from_user.id, States_admin_menu.send_all_nots, message.chat.id)

            else:
                await bot.send_message(message.chat.id, "Не вірний текст")
        else:
            await bot.send_message(message.chat.id, "Ви не зарегистровані, зверніться до @zRAMPAz")


bot.add_custom_filter(asyncio_filters.StateFilter(bot))


async def main():
    loop = asyncio.get_running_loop()
    await asyncio.gather(bot.polling(non_stop=True))

asyncio.run(main())
