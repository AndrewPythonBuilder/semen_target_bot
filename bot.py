import time

from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup, Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Job
import logging

import constants, base_work

updater = Updater(token=constants.TOKEN, use_context=True, workers=3)
dispatcher = updater.dispatcher

job_queue = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


@run_async
def start(update, context):
    message = update.message
    bot = context.bot
    if message.chat.id in constants.admins:
        buttons = [['👋Изменить вступительное сообщение'], ['Изменить ответное сообщение'], ['📩Рассылка']]
        keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        bot.send_message(message.chat.id, 'Приветствую, Семен, нагибатель таргета!', reply_markup=keyboard)
        constants.last_message = 'меню'
    else:
        if message.chat.id in base_work.get_all_ids():
            pass
        else:
            base_work.register_user(message.chat.id, message.chat.username)

        bot.send_message(message.chat.id, base_work.get_message())



@run_async
def answer_questions(update, context: CallbackContext):
    message = update.message
    bot = context.bot
    if message.chat.id in constants.admins:
        if message.text == '👋Изменить вступительное сообщение':
            bot.send_message(message.chat.id, 'Сейчас вступительное сообщение такое⬇️⬇️⬇️')
            bot.send_message(message.chat.id, base_work.get_message())
            bot.send_message(message.chat.id, 'Семен Дмитриевич, напишите, пожалуйста, вступительное сообщение🙋‍♂️')
            constants.last_message = 'вступительное'
        elif message.text == '📋 Главное меню':
            buttons = [['👋Изменить вступительное сообщение'], ['Изменить ответное сообщение'], ['📩Рассылка']]
            keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
            bot.send_message(message.chat.id, 'Чем же займемся?', reply_markup=keyboard)
            constants.last_message = 'меню'
        elif message.text == 'Изменить ответное сообщение':
            bot.send_message(message.chat.id, 'Сейчас ответное сообщение такое⬇️⬇️⬇️')
            bot.send_message(message.chat.id, base_work.get_endl_message())
            buttons = [['📋 Главное меню']]
            keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
            bot.send_message(message.chat.id,
                             'Семен Дмитриевич, напишите, пожалуйста, новое ответное сообщение',
                             reply_markup=keyboard)
            constants.last_message = 'ответ'
        elif message.text == '📩Рассылка':
            buttons = [['📋 Главное меню']]
            keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
            bot.send_message(message.chat.id,
                             'Семен Дмитриевич, напишите, пожалуйста сообщение, которое вы хотите разослать📟',
                             reply_markup=keyboard)
            constants.last_message = 'рассылка'
        elif constants.last_message == 'рассылка':
            bot_mailing(message.message_id, message.chat.id, base_work.get_all_ids())
            bot.send_message(message.chat.id, '📍Рассылка началась...')
        elif constants.last_message == 'ответ':
            base_work.edit_endl_message(message.text)
            bot.send_message(message.chat.id, 'Ответное сообщение изменено, СЕМА, ты умничка!')
        elif constants.last_message == 'вступительное':
            base_work.edit_message(message.text)
            bot.send_message(message.chat.id, '🎉Вступительное сообщение изменено')
        else:
            constants.last_message = 'меню'
            bot.send_message(message.chat.id, '❤️Семен Дмитриевич, идите нахуй...')
    else:
        bot.forward_message(message_id=message.message_id, from_chat_id=message.chat.id, chat_id=constants.admins[0])
        buttons = [[InlineKeyboardButton('Перейти в диалог с пользователем', url='https://t.me/'+str(message.chat.username))]]
        reply_markup = InlineKeyboardMarkup(buttons)
        bot.send_message(constants.admins[0], 'Написать', reply_markup=reply_markup)
        bot.send_message(message.chat.id, base_work.get_endl_message())


@run_async
def bot_mailing(message_id, chat_id, ids):
    bot = Bot(token=constants.TOKEN)
    for i in range(len(ids)):
        if (i != 0) and (i % 20 == 0):
            time.sleep(20)
        try:
            bot.forward_message(chat_id=ids[i], from_chat_id=chat_id, message_id=message_id)
        except:
            pass

    bot.send_message(chat_id, '✅Рассылка завершена')


start_handler = CommandHandler('start', start)
answer_handler = MessageHandler(Filters.all, answer_questions)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(answer_handler)
updater.start_polling(timeout=5, clean=True)
