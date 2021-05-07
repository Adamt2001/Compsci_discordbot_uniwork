# This code also includes a bookings.txt file which I couldn't attach to this submission.
# if you want to run the bot, in the same file directory, create a "bookings.txt" file for its full functionality.
import random
import time
import discord

botID = 3
# When the bot is active, it will store user names and the number of messages they have typed in a dictionary
visitorList = {}
userState = 0  # This will show the current state or location the user is in
loginAttempts = 0  # loginAttempts set to 0 as default for the staff access function
# Access to staff login set to false as default meaning from start the user will have to input the password to gain
# access
access = False
channel = 0  # This will be set to the channel ID as soon as the bot is ran
# Stores contact details of module tutors in an embedded dictionary
contactDetails = {"naveed": {"name": "Naveed Anwar",
                             "email": "",
                             "hours": "Mondays 12.00-13.00 hrs, Fridays 15.30-16.30 hrs",
                             "location": "Ellison Building Block B Room 121"},
                  "david": {"name": "David Hastings",
                            "email": "",
                            "hours": "Tuesdays 11:00 - 12:00. Thursdays 11:00 - 12:00",
                            "location": "CIS Building Room 308"},
                  "nick": {"name": "Nick Dalton",
                           "email": "",
                           "hours": "",
                           "location": "308 CIS Building"},
                  "alun": {"name": "Alun Moon",
                           "email": "",
                           "hours": "Working hours unavailable",
                           "location": "Ellison Bldg"},
                  "colin": {"name": "Colin Goodlet",
                            "email": "",
                            "hours": "Working hours unavailable",
                            "location": "Ellison Bldg"},
                  "petia": {"name": "Petia Sice",
                            "email": "",
                            "hours": "Working hours unavailable",
                            "location": "Ellison Bldg"},
                  "jill": {"name": "Jill Bradnum",
                           "email": "",
                           "hours": "Working hours unavailable",
                           "location": "Ellison Bldg"},
                  "biddy": {"name": "Biddy Casselden",
                            "email": "",
                            "hours": "Working hours unavailable",
                            "location": "Ellison Bldg"},
                  "ali": {"name": "Alison Pickard",
                          "email": "",
                          "hours": "Working hours unavailable",
                          "location": "Ellison Bldg"},
                  "shelagh": {"name": "Shelagh Keogh",
                              "email": "",
                              "hours": "Working hours unavailable",
                              "location": "Ellison Bldg"}}

# creating an array of generic error responses to make my bot feel more human with multiple different responses to
# an unknown command.
error = ["I'm sorry, I didn't understand that. You could try typing __**help**__ if you are stuck.",
                 "Pardon me, I didn't understand your request :confused:.",
                 "I didn't understand that, please try again. Remember __**help**__ can give you a prompt too.",
                 "I found that difficult to understand :thinking_face:. Please try again.",
                 ":thinking_face: I'm sorry, I didn't understand that request. Try __**help**__ if you are stuck.",
                 "I can't work out what you are trying to say, try typing __**help**__ to see a list of commands.",
                 "That request was a mystery to me :face_with_monocle:, please try again."]


# def setup will run on start, generating a random welcome message for the user.
# this will run when the bot is booted up, generating a random greeting from the set array
def setup():
    greetings = ["I am an on-campus staff/student tutorial booking system and I am ready to help!",
                 "Hello, I'm a tutorial booking system for staff and students!",
                 "Hey, I am an on-campus tutorial booking system, how can I help you today?",
                 "Hello there, I am a staff and student tutorial booking system and I am ready to help!",
                 "Nice to see you here, give me a second to warm up and say hello, I can help you with booking a "
                 "tutorial.",
                 ":wave: Hi there, I am on on-campus tutorial booking system!"]
    result = random.choice(greetings)
    return result


# End of  method setup


