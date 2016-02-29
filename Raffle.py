import random
# Raffle - after authorized user sends !raffle in irc all users can send !join <points> to join the raffle
# with <points> points that are immediately subtracted from their points pool. When authorized user sends !raffle
# again the winner receives all the points accumulated in the raffle and the raffle stops.
# Every user is stored in the redis database, new users are inserted into database and given starting points (20)
class Raffle:
	"""Handles raffles in chat. !join to participate. Stores usernames in local file"""
	def __init__(self, pointsManager):
		# Create set to store users who joined the raffle
		self.usersJoined = []
		self.winner = ""
		self.numberOfPoints = 0
		self.pointsManager = pointsManager
		self.active = False

	def RaffleStart(self):
		"""Sends instructions about the raffle to the chat"""
		self.active = True
		return "Raffle has started! Type !join to participate."

	def RaffleJoin(self, username, points):
		"""Adds username to the raffle with points. User can join raffle only once"""
		# Check if user already joined the raffle
		if username not in self.usersJoined:
			# Check if PointsManager successfuly subtracted points from the user
			if self.pointsManager.SubtractPoints(username, points) == True:
				self.usersJoined.append(username)
				self.numberOfPoints += int(points)
				return 0
			else:
				return username + " unable to join: not enough points! Have " + str(self.pointsManager.GetPoints(username)) + \
							" joined with " + str(points)
		else:
			return username + " already joined the raffle!"

	def RaffleDraw(self):
		"""Draws the winner of the raffle and gives him all the points"""
		# draw the winner
		if len(self.usersJoined) == 0:
			returnStr = "Raffle is empty :("
		else:
			self.winner = random.choice(self.usersJoined)
			self.pointsManager.AddPoints(self.winner, self.numberOfPoints)
			returnStr = self.winner + " won the raffle with " + str(self.numberOfPoints) + " points!"

		self.active = False
		return returnStr

