import discord, logging, json
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
#import platform
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment

bot = Bot(description="Channel Logger Bot by jskrist#3569", command_prefix="!", pm_help = True)
db = TinyDB('data.json')
msg = Query()

@bot.event
async def on_ready():
	print('Bot is up and running.')


@bot.listen()
async def on_message(message):
	if message.author.id != bot.user.id:
		await bot.send_message(message.channel, message.author.name + ' says: ' + message.content)
		if not db.search(msg.content == message.content):
			await bot.send_message(message.channel, 'New Message')
			db.insert({'content': message.content, 'authorName': message.author.name})

@bot.command(pass_context=True)
async def printDB(context):
	await bot.send_message(context.message.channel, 'ack')
	for item in db:
		await bot.send_message(context.message.channel, item)

@bot.command(pass_context=True)
async def stats(context):
	await bot.send_message(context.message.channel, 'ack')
	postingUsers = getPostingUsers()
	for user in postingUsers:
		userMsgs = db.search(msg.authorName == user)
		await bot.send_message(context.message.channel, '{0} has {1} messages'.format(user, len(userMsgs)))

def getPostingUsers():
	postingUsers = set();
	for item in db:
		postingUsers.add(item['authorName'])

	return postingUsers

with open('botToken.txt', 'r') as myfile:
    botToken = myfile.read().replace('\n', '')

bot.run(botToken)


