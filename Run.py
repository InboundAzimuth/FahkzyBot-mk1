import string
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Init import joinRoom
import parser

s = openSocket()
joinRoom(s)
readbuffer = ""
#components = parser.parse_command(command)

while True:
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)
			if "PING" in line:
				s.send(line.replace("PING", "PONG"))
				break
			user = getUser(line)
			message = getMessage(line)
			print user + " typed :" + message
			#You suck
			if "You suck" in message:
				sendMessage(s, "No, you suck!")
				break
			#trade
			if "!trade" in message:
				sendMessage(s, "Fahkzy's trade link: https://steamcommunity.com/tradeoffer/new/?partner=65390294&token=efmHK3WH")
				break
			#Help Command
			if "!help" in message:
				sendMessage(s, "All commands are case sensitive.")
				sendMessage(s, "I am a lazy developer.")
				sendMessage(s, "The current commands:")
				sendMessage(s, "!help, !trade")
				break