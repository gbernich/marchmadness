class Matchup:
	def __init__(self, winner_name, winner_seed, loser_name, loser_seed):
		self.winner_name = winner_name
		self.winner_seed = winner_seed
		self.loser_name  = loser_name
		self.loser_seed  = loser_seed

		self.seed_diff   = int(self.winner_seed) - int(self.loser_seed)


class Tier:
	def __init__(self, number):
		self.number   = number
		self.matchups = []
		self.seed_diff_sum = 0

	def addMatchup(self, matchup):
		self.matchups.append(matchup)
		self.seed_diff_sum += matchup.seed_diff
		m = matchup
		# print(m.winner_seed, m.winner_name, ',', m.loser_seed, m.loser_name, ',', m.seed_diff)


class Year:
	def __init__(self, number):
		self.number = number
		self.tiers  = {}

	def addTier(self, tier):
		self.tiers[tier.number] = tier

	def hasTier(self, number):
		if number in self.tiers.keys():
			return True
		else:
			return False

	def getSeedDiffSum(self, tiers):
		sum = 0
		for ii in tiers:
			if ii in self.tiers.keys():
				tier = self.tiers[ii]
				sum += tier.seed_diff_sum
		return sum


class Dataset:
	def __init__(self):
		self.years = {}

	def addYear(self, year):
		self.years[year.number] = year

	def hasYear(self, number):
		if number in self.years.keys():
			return True
		else:
			return False



