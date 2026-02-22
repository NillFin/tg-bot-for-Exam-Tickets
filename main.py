import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import fitz

bot = telebot.TeleBot("6487860967:AAFcty0VPPuJg4ugy6HWXmJRXmtybGXvPY4", parse_mode=None)
semSubjects = ["cb_calc", "cb_physics", "cb_CoV", "cb_NM", "cb_complex", "cb_diff"]

def linkToFile(subject, i):
    return ("/Users/aleksandrsafonenko/dev/projects/tgBotForExamTickets/" 
        + subject + "_tickets/" + subject + "_" + str(i) + ".pdf")

def getOrAddTicket_markup():
    keyboard = [
        [InlineKeyboardButton("получить билеты", callback_data="cb_getTicket")],
        [InlineKeyboardButton("добавить билет", callback_data="cb_addTicket")],
        [InlineKeyboardButton("какие билеты проверены?", callback_data="cb_checkTicket")]
    ]
    return InlineKeyboardMarkup(keyboard)

def chooseSubject1_markup():
    keyboard = [
        [
            InlineKeyboardButton("матан", callback_data="cb_calc1"),
            InlineKeyboardButton("физика", callback_data="cb_physics1"),
        ],
        [
            InlineKeyboardButton("вариационка", callback_data="cb_CoV1"),
            InlineKeyboardButton("числаки", callback_data="cb_NM1"),
        ],
        [
            InlineKeyboardButton("тфкп", callback_data="cb_complex1"),
            InlineKeyboardButton("диффуры", callback_data="cb_diff1"),
        ],
        [
            InlineKeyboardButton("назад🔙", callback_data="cb_home")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def chooseSubject2_markup():
    keyboard = [
        [
            InlineKeyboardButton("матан", callback_data="cb_calc2"),
            InlineKeyboardButton("физика", callback_data="cb_physics2"),
        ],
        [
            InlineKeyboardButton("вариационка", callback_data="cb_CoV2"),
            InlineKeyboardButton("числаки", callback_data="cb_NM2"),
        ],
        [
            InlineKeyboardButton("тфкп", callback_data="cb_complex2"),
            InlineKeyboardButton("диффуры", callback_data="cb_diff2"),
        ],
        [
            InlineKeyboardButton("назад🔙", callback_data="cb_home")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def home_markup():
    keyboard = [[InlineKeyboardButton("назад🔙", callback_data="cb_home")]]
    return InlineKeyboardMarkup(keyboard)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_home":
        home(call.message)
    elif call.data == "cb_checkTicket":
        bot.send_message(
            call.message.chat.id, 
            """
            пока никакие🫠
            """
        )
        home(call.message)
    elif call.data == "cb_getTicket":
        chooseSubject1(call.message)
    elif call.data == "cb_addTicket":
        chooseSubject2(call.message)

    elif (call.data[:len(call.data) - 1] in semSubjects) and (call.data[-1] == "1"):
        chooseTicket1(call.message, call.data)
    elif (call.data[:len(call.data) - 1] in semSubjects) and (call.data[-1] == "2"):
        chooseTicket2(call.message, call.data)
    """elif call.data == "cb_calc1" or call.data == "cb_physics1":   
        chooseTicket1(call.message, call.data)
    elif call.data == "cb_calc2" or call.data == "cb_physics2":   
        chooseTicket2(call.message, call.data)"""


@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(
        message.chat.id, 
        "Привет! С помощью этого бота ты сможешь запросто добавлять новые билеты, загружать исправленные и" +
        " получать доступ ко всем остальным, не отвлекая других людей.\n" +
        "Взаимодействовать с ботом можно посредством кнопок, расположенных под сообщением👇", 
        reply_markup=getOrAddTicket_markup()
    )

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if str(message.chat.id) == "498308814":
        bot.reply_to(message, message.text)

def home(message):
    bot.send_message(
        message.chat.id, 
        "Нажмите на нужную кнопочку👇", 
        reply_markup=getOrAddTicket_markup()
    )

def chooseSubject1(message):
    bot.send_message(message.chat.id, "Выберите предмет:", 
                        reply_markup=chooseSubject1_markup())
    
def chooseTicket1(message, subject):
    subject = subject[3:]
    subject = subject[:len(subject)-1]
    existsTickets = ""
    for i in range(200):
        if os.path.isfile(
            linkToFile(subject, str(i))
        ):
            existsTickets += str(i) + ", "
    existsTickets = existsTickets[:len(existsTickets)-2] + "."
    if subject == "NM":
        bot.send_message(
            message.chat.id,
            "По численным методам мы не расписываем билеты, т.к. это не имеет" +
            " большого смысла. Поэтому вот вам файлик с лекциями🙃"
        )
        if os.path.isfile(
            "/Users/aleksandrsafonenko/dev/projects/tgBotForExamTickets/"
                + "NM_tickets/NM_lectures.pdf"
        ):
            bot.send_document(
                message.chat.id, 
                open(
                    "/Users/aleksandrsafonenko/dev/projects/tgBotForExamTickets/"
                    + "NM_tickets/NM_lectures.pdf", 
                    "rb"
                )
            ) 
        else:
            bot.send_message(message.chat.id, "ooops, его пока нет😔")
        # bot.register_next_step_handler(message, home)
        home(message)
    elif subject == "calc":
        bot.send_message(
            message.chat.id,
            "Попытки найти билеты по матану удачными нельзя назвать😕\n" +
            "Поэтому пока наслаждайтесь лекциями, в которых все разбито по темам. "
            + "По ним можно спокойно готовиться, так как Камачкин эти темы и" 
            + " разбивает по билетам👍" 
        )
        if os.path.isfile(
            "/Users/aleksandrsafonenko/dev/projects/tgBotForExamTickets/"
                + "calc_tickets/calc_lectures.pdf"
        ):
            bot.send_document(
                message.chat.id, 
                open(
                    "/Users/aleksandrsafonenko/dev/projects/tgBotForExamTickets/"
                    + "calc_tickets/calc_lectures.pdf", 
                    "rb"
                )
            ) 
        else:
            bot.send_message(message.chat.id, "ooops, файлика пока нет😔")
        # bot.register_next_step_handler(message, home)
        home(message)
    elif existsTickets == ".":
        bot.send_message(
            message.chat.id,
            "По этому предмету билеты пока не расписаны :("
        )
        #bot.register_next_step_handler(message, home)
        home(message)
    else: 
        bot.send_message(
            message.chat.id,
            "Расписаны (необязательно проверены, но расписаны) следующие билеты:\n"
            + existsTickets + "\n\n" +
            "Напишите промежуток билетов, который хотите получить\n" +
            "(Пример: 1-5 выведет все билеты с 1-го по 5-ый\n" +
            " 1-1 выведет только 1-ый билет\n" +
            " \"все\" (без кавычек) выведет все билеты по отдельности\n" +
            " \"итог\" (без кавычек) выведет один файл пдф со всеми билетами)",
            reply_markup=home_markup()
        )
        bot.register_next_step_handler(message, chooseTicket1next, subject)

def chooseTicket1next(message, subject):
    bot.send_message(message.chat.id, "Готовлю файлы, подождите, пожалуйста")
    if message.text == "итог" or message.text == "Итог" or message.text == "ИТОГ":
        result = fitz.open()
        for i in range(200):
                if os.path.isfile(
                    linkToFile(subject, str(i))
                ):
                    with fitz.open(
                        linkToFile(subject, str(i))
                    ) as mfile:
                        result.insert_pdf(mfile)
        result.save(
            "/Users/aleksandrsafonenko/dev/projects/tgBotForExamTickets/" + 
            subject + "_tickets/" + subject + "_res.pdf"
        )
        bot.send_document(
            message.chat.id, 
            open(
                "/Users/aleksandrsafonenko/dev/projects/tgBotForExamTickets/"
                + subject + "_tickets/" + subject + "_res.pdf", 
                "rb"
            )
        )
        home(message)
    elif message.text == "все" or message.text == "Все" or message.text == "ВСЕ":
        for i in range(200):
            if os.path.isfile(
                linkToFile(subject, str(i))
            ):
                bot.send_document(
                    message.chat.id, 
                    open(linkToFile(subject, str(i)), "rb"),
                    # visible_file_name = str(i) + ".pdf"
                )
        home(message)
    else:
        nums = message.text.split("-")
        flag = True
        id = message.chat.id
        try:
            num1 = int(nums[0])
            num2 = int(nums[1])
        except Exception as e:
            chooseTicket1(message, "cb_"+subject+"n")
            # chooseTicket1(message, subject)
            flag = False
        if flag:
            for i in range(num1, num2+1):
                if os.path.isfile(
                    linkToFile(subject, str(i))
                ):
                    bot.send_document(
                        id, 
                        open(linkToFile(subject, str(i)), "rb")
                    )
                else:
                    bot.send_message(id, "Билета " + str(i) + " пока нет :(")
            home(message)


def chooseSubject2(message):
    bot.send_message(message.chat.id, "Выберите предмет:", 
                        reply_markup=chooseSubject2_markup())

def chooseTicket2(message, subject):
    subject = subject[3:]
    subject = subject[:len(subject)-1]
    bot.send_message(
        message.chat.id, 
        "Напишите номер билета (целое неотрицательное число):\n\n"
        + "P.s. Если это лекции по матану/числакам, то пишите 0",
        reply_markup=home_markup()
    )
    bot.register_next_step_handler(message, chooseTicket2next, subject)

def chooseTicket2next(message, subject):
    flag = True
    try:
        num = int(message.text)
    except Exception as e:
        chooseTicket2(message, "cb_"+subject+"n")
        # chooseTicket2(message, subject)
        flag = False
    if num < 0:
        chooseTicket2(message, "cb_"+subject+"n")
        # chooseTicket2(message, subject)
        flag = False
    if flag:
        bot.send_message(
            message.chat.id, 
            "загрузите файл (насчет названия не переживайте," +
            "оно будет автоматически сгенерировано)",
            reply_markup=home_markup()
        )
        print("there was added file:", subject, num)
        bot.register_next_step_handler(message, addFile, subject, num)

@bot.message_handler(content_types=['document'])
def addFile(message, subject, num):
    if subject == "calc" or subject == "NM":
        file_name = subject + "_lectures.pdf"
    else:
        file_name = subject + "_" + str(num) + ".pdf"
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("/Users/aleksandrsafonenko/dev/projects/tgBotForExamTickets/" +
                subject + "_tickets/" + file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
    except Exception as e:
        bot.send_message(message.chat.id, "Извините, но это не тот файл, о котором вас просили :(")
    # bot.register_next_step_handler(message, home)
    home(message)


bot.infinity_polling()
