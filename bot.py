import logging
import os
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from readFile import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

helpText = f'''This Bot🤖 will send you Timetable of your course

<b>How to Get All Timetable of my Course?</b>
First Send /start command to bot🤖
After that follow instructions
1️⃣ Select Your University 🎓
2️⃣ Select Your Semester 📚
3️⃣ Select Your Course 📖
✅ You'll Receive Timetables

<b>How to Get Single Subject Date and Time?</b>
To get perticular subject date and time use /qpcode command

1️⃣Send /qpcode with your subject QPCode
    EX - /qpcode 12345
    type /qpcode give a single space then type QPCode and send
2️⃣This will reply you Date and Time of that Subject
✅Done

If you have any question contact us by using /contact command[You'll get contact details]

➡️ Kindly Report if you have any issues regarding 🤖bot as well as the Data 🤖bot returned
➡️ Don't follow blindly Bot🤖 given data kindly cross verify with the timetable in university website🌐
'''


def help_command(update, context):
    update.message.reply_html(helpText)


footer = f"<b>🤝All The Best for your Exams📚</b>\n<b>👏Do Well in All the Exams 📚</b>\n\n\n\n🔗Connect With Us\n\n\nFor Study Materials 📖 Check<a href='https://bustudymate.in'> BUStudymate Blog</a>\n\nFor Instant Updates📢 Follow On <a href = 'https://instagram.com/bustudymate'>Instagram🖼️</a>\n\nFor 👩‍💻Discussion/Q & A⁉️ - <a href='https://forum.bustudymate.in'>Join BUForum</a>\n\nFeedbacks👏/ Report❌ Email ✉️ - admin@bustudymate.in\n\nDonate💵 to Run the Service - contact BUStudymate"


def createUniversityKeyboard():
    university = getAllUniversities()
    keyboard = []
    for uni in university:
        keyboard.append([InlineKeyboardButton(uni, callback_data=uni)])
    return InlineKeyboardMarkup(keyboard)


def createSemesterKeyboard(university):
    semesters = getAllSemesterOfUniversity(university)
    keyboard = []
    for sem in semesters:
        keyboard.append([InlineKeyboardButton(sem, callback_data=sem)])
    return InlineKeyboardMarkup(keyboard)


def createCourseKeyboard(callbackdata):
    print(callbackdata)
    courses = getAllCourseOfSemester(callbackdata)
    keyboard = []
    for course in courses:
        keyboard.append([InlineKeyboardButton(course, callback_data=course)])
    return InlineKeyboardMarkup(keyboard)


def sendTimeTable(callbackdata, update):
    data = getTimeTable(callbackdata)
    dataString = ""
    dataList = []
    for i, j in enumerate(data):
        if i == 0:
            heading = f"<b><u>{j['University']} {j['Course']} - Time Table </u></b>\n\n🎓 University - <b>{j['University']}</b>\n📚 Course - <b>{j['Course']}</b>\n📖 Semester - <b>{j['Sem']}</b>\n\n"
            dataString += heading

        singleData = f"📝 Subject Name - <b>{j['SubjectName']}</b>\n🗓️ Exam Date - <b>{j['Date']}</b>\n⏰ Exam Time - <b>{j['Time']}</b>\n❓ QP Code - <b>{j['QPCode']}</b>\n\n\n"
        dataString += singleData
        if i != 0 and i % 10 == 0:
            dataList.append(dataString)
            dataString = ""
    print(len(dataList))
    if len(dataList) == 0:
        update.callback_query.edit_message_text(dataString, parse_mode="HTML")
        update.callback_query.message.reply_html(
            footer, disable_web_page_preview=True)
    else:
        update.callback_query.message.delete()
        for i in dataList:
            update.callback_query.message.reply_html(i)
        update.callback_query.message.reply_html(
            footer, disable_web_page_preview=True)


help_keyboard = [[InlineKeyboardButton(
    "Join Channel", url="https://t.me/bustudymate")]]
help_reply_markup = InlineKeyboardMarkup(help_keyboard)


def start(update, context):
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action="typing")
    user = update.message.from_user
    channel_member = context.bot.get_chat_member(
        os.environ.get("CHANNEL_ID"), user_id=update.message.chat_id)
    status = channel_member["status"]
    if(status == 'left'):
        update.message.reply_html(
            text=f"Hi {user.first_name}👋🏻, to use me(Bot🤖) you have to be a member of the BUStudymate channel in order to stay updated with the latest updates.\n\n<b>Please click below button to join and then /start the bot again.</b>", reply_markup=help_reply_markup)
        return
    else:
        update.message.reply_text(
            'Choose Your 🎓University ⬇️', reply_markup=createUniversityKeyboard())


