import telebot
import entry
import bot

entriesFile = open('entries.json', 'r')
entriesText = entriesFile.read()
entry.Entry.parseJson(entriesText)

bot.entries = entry.Entry.entries

bot.startBot()