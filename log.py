import os


def addToLog(context, update):
    template = f'''New Query in BUTimetable Bot\n
Checked Time Table\n
User ID - {update.callback_query.message.chat.id}
UserName - @{update.callback_query.message.chat.username}
User Name - {update.callback_query.message.chat.first_name} {update.callback_query.message.chat.last_name}
Date Time - {update.callback_query.message.date}\n
Call Back Query Data - {context.user_data}
'''
    print(template)
    context.bot.send_message(
        chat_id=os.environ.get("LOG_CHANNEL"), text=template)


def startLog(update, context, status):
    template = f'''New Query in BUTimetable Bot\n
User sent /start command \n
User ID - {update.message.chat.id}
UserName - @{update.message.chat.username}
User Name - {update.message.chat.first_name} {update.message.chat.last_name}
User Status in Channel - {status}
Date Time - {update.message.date}\n
    '''
    print(template)
    context.bot.send_message(
        chat_id=os.environ.get("LOG_CHANNEL"), text=template)