contactString = "🔗Connect With Us\n\n\nFor Study Materials 📖 Check<a href='https://bustudymate.in'> BUStudymate Blog</a>\n\nFor Instant Updates📢 Follow On <a href = 'https://instagram.com/bustudymate'>Instagram🖼️</a>\n\nFor 👩‍💻Discussion/Q & A⁉️ - <a href='https://forum.bustudymate.in'>Join BUForum</a>\n\nFeedbacks👏/ Report❌ Email ✉️ - admin@bustudymate.in\n\nDonate💵 to Run the Service - contact BUStudymate"


def contactus(update, context):
    update.message.reply_html(contactString, disable_web_page_preview=True)


def end(update, context):
    callBackData.clear()
    update.callback_query.message.delete()
    update.callback_query.message.reply_text(
        'if you want again send /start')
    update.callback_query.message.reply_text(
        'If its not working please contact us through BUStudymate Group')


callBackData = []


def callBackQuery(update, context):
    query_data = update.callback_query.data
    callBackData.append(query_data)
    update.callback_query.answer()
    try:
        if query_data in getAllUniversities():
            update.callback_query.edit_message_text(
                'Choose Your 📖Semester⬇️', reply_markup=createSemesterKeyboard(query_data))
        print(len(callBackData))
        if len(callBackData) == 2 and query_data in getAllSemesterOfUniversity(callBackData[0]):
            update.callback_query.edit_message_text(
                'Choose Your 📚Course⬇️', reply_markup=createCourseKeyboard(callBackData))
        if len(callBackData) == 3 and query_data in getAllCourseOfSemester(callBackData):
            sendTimeTable(callBackData, update)
            callBackData.clear()
            update.callback_query.message.reply_text(
                'if you want again send /start')
        if len(callBackData) > 3:
            end(update, context)

    except Exception as e:
        print(str(e))
        end(update, context)


def getTimeTablefromQPCode(update, context):
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action="typing")
    user = update.message.from_user
    channel_member = context.bot.get_chat_member(
        os.environ.get("CHANNEL_ID"), user_id=update.message.chat_id)
    status = channel_member["status"]
    if(status == 'left'):
        update.message.reply_html(
            text=f"Hi {user.first_name}👋🏻, to use me(Bot🤖) you have to be a member of the BUStudymate channel in order to stay updated with the latest updates.\n\n<b>Please click below button to join and then /start the bot again.</b>", reply_markup=help_reply_markup)
        return
    else:
        query = update.message.text[8:].split(' ')
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action="typing")
        if len(query[0]) == 0:
            qpText = f"Please enter QPCode after /qpcode command\nCheck /help if you have doubt or to know more"
            update.message.reply_text(qpText)
            return
        try:
            data = getTimeTablebyQPCode(query[0])
            if(len(data) == 0):
                raise Exception(
                    f"Sorry, Data Not Found for {query[0]} QP Code\nPlease Check QP Code and Try Again")
            dataString = ""
            for i, j in enumerate(data):
                if i == 0:
                    heading = f"<b><u>Time Table of QPCode {j['QPCode']}</u></b>\n\n\n"
                    dataString += heading
                singleData = f"🎓 University - <b>{j['University']}</b>\n📚 Course - <b>{j['Course']}</b>\n📖 Semester - <b>{j['Sem']}</b>\n📝 Subject Name - <b>{j['SubjectName']}</b>\n🗓️ Exam Date - <b>{j['Date']}</b>\n⏰ Exam Time - <b>{j['Time']}</b>\n❓ QP Code - <b>{j['QPCode']}</b>\n\n\n"
                dataString += singleData

            update.message.reply_html(dataString)
            update.message.reply_html(footer, disable_web_page_preview=True)
        except Exception as e:
            update.message.reply_text(str(e))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.

    updater = Updater(
        token=os.environ.get("BOT_TOKEN"), use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("contact", contactus))
    dispatcher.add_handler(CommandHandler("qpcode", getTimeTablefromQPCode))
    updater.dispatcher.add_handler(CallbackQueryHandler(callBackQuery))

    dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=PORT,
                          url_path=os.environ.get("BOT_TOKEN"))
    updater.bot.set_webhook(
        os.environ.get("HOST_NAME") + os.environ.get("BOT_TOKEN"))
    logging.info("Starting Long Polling!")

    updater.idle()


if __name__ == '__main__':
    main()
