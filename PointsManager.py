class PointsManager:
	def __init__(self, r):
		self.redis = r
		if self.redis.get("tallyon") is None:
			self.redis.set("tallyon", 100)
			print "tallyon has" + self.redis.get("tallyon") + "points"
	
	def AddPoints(self, user, points):
		# If user was not found in dictionary, add him and give him 20 points
		if self.redis.get(user) is None:
			self.redis.set(user, 20)
		
		self.redis.incr(user, int(points))
		
	
	def SubtractPoints(self, user, points):
		# If user was not found in dictionary, add him and give him 20 points
		if self.redis.get(user) is None:
			self.redis.set(user, 20)
			
		if int(self.redis.get(user)) >= int(points):
			self.redis.decr(user, int(points))
			return True
		else:
			return False
	
	def GetPoints(self, user):
		# If user was not found in dictionary, add him and give him 20 points
		if self.redis.get(user) is None:
			self.redis.set(user, 20)

		return self.redis.get(user)