async def overheard(message, user):  # main function to listen to user messages, this will be the main hub
    global userState, visitorList, error

    if user in visitorList:
        visitorList[user] = visitorList[user] + 1  # adds one to the message counter
    else:
        visitorList[user] = 1  # If user is new, it will create a new user in the visitor list with the value 1
        return "Hi " + user + ". I don't think we've met before. I'm a tutorial booking system." \
                              "  If you are a staff member looking for your bookings," \
                              " type __**staff**__, or __**help**__ for students. (for testing purposes, the password" \
                              " for the staff login is Admin_ this is case sensitive) "

    # This will allow the user to see the visitors of the bot and how many times they have messaged
    if "visitors" in message.lower():
        s = "__**The visitors are:**__"
        for user in visitorList:
            s = s + "\n> " + str(user) + " " + str(visitorList[user])
        return s

    # These If statements are used to detect user inputs, if one is detected, it will run the relevant function
    if "help" in message.lower() or "options" in message.lower() or userState == 1:
        return await bothelp(message, user)

    if "hello" in message.lower() or "hi" in message.lower() or userState == 2:
        return await bothello(message, user)

    if "contact" in message.lower() or userState == 3:
        return await contactinfo(message)

    if "staff" in message.lower() or userState == 4:
        return await botstaff(message, user)

    if "book a tutorial" in message.lower() or "book tutorial" in message.lower() or userState == 5:
        return await tutorialbooking(message, user)

    if "check a booking" in message.lower() or "check booking" in message.lower() or userState == 6:
        return await checkbooking(message, user)

    if "cancel a booking" in message.lower() or "cancel booking" in message.lower() or userState == 7:
        return await cancelbooking(message, user)

    if "thanks" in message.lower() or "thank you" in message.lower() or "cheers" in message.lower():
        return "No problem, Happy to help! :grin:"

    if "bye" in message.lower() or "goodbye" in message.lower() or "cya" in message.lower():
        return "See you next time. If you need help again, just say __**help**__ :grin:"

    if "what do you do" in message.lower() or "what can you do" in message.lower():
        return "I am a tutorial booking system to book, view and cancel tutorials, type __**help**__ to find commands"

    if userState == 8:
        return await staffaccess(message, user)

    # If the user types something that inst in the about IF statements, this generic error message will display with
    # a prompt if the user has never used this bot before
    else:
        return random.choice(error)


# user state 1 (help section)
async def bothelp(message, user):
    global userState

    if "help" in message.lower() or "options" in message.lower():
        userState = 1  # This will change the user state to lock them into this function, until something has happened
    if userState == 1:
        if "list" in message.lower():
            userState = 0
            reply = "**__As a student, you can:__**\n> ○ Help and more Information\n> ○ Say Hello\n> ○ Get contact " \
                    "information about a lecturer\n> ○ Staff Login\n> ○ Book a Tutorial\n> ○ Check a Booking\n> ○ " \
                    "Cancel a Booking\n> ○ Check the Visitors\n ** Simply type what you would like to do!**"
            return reply
        elif "booking" in message.lower():
            userState = 0
            reply = '> ○ To book a tutorial, say __**book a tutorial**__\n> ○ To cancel a booking, say __**cancel a ' \
                    'booking**__\n> ○ To check when your booking is, say __**check a booking**__ '
            return reply
        elif "back" in message.lower():
            userState = 0
            return "No problem, just say __**help**__ if you ever get stuck."
        else:  # This will prompt the user what to say within the function
            reply = 'Hey ' + user + ', type __**list**__ or __**bookings**__ for more information or __**back**__ ' \
                                    'to exit. '
            return reply


# user state 2 (say hello)
async def bothello(message, user):
    global userState

    if "hello" in message.lower():
        userState = 2
    if userState == 2:
        userState = 0
        return "Hello " + user + ", I hope you are having a nice day, " \
                                 "if there is anything I can help you with, just say __**help**__."


