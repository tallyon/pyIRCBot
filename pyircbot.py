import socket
import sys
import time
import BotController
import Raffle
import PointsManager

# Help for CLI
if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
	print "Usage: \
			\n\tpyircbot.py [COMMAND] [FILE] [SERVER] [CHANNEL] [BOT NICK] [PASSWORD] \
			\n\n\tCOMMAND: \
			\n\t\t-h, --help\t\tHelp you are seeing right now \
			\n\t\t-t, --testconfig\tTests [FILE] for being valid config file.\n\t\t\t\t\tIf no [FILE] specified use default (pyircbot.config) \
			\n\n\tExample of usage: \
			\n\n\tpython pyircbot.py irc.freenode.com \"#python\" ircbot secretpass \
			\n\tConnects to irc.freenode.com, join channel \"#python\" as ircbot and identify with password secretpass"
	sys.exit()

# Runtime argument -t or --testconfig runs config file check
if len(sys.argv) > 1 and (sys.argv[1] == "-t" or sys.argv[1] == "--testconfig"):
	# Second argument after -t or --testconfig should be config file path
	# if there's second argument parse it as config file, if not use default config file
	if len(sys.argv) == 3:
		Bot = BotController.BotController(sys.argv[2])
	else:
		Bot = BotController.BotController()

	# Print config generated from config file
	print Bot.TestConfigurationFile()
	sys.exit()

# There should be at least 4 arguments to run the bot properly or exactly 1 argument to load
if len(sys.argv) < 4:
	print "Invalid usage! Run script with flag -h or --help to see usage information."
	sys.exit()

# Create Bot controller object
Bot = BotController.BotController()

# Connect to redis server
print "Connecting to Redis server: {}".format(Bot.ConnectToRedis())

pointsMan = PointsManager.PointsManager(Bot.GetRedisInstance())
raffle = Raffle.Raffle(pointsMan)

server = sys.argv[1]
channel = sys.argv[2]
botnick = sys.argv[3]
password = ""
if(len(sys.argv) > 4):
	password = sys.argv[4]

# define the socket
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "\tAttempting to connect to:" + server + "\n"
# connect to the server
irc.connect((server, 6667))
print "\tSuccessfuly connected to: " + server + "\n"
# pass
sendStr = "PASS \n"
irc.send(sendStr)

sendStr = "NICK "+ botnick +"\n"
irc.send(sendStr)
print "\tSending " + sendStr + "\n"

# user authentication
sendStr = "USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n"
irc.send(sendStr)
print "\tSending " + sendStr + "\n"

time.sleep(3)

# auth
sendStr = "PRIVMSG nickserv :identify " + botnick + " " + password + "\r\n"
irc.send(sendStr)
print "\tSending " + sendStr + "\n"
# join channel
sendStr = "JOIN "+ channel +"\n"
irc.send(sendStr)
print "\tSending " + sendStr + "\n"

# loops to continously receive text from irc and prints it to the console
while 1:
	text = irc.recv(512)
	#print text
	splitText = text.split(':')
	index = 0
	for t in splitText:
		# Print all PRIVMSG messages in format <user>: <message>
		if t.find("PRIVMSG") != -1:
			userName = t[0:t.find(" ")]
			message = splitText[index + 1]
			# print it
			print userName + ": " + message

			# check for !raffle
			if userName.find("tallyon!") == 0:
				if message.find("!raffle") == 0:
					irc.send("PRIVMSG " + channel + " :tallyon started the raffle\n")
					# if raffle is inactive start it
					if raffle.active == False:
						sendStr = "PRIVMSG " + channel + " :" + raffle.RaffleStart() + "\n"
						irc.send(sendStr)
					# otherwise stop it and draw winner
					else:
						sendStr = "PRIVMSG " + channel + " :" + raffle.RaffleDraw() + "\n"
						irc.send(sendStr)

			# check for !join
			if message.find("!join") == 0:
				if raffle.active == True:
					points = message[message.find(' ')+1:-1]
					normalizedUsername = userName[0:userName.find("~")-1]
					raffleJoinReturned = raffle.RaffleJoin(normalizedUsername, points)
					if raffleJoinReturned != 0:
						sendStr = "PRIVMSG " + channel + " :" + raffleJoinReturned + "\n"
						irc.send(sendStr)
				else:
					sendStr = "PRIVMSG " + channel + " :Raffle is not active\n"
					irc.send(sendStr)

			# check for !points
			if message.find("!points") == 0:
				# send message to channel "<username> has <points> points"
				sendStr = "PRIVMSG " + channel + " :" + \
					userName[0:userName.find('!')] + " has " + \
					str(pointsMan.GetPoints(userName[0:userName.find('!')])) + " points\n"
				print "\t" + sendStr
				irc.send(sendStr)

		index += 1


	# if PING was received answer with PONG
	if text.find("PING") != -1:
		pingEnd = text.find(' ', text.find("PING"))
		pingMessage = text[text.find("PING"):].split(':')[0]
		print "  " + pingMessage
		sendStr = "PONG " + text.split() [0] + "\r\n"
		irc.send(sendStr)
		print " Sending: " + sendStr + "\n"
