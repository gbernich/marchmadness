# Object holds winning and losing team names and seeds
class Matchup:
	def __init__(self, winner_name, winner_seed, loser_name, loser_seed):
		self.winner_name = winner_name
		self.winner_seed = winner_seed
		self.loser_name  = loser_name
		self.loser_seed  = loser_seed


# Object holds all of the matchups within its Tier (round)
# Synonomous with "Round", using Tier because "round" is a python keyword
class Tier: 
	def __init__(self, number):
		self.number   = number
		self.matchups = []

	def addMatchup(self, matchup):
		self.matchups.append(matchup)


# Object holds all of the Tiers (rounds) within the Year's tournament
# Its Tiers can be accessed in a loop with year.tierList or directly with year.tierDict['year']
class Year:
	def __init__(self, number):
		self.number      = number
		self.tierList    = []
		self.tierDict    = {}
		self.tierNumbers = []

	def addTier(self, tier):
		self.tierList.append(tier)
		self.tierDict[tier.number] = tier
		self.tierNumbers.append(tier.number)

	def hasTier(self, number):
		if number in self.tierNumbers:
			return True
		else:
			return False


# Object holds all of the Years within the Dataset
# Its Years can be accessed in a loop with data.yearList or directly with data.yearDict['year']
class Dataset:
	def __init__(self):
		self.yearList    = []
		self.yearDict    = {}
		self.yearNumbers = []

	def addYear(self, year):
		self.yearList.append(year)
		self.yearDict[year.number] = year
		self.yearNumbers.append(year.number)

	def hasYear(self, number):
		if number in self.yearNumbers:
			return True
		else:
			return False