# user state 3 (contact info)
async def contactinfo(message):
    global userState, contactDetails

    if "contact" in message.lower():
        userState = 3
        return "Please enter the name of the lecturer to find more info, type __**list**__ for a list of lecturers " \
               "or type __**back**__ to return to the normal bot. "
    if userState == 3:
        reply = f'__**Information about "{message}"**__\n> '  # Creates a default start to the message

        # Checks if a lecturer in the dictionary is in the users message, and apeneds it to the reply variable before
        # returning it to the user. This will ensure what the user sees is well formatted.
        if "naveed" in message.lower():
            userState = 0
            reply = reply + contactDetails["naveed"]["name"] + \
                    "\n> " + contactDetails["naveed"]["email"] + \
                    "\n> " + contactDetails["naveed"]["hours"] + \
                    "\n> " + contactDetails["naveed"]["location"]
            return reply
        elif "david" in message.lower():
            userState = 0
            reply = reply + contactDetails["david"]["name"] + \
                    "\n> " + contactDetails["david"]["email"] + \
                    "\n> " + contactDetails["david"]["hours"] + \
                    "\n> " + contactDetails["david"]["location"]
            return reply
        elif "nick" in message.lower():
            userState = 0
            reply = reply + contactDetails["nick"]["name"] + \
                    "\n> " + contactDetails["nick"]["email"] + \
                    "\n> " + contactDetails["nick"]["hours"] + \
                    "\n> " + contactDetails["nick"]["location"]
            return reply
        elif "alun" in message.lower():
            userState = 0
            reply = reply + contactDetails["alun"]["name"] + \
                    "\n> " + contactDetails["alun"]["email"] + \
                    "\n> " + contactDetails["alun"]["hours"] + \
                    "\n> " + contactDetails["alun"]["location"]
            return reply
        elif "colin" in message.lower():
            userState = 0
            reply = reply + contactDetails["colin"]["name"] + \
                    "\n> " + contactDetails["colin"]["email"] + \
                    "\n> " + contactDetails["colin"]["hours"] + \
                    "\n> " + contactDetails["colin"]["location"]
            return reply
        elif "petia" in message.lower():
            userState = 0
            reply = reply + contactDetails["petia"]["name"] + \
                    "\n> " + contactDetails["petia"]["email"] + \
                    "\n> " + contactDetails["petia"]["hours"] + \
                    "\n> " + contactDetails["petia"]["location"]
            return reply
        elif "jill" in message.lower():
            userState = 0
            reply = reply + contactDetails["jill"]["name"] + \
                    "\n> " + contactDetails["jill"]["email"] + \
                    "\n> " + contactDetails["jill"]["hours"] + \
                    "\n> " + contactDetails["jill"]["location"]
            return reply
        elif "biddy" in message.lower():
            userState = 0
            reply = reply + contactDetails["biddy"]["name"] + \
                    "\n> " + contactDetails["biddy"]["email"] + \
                    "\n> " + contactDetails["biddy"]["hours"] + \
                    "\n> " + contactDetails["biddy"]["location"]
            return reply
        elif "ali" in message.lower() or "alison" in message.lower():
            userState = 0
            reply = reply + contactDetails["ali"]["name"] + \
                    "\n> " + contactDetails["ali"]["email"] + \
                    "\n> " + contactDetails["ali"]["hours"] + \
                    "\n> " + contactDetails["ali"]["location"]
            return reply
        elif "shelagh" in message.lower():
            userState = 0
            reply = reply + contactDetails["shelagh"]["name"] + \
                    "\n> " + contactDetails["shelagh"]["email"] + \
                    "\n> " + contactDetails["shelagh"]["hours"] + \
                    "\n> " + contactDetails["shelagh"]["location"]
            return reply

        # this is used to show a list of all the lecturers in the dictionary
        elif "list" in message.lower():
            response = "__**The list of available lecturers are:**__" + \
                       "\n> ○ " + contactDetails["jill"]["name"] + " **Foundation year Leader**" + \
                       "\n> ○ " + contactDetails["naveed"]["name"] + \
                       "\n> ○ " + contactDetails["nick"]["name"] + \
                       "\n> ○ " + contactDetails["alun"]["name"] + \
                       "\n> ○ " + contactDetails["colin"]["name"] + \
                       "\n> ○ " + contactDetails["petia"]["name"] + \
                       "\n> ○ " + contactDetails["david"]["name"] + \
                       "\n> ○ " + contactDetails["biddy"]["name"] + \
                       "\n> ○ " + contactDetails["ali"]["name"] + \
                       "\n> ○ " + contactDetails["shelagh"]["name"] + \
                       "\nType __**back**__ to cancel"
            return response

        # this creates a way back to the overheard function
        elif "back" in message.lower():
            userState = 0
            return "No problem!"
        else:
            return "I'm sorry, I dont have that lecturer listed down, get them to contact the bot owner to set up a " \
                   "profile :) "


