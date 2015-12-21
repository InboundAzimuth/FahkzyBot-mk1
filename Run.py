import parser
import time
import datetime
import string
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Init import joinRoom

nameint = 0
s = openSocket()
joinRoom(s)
readbuffer = ""
start_time = time.time()

#I KNOW HOW SHIT THIS BOT IS, BUT HONESTLY. I DON'T CARE :D
#I WAS BORED WHEN I MADE THIS
#Copyright please Fahkzy

while True:
		readbuffer = readbuffer + s.recv(4096)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)
			if "PING" in line:
				s.send(line.replace("PING", "PONG"))
				sendMessage(s, "I just recieved a ping, and sent back a pong!")
				break
			user = getUser(line)
			message = getMessage(line).upper()
			print user + " typed :" + message
			#You suck and bad
			if "YOU SUCK" in message in message:
				sendMessage(s, "No, you suck!" + user)
				break
			#trade
			if "!TRADE" in message:
				sendMessage(s, "Fahkzy's trade link: https://steamcommunity.com/tradeoffer/new/?partner=65390294&token=efmHK3WH")
				break
			#Help Command
			if "!HELP" in message:
				sendMessage(s, "I am a lazy developer.")
				sendMessage(s, "The current commands:")
				sendMessage(s, "!help, !rules, !trade, !source, and !uptime")
				sendMessage(s, "If it breaks... Well shit, I coded this in a hour")
				break
			#Hai
			if "HI" in message:
				sendMessage(s, "Hai I'm a bot!")
				break
			#Uptime
			if "!UPTIME" in message:
				end_time = time.time()
				uptime = end_time - start_time
				uptime = str(datetime.timedelta(seconds=int(uptime)))
				sendMessage(s,"I've been in my box for this long; " + uptime)
				break
			#Source
			if "!SOURCE" in message:
				sendMessage(s, "Yeah... I think it's on github. Maybe.")
				break
			#"Rules"
			if "!RULES" in message:
				sendMessage(s,"Just be nice please, we're all here to have a fun time! :D")
				break
			#Colour Testing
			if "fahkzy" in user:
				if "!COLOR ORANGE" in message:
					sendMessage(s, "/color OrangeRed")
				break
				if "!COLOR BLUE" in message:
					sendMessage(s, "/color CadetBlue")
				break
			##TESTINGSTUFF##################################
			if ("!" in message) or ("?" in message):
				nameint += 1
				break
			if "!COUNT" in message:
				sendMessage(s,"The number of !'s and ?'s I've seen are: " + str(nameint))
				break
			################################################
