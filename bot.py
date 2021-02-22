import logging

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
    return data


def start(update, context):
    update.message.reply_text(
        'Choose Your University:', reply_markup=createUniversityKeyboard())


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
                'Choose Your Semester:', reply_markup=createSemesterKeyboard(query_data))
        print(len(callBackData))
        if len(callBackData) == 2 and query_data in getAllSemesterOfUniversity(callBackData[0]):
            update.callback_query.edit_message_text(
                'Choose Your Course:', reply_markup=createCourseKeyboard(callBackData))
        if len(callBackData) == 3 and query_data in getAllCourseOfSemester(callBackData):
            update.callback_query.edit_message_text(getTimeTable(callBackData))
            callBackData.clear()
            update.callback_query.message.reply_text(
                'if you want again send /start')
        if len(callBackData) > 3:
            end(update, context)

    except:
        end(update, context)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1673078957:AAGJdst1sKMeQv_6YcnIFZTms_fzVVfCOVk")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(callBackQuery))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