# user state 4 (staff login)
# This is the password I have set to create a small security door to viewing the whole database.
# the user will need to know the exact password, and guess it within 3 tries before being locked out.
# this will mean as long as the bot is running, that user wont be able to access the staff area.
# if the user guesses the password correctly, it will change access to True and allow them to continue.
async def botstaff(message, user):
    global userState, loginAttempts, visitorList, access

    if "staff" in message.lower() and loginAttempts < 3:
        userState = 4
        return "Welcome " + user + ", to the staff login portal, you have 3 attempts at the password. \n" \
                                   "To login, enter your password or type __**back**__ to return to the normal bot"

    if loginAttempts > 3:
        userState = 0
        return "I'm sorry, you have tried to login before and entered the password wrong too many times, " \
               "you no longer have access to the staff portal. "

    if userState == 4 and loginAttempts < 3:
        if "Admin_" in message and loginAttempts < 3:
            loginAttempts = 0
            access = True
            return await staffaccess(message, user)
        elif "back" in message.lower():
            userState = 0
            loginAttempts = 0
            return "No problem, taking you out of the staff login portal now."
        else:
            loginAttempts += 1
            # this is for a better user experience, creating two different options if you have and 1 try or 2 tries
            if loginAttempts == 1:
                response = "Incorrect password, you have had " + str(loginAttempts) + " try."
                return response
            elif loginAttempts < 3:
                response = "Incorrect password, you have had " + str(loginAttempts) + " tries."
                return response
            elif loginAttempts >= 3:
                userState = 0
                return "Access Denied"
    else:
        return "You no longer have access to the staff login, Contact bot owner to reset the login attempts."


# user state 5 (book a tutorial)
async def tutorialbooking(message, user):
    global userState

    if "book a tutorial" in message.lower() or "book tutorial" in message.lower():
        userState = 5
        return "please enter the following details in one line: (type __**back**__ to return to the normal bot)" \
               "\nStudent ID Full name Lecturers name dd/mm/yyyy time"
    if "back" in message.lower():
        userState = 0
        return "No problem!"
    elif userState == 5:
        # opens the txt file and appends the users input onto a new line
        f = open("bookings.txt", "a+")
        booking = user + " " + message + "\n"
        f.write(booking)
        f.close()
        userState = 0

        return "Thank you, your tutorial has been booked, to view your tutorials, type __**Check a booking **__ or " \
               "to cancel, type __**cancel a booking**__ "


