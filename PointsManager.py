class PointsManager:
	def __init__(self, r):
		#self.userPointsDict = {"tallyon": 100}
		self.redis = r
		if self.redis.get("tallyon") is None:
			self.redis.set("tallyon", 100)
		print "Tallyon has" + self.redis.get("tallyon") + "points"
	
	def AddPoints(self, user, points):
		# If user was not found in dictionary, add him and give him 20 points
		#if user not in self.userPointsDict:
		if self.redis.get(user) is None:
			#self.userPointsDict[user] = 20
			self.redis.set(user, 20)
		
		#self.userPointsDict[user] += points
		self.redis.incr(user, int(points))
		
	
	def SubtractPoints(self, user, points):
		# If user was not found in dictionary, add him and give him 20 points
		#if user not in self.userPointsDict:
			#self.userPointsDict[user] = 20
		if self.redis.get(user) is None:
			self.redis.set(user, 20)
		
		#if self.userPointsDict[user] >= int(points):
			#self.userPointsDict[user] -= int(points)
			
		if int(self.redis.get(user)) >= int(points):
			self.redis.decr(user, int(points))
			return True
		else:
			return False
	
	def GetPoints(self, user):
		# If user was not found in dictionary, add him and give him 20 points
		#if user not in self.userPointsDict:
			#self.userPointsDict[user] = 20
		if self.redis.get(user) is None:
			self.redis.set(user, 20)

		return self.redis.get(user)
