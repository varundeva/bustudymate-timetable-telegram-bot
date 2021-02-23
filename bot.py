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


def help_command(update, context):
    update.message.reply_text('Help!')


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


def sendTimeTable(callbackdata):
    data = getTimeTable(callbackdata)
    dataString = ""
    for i, j in enumerate(data):
        if i == 0:
            heading = f"<b><u>{j['University']} {j['Course']} - Time Table </u></b>\n\n🎓 University - <b>{j['University']}</b>\n📚 Course - <b>{j['Course']}</b>\n📖 Semester - <b>{j['Sem']}</b>\n\n"
            dataString += heading
        singleData = f"📝 Subject Name - <b>{j['SubjectName']}</b>\n🗓️ Exam Date - <b>{j['Date']}</b>\n⏰ Exam Time - <b>{j['Time']}</b>\n❓ QP Code - <b>{j['QPCode']}</b>\n\n\n"
        dataString += singleData

    return dataString


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
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"Hi {user.first_name}, to use me(bot) you have to be a member of the BUStudymate channel in order to stay updated with the latest updates.\nPlease click below button to join and /start the bot again.", reply_markup=help_reply_markup)
        return
    else:
        update.message.reply_text(
            'Choose Your 🎓University ⬇️', reply_markup=createUniversityKeyboard())


def end(update, context):
    callBackData.clear()
    update.callback_query.delete_message()
    update.callback_query.message.reply_text(
        'if you want again send /start')
    update.callback_query.message.reply_text(
        'If its not working please contact us through BUStudymate Group')


callBackData = []


def callBackQuery(update, context):
    query_data = update.callback_query.data
    callBackData.append(query_data)
    print(callBackData)
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
            update.callback_query.edit_message_text(
                sendTimeTable(callBackData), parse_mode="HTML")
            callBackData.clear()
            update.callback_query.message.reply_text(
                'if you want again send /start')
        if len(callBackData) > 3:
            end(update, context)

    except:
        end(update, context)


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