# user state 6 (check when a booking is)
# opens the file, and compares it to the message to check if the student ID is in the database.
# if it is, it will return it to the user, if it cant find a match, it will prompt with a generic message.
async def checkbooking(message, user):
    global userState

    response = ""
    if "check a booking" in message.lower() or "check booking" in message.lower():
        userState = 6
        return "To check a booking, please enter your __**name**__, or to return type __**back**__"
    if "back" in message.lower():
        userState = 0
        return "No problem! Sending you back now :grin:"
    elif userState == 6:
        f = open("bookings.txt", "r+")
        for line in f:
            if user in line:
                response = response + line
        f.close()
        await channel.send("Searching for your request :hourglass_flowing_sand: ")
        time.sleep(2)
        if response == "":
            userState = 0
            return "I'm Sorry, I couldn't find any details under your name. Sending you back now."
        else:
            userState = 0
            await channel.send("__**Below is a list of bookings with the name:**__ " + message)
            return response


# user state 7 (cancel bookings)
async def cancelbooking(message, user):
    global userState

    response = ""
    if "cancel a booking" in message.lower() or "cancel booking" in message.lower():
        userState = 7
        return "Please enter your __**name**__ to cancel all bookings under that name, or __**back**__ to return."
    if "back" in message.lower():
        userState = 0
        return "No problem, sending you back now."
    elif userState == 7:
        # opens the original file in read/write mode
        with open("bookings.txt", "r+") as f:
            working = f.readlines()
            f.seek(0)
            for line in working:
                if user not in line:  # check to see if the user is not in the line
                    f.write(line)  # if not, then it will re write the line
                else:
                    response = response + line
            f.truncate()  # this will shorten the file if there are blank spaces when removing data

        if response == "":
            userState = 0
            return "I'm Sorry, I couldn't find any details under your name. Sending you back now."
        else:
            userState = 0
            await channel.send("__**Below is a list of canceled bookings with the name:**__ " + message)
            return response


# user state 8 (staff access) checks to see if the user has entered the correct password and gives the user the
# option to view the booked tutorials or to logout
async def staffaccess(message, user):
    global userState, loginAttempts, access, error

    if access:
        userState = 8
        access = False
        return "Would you like to see the booked tutorials, or logout?\n> __**tutorials**__ \n> __**logout**__"
    if userState == 8:
        if "tutorials" in message.lower():
            f = open("bookings.txt", "r")
            lines = f.read()  # stores all of the data from the bookings.txt file into a temporary variable
            f.close()
            userState = 0
            await channel.send("__Here are all the booked tutorials!__\n" + ">>> " + lines)
            return "\n Thanks for logging in, see you again next time. "
        elif "logout" in message.lower():
            userState = 0
            loginAttempts = 0
            return "You have successfully been logged out. Thank you " + user + "."
            # logs the user out by changing the access to false, reseting the login attempts and returning userstate
            # back to 0
        else:
            return random.choice(error)


# END of  method overheard

# IGNORE EVERYTHING BELOW FOR NOW

client = discord.Client()
botChannel = "bot" + str(botID)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord! <')
    # print out serve name and id
    for guild in client.guilds:
        print("Server/Guild", guild.name, guild.id)
        # print out the members on this server.
        for member in guild.members:
            print("Member", member)

    time.sleep(3)

    for guildServer in client.guilds:
        chn = discord.utils.get(guildServer.text_channels, name=botChannel)
        print(f'{botChannel} found ', chn)
        message = setup()  # "I have arrived on " + botChannel
        if not (chn is None):
            await chn.send(content=message)


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    print('***TELLS', message.author.name, client.user.name)
    if message.author == client.user:
        return
    if message.author.name in client.user.name:
        return
    if message.channel.name != botChannel:
        return

    if "CodeWrangleBot" in message.author.name or "CodeWranglingBot" in message.author.name:
        return

    print("** OK ", message.author.name, client.user.name)
    global channel
    channel = client.get_channel() # add channel number here

    response = await overheard(message.content, message.author.name)  # "I hear what you say"
    await message.channel.send(response)


Tokens = []  # working # add tokens here

TOKEN = Tokens[botID % len(Tokens)]
print(TOKEN, botID % len(Tokens))

DISCORD_GUILD = 'Codewrangling'
client.run(TOKEN)
