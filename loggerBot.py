import asyncio, discord, json
from discord.ext.commands import Bot
from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import delete, increment

'''
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	SETUP
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
# Create a bot
bot = Bot(description="Channel Logger Bot by jskrist#3569", command_prefix="!", pm_help = True)
# Start or connect to a database to log the messages
db = TinyDB('data.json')
# This is a Query object to use when searching through the database
msg = Query()
usr = Query()
'''
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	HELPER FUNCTIONS
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
# this function returns a list of all the users that have posted to the server
def getPostingUsers():
	postingUsers = set();
	for item in db:
		postingUsers.add(item['authorName'])

	return postingUsers

async def addMsgToDB(message):
	# Confirm that the message did not come from this Bot to make sure we don't get
	# into an infinite loop if this bot send out any messages in this function also
	# check that the first character of the message is not a "!" or "]", which would
	# indicate a command
	if (message.author.id != bot.user.id) & \
					(message.content[0] != '!') & (message.content[0] != ']'):
		# if the mesage content is not in the database yet
		if not db.search(msg.content == message.content.lower()):
			# Insert the content into the database, along with the name of the user that posted it.
			# You could add any other data to the database at this point.
			db.insert({'content': message.content.lower(), 'authorName': message.author.name})
'''
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	BOT EVENTS AND COMMANDS
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
# This function prints a message to the terminal/command window to let you know the bot started correctly
@bot.event
async def on_ready():
	print('Bot is up and running.')

# when a message comes into the server, this function is executed
@bot.listen()
async def on_message(message):
	await addMsgToDB(message)

# when a message on the server is edited, this function is executed
@bot.listen()
async def on_message_edit(msgBefore, msgAfter):
	'''
	 update the database to reflect only the edited message.  This could create a state where a
	 duplicate message is on the server, but not represented in the database, e.g.

	 User1 sends "Hello"
	 User2 sends "Hello"

	 Database no has {'content':"hello", "authorName":"User1"}

	 User1 edits post to say "Hello World"

	 Database now has {'content':"hello world", "authorName":"User1"}
	 Should it also contain a copy of the message "hello"? since User2 also sent it?
	'''
	# db.update({'content': msgAfter.content.lower()}, msg.content == msgBefore.content.lower())
	'''
	 Alternatively, you could just add the updated message to the database:
	'''
	await addMsgToDB(msgAfter)

@bot.command(pass_context=True)
async def printDB(context):
	# this command prints out the contents of the database.  It should not be used with a large database.
	# the database will be save into a file called data.json (see line 12 of this file).
	for item in db:
		await bot.send_message(context.message.channel, item)

@bot.command(pass_context=True)
async def stats(context):
	# this command returns the stats for each user, at the moment that is just the number of messages
	# each user has posted, but could be expanded however you'd like
	postingUsers = getPostingUsers()
	for user in postingUsers:
		userMsgs = db.search(msg.authorName == user)
		await bot.send_message(context.message.channel, '{0} has {1} messages'.format(user, len(userMsgs)))

@bot.command(pass_context=True)
async def clearDB_all(context):
	# this command removes all of messages from the Database
	db.purge()

@bot.command(pass_context=True)
async def clearDB_usr(context, User=""):
	# this command removes all of messages in the Database from the given user
	db.remove(usr.authorName == User)

@bot.command(pass_context=True)
async def clearDB_msg(context, Msg=""):
	# this command removes the given messages from the Database if it exists
	db.remove(msg.content == Msg.lower())

'''
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	STARTING THE BOT
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
# this opens up a file named botToken.txt which should contain a single line of text; the bot's token
with open('botToken.txt', 'r') as myfile:
    botToken = myfile.read().replace('\n', '')

# start the bot
bot.run(botToken)

