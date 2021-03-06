# -*- coding: utf-8 -*-
import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

chat_id, user_id = (None,None)

TOKEN = '293519004:AAFFhIBJrrxYzVs9clx9g2tDpWIi84ZSiio'

def onChatMessage(msg):
    global user_id, chat_id
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Confirmar',
                                        callback_data='yes')],
                    [InlineKeyboardButton(text='Recusar',
                                        callback_data='no')]
                ])

    if 'new_chat_member' in msg:
        if msg['new_chat_member']['username'] != 'PyLadiesBot':
            user_id = msg['new_chat_member']['id']
            bot.sendMessage(chat_id,
                            'Confirmar usuária que entrou?',
                            reply_markup=keyboard)

def onCallbackQuery(msg):
    global user_id, chat_id

    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print 'Callback Query:', query_id, from_id, query_data

    if query_data == 'yes':
        bot.answerCallbackQuery(query_id, text='Confirmada!')
        bot.sendMessage(chat_id, 'Seja bem vinda PyLady!')
        user_id = None
    else:
        if user_id:
            bot.sendMessage(chat_id, 'Usuário '+
                        str(user_id) + ' sendo retirado..')
            bot.kickChatMember(chat_id, user_id)
            bot.answerCallbackQuery(query_id, text='Usuário retirado.')
        else:
            bot.answerCallbackQuery(query_id, text='Erro.')

bot = telepot.Bot(TOKEN)

bot.message_loop({'chat': onChatMessage,
                'callback_query': onCallbackQuery},
                run_forever='Listening ...')
