import telebot
from entry import Entry
from neural_network.run_model import *

entries = []

bot = telebot.TeleBot('1818273201:AAGnC6dQwHLiKZ7Dbd8IbrowtUY_s9fB7Rw')
userSteps = dict()

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    global userSteps
    userId = message.from_user.id
    if message.text == "/start" or userId not in userSteps:
        userSteps[userId] = 0
        sendMessage(userId, entries[0].output, entries[0].inputs)
        print(userSteps)
        return
    prevEntry: Entry = entries[userSteps[userId]]
    if prevEntry.isAi:
        newEntryIndex = handleAi(message.text, prevEntry.inputs)
    elif len(prevEntry.inputs) == 0:
        newEntryIndex = 0
    else:
        try:
            newEntryIndex = list(map(lambda x: x.lower(), prevEntry.inputs)).index(message.text.lower())
        except ValueError:
            newEntryIndex = -1
    if newEntryIndex == -1:
        notifyError(userId, prevEntry)
        return

    newIndex = prevEntry.next[newEntryIndex]
    newEntry = Entry.entries[newIndex]
    sendMessage(userId, newEntry.output, newEntry.inputs, newEntry.isAi)
    userSteps[userId] = newIndex
    print(userSteps)

def notifyError(userId, prevEntry):
    sendMessage(userId, "We weren't able to recognise your text", prevEntry.inputs, prevEntry.isAi)
    print(userSteps)

def handleAi(text: str, answ: [str]) -> int:
    emotion = chatbot_response(text)
    for i, s in enumerate(answ):
        if s == emotion:
          return i
    return -1

def sendMessage(userId, text: str, answ: [str], isAi: bool = False):
    reply_markup = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
    for s in answ:
        reply_markup.row(s)
    if isAi:
        reply_markup = None
    bot.send_message(userId, text, reply_markup=reply_markup)

def startBot():
    global bot
    bot.polling(none_stop=True, interval=0)
