import asyncio, discord, json
from discord.ext.commands import Bot
from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import delete, increment


# Create a bot
bot = Bot(description="Channel Logger Bot by jskrist#3569", command_prefix="!", pm_help = True)
# Start or connect to a database to log the messages
db = TinyDB('data.json')
# This is a Query object to use when searching through the database
msg = Query()

# This function prints a message to the terminal/command window to let you know the bot started correctly
@bot.event
async def on_ready():
	print('Bot is up and running.')

# when a message comes into the server, this function is executed
@bot.listen()
async def on_message(message):
	# Confirm that the message did not come from this Bot to make sure we don't get
	# into an infinite loop if this bot send out any messages in this function
	if message.author.id != bot.user.id:
		# debug code, this repeats anything that other users send to the server
		await bot.send_message(message.channel, message.author.name + ' says: ' + message.content)
		# if the mesage content is not in the database yet
		if not db.search(msg.content == message.content):
			# send a debug message
			await bot.send_message(message.channel, 'New Message')
			# Insert the content into the database, along with the name of the user that posted it.
			# You could add any other data to the database at this point.
			#
			# Consider filtering out messages that start with '!' or other command characters
			# also consider using message.content.lower() to make sure "Hi", hI, and "hi" are all the same
			db.insert({'content': message.content, 'authorName': message.author.name})

# this command prints out the contents of the database.  It should not be used with a large database.
# the database will be save into a file called data.json (see line 12 of this file).
@bot.command(pass_context=True)
async def printDB(context):
	await bot.send_message(context.message.channel, 'ack')
	for item in db:
		await bot.send_message(context.message.channel, item)

# this command returns the stats for each user, at the moment that is just the number of messages
# each user has posted, but could be expanded however you'd like
@bot.command(pass_context=True)
async def stats(context):
	await bot.send_message(context.message.channel, 'ack')
	postingUsers = getPostingUsers()
	for user in postingUsers:
		userMsgs = db.search(msg.authorName == user)
		await bot.send_message(context.message.channel, '{0} has {1} messages'.format(user, len(userMsgs)))

# this function returns a list of all the users that have posted to the server
def getPostingUsers():
	postingUsers = set();
	for item in db:
		postingUsers.add(item['authorName'])

	return postingUsers

# this opens up a file named botToken.txt which should contain a single line of text; the bot's token
with open('botToken.txt', 'r') as myfile:
    botToken = myfile.read().replace('\n', '')

# start the bot
bot.run(botToken)

