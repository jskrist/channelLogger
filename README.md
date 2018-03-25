# channelLogger
This is a bot that logs unique messages from a Discord channel and information about the user that posted the message.  It also allows for management of this data, so you can get a report of how many messages each user has contributed, as well as delete entries from the log either by user, or by message, or wipe the entire log.  It is intended to be a starter bot that introduces some of the basic staeps required to create a bot.

## How to create a Discord Bot

### Step 1 - Create a Application on Discord

To use this bot, you will need to create a discord Application:

https://discordapp.com/developers/applications/me

There are plenty of guides for how to do this e.g.

https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token

As part of this process you will create a token for your Bot.  This token is a random string of characters that is unique to your bot and allows Discord to regocnize and authenticae your application.  To use this code, you will need to create a text file named:

botToken.txt

and put your Bot's token as the only content of this file.

**NOTE:** Do **NOT** commit this file to your Git Repo, or otherwise share this token with anyone.  If you do, they can use this token to authenticate their code as though it was your bot.  If you believe your token is comprimised, follow the steps in the link above to reset your application token.

### Step 2 - Git This Repository

You can either clone/fork the repo, or download it as an archive file (e.g. \*.zip), but you will need to get the code in one way or another.  You can find the code at:

https://github.com/jskrist/channelLogger

### Step 3 - Update Code For Your Application

You will need to update different sections of this code for your needs, i.e.

* When creating the 'bot' variable:
  * You can put your own bot description and specify your own command prefix character.
* when creating the 'db' variable:
  * you can name your database file anything you want (\*.json)

Read through the commands and helper files, and feel free to tweak any logic you need to for this bot to do what you want, with one exception:

__The end of the file opens the "botToken.txt" file and uses the token stored in there to run the bot.  You are welcome to change the name of the file being read to correspond to the file you created, but I **strongly** suugest, not hardcoding the bot token in this file.__

