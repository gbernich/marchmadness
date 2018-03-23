from bs4 import BeautifulSoup
import sys
import numpy

from objects import Matchup
from objects import Tier
from objects import Year
from objects import Dataset

TIERS = { 'First Round'           : '64',
          'Second Round'          : '32',
          'Sweet 16'              : '16',
          'Elite Eight'           :  '8',
          'Final Four'            :  '4',
          'National Championship' :  '2'
        }

def parseData(fn):

	fp   = open(fn, 'r')
	html = fp.read()

	tmp = BeautifulSoup(html, "html.parser").findAll('tr')

	# Init data object
	data = Dataset()

	# Init records dictionary
	records = {}

	# Loop trough all raw matchups
	for game in tmp:

		try:
			year = game.find('td', {'class':'year' }).find('a'   ).getText()

			# Only process 2017 and earlier
			if (int(year) < 2019):
				tier        = game.find('td', {'class':'round'}).find('span').getText()
				winner_name = game.find('td', {'class':'win'  }).find('span').getText()
				winner_seed = game.find('td', {'class':'win'  }).findPrevious().getText()
				loser_name  = game.find('td', {'class':'lose' }).find('span').getText()
				loser_seed  = game.find('td', {'class':'lose' }).findPrevious().getText()

				newMatchup = Matchup(winner_name, winner_seed, loser_name, loser_seed)

				tier = TIERS[tier]

				# Add to data structure
				if not data.hasYear(year):
					newYear = Year(year)
					data.addYear(newYear)
					# print(newYear.number)

				if not data.years[year].hasTier(tier):
					newTier = Tier(tier)
					data.years[year].addTier(newTier)
					# print(newTier.number)

				data.years[year].tiers[tier].addMatchup(newMatchup)
				#print(newMatchup.winner_name)

				# # Update the records
				# if winner_seed not in records.keys():
				# 	records[winner_seed] = {}
				# if loser_seed not in records[winner_seed].keys():
				# 	records[winner_seed][loser_seed] = {'wins' : 0, 'losses' : 0}

				# if loser_seed not in records.keys():
				# 	records[loser_seed] = {}
				# if winner_seed not in records[loser_seed].keys():
				# 	records[loser_seed][winner_seed] = {'wins' : 0, 'losses' : 0, 'weight' : 0}

				# records[winner_seed][loser_seed]['wins']   += 1
				# records[loser_seed][winner_seed]['losses'] += 1
				# records[winner_seed][loser_seed]['weight'] = records[winner_seed][loser_seed]['losses'] / (records[winner_seed][loser_seed]['wins'] + records[winner_seed][loser_seed]['losses'])
				# records[loser_seed][winner_seed]['weight'] = records[loser_seed][winner_seed]['losses'] / (records[loser_seed][winner_seed]['wins'] + records[loser_seed][winner_seed]['losses'])
		
		except Exception as e:
			#print('SKIP')
			#print(game)
			#print(e)
			continue

	return data


# Use the historical data to determine the probability of it occuring
def getProbabilityOfOutcomes(data, excludeYears):
	
	# Start by adding up the records of one seed against another
	records = {}

	for y in data.years.keys():
		if y in excludeYears:
			continue
		year = data.years[y]
		for t in year.tiers.keys():
			tier = year.tiers[t]
			for m in tier.matchups:

				if m.winner_seed not in records.keys():
					records[m.winner_seed] = {}
				if m.loser_seed not in records[m.winner_seed].keys():
					records[m.winner_seed][m.loser_seed] = {'wins' : 0, 'losses' : 0}

				if m.loser_seed not in records.keys():
					records[m.loser_seed] = {}
				if m.winner_seed not in records[m.loser_seed].keys():
					records[m.loser_seed][m.winner_seed] = {'wins' : 0, 'losses' : 0}

				records[m.winner_seed][m.loser_seed]['wins']   += 1
				records[m.loser_seed][m.winner_seed]['losses'] += 1


	# Calculate the probability of each seed matchup
	prob = {}

	for ii in range(1,17):
		for jj in range(1,17):

			w = str(ii)
			l = str(jj)

			if w not in prob.keys():
				prob[w] = {}
			if l not in prob[w].keys():
				prob[w][l] = -1

			if l not in prob.keys():
				prob[l] = {}
			if w not in prob[l].keys():
				prob[l][w] = -1

			try:
				prob[w][l] = records[w][l]['wins']   / (records[w][l]['wins'] + records[w][l]['losses'])
				prob[l][w] = records[w][l]['losses'] / (records[w][l]['wins'] + records[w][l]['losses'])
			except Exception as e:
				# This means there was no data
				#print("Warning: no data for " + w + " vs " + l)
				prob[w][l] = 1 - (15 + int(w) - int(l)) / 30
				prob[l][w] = 1 - (15 + int(l) - int(w)) / 30
				#print(prob[w][l], prob[l][w])

	return prob

def getStatistics(data, prob, includeTiers):

	stats = {}

	for y in data.years.keys():
		year = data.years[y]
		stats[y] = {'scores':[], 'mean':0, 'std':0}
		for t in year.tiers.keys():
			if t in includeTiers:
				tier = year.tiers[t]
				for m in tier.matchups:
					score = 1.0 - prob[m.winner_seed][m.loser_seed]
					stats[y]['scores'].append(score)
					stats[y]['mean'] = numpy.mean(stats[y]['scores'])
					stats[y]['std']  = numpy.std( stats[y]['scores'])

	return stats

# # Print results for each year
# diffs = []
# for ii in data.years.keys():
# 	year = data.years[ii]
# 	#print(year.number, year.getSeedDiffSum(['64','32']))
# 	#diffs.append(year.getSeedDiffSum(['64','32']))
# 	x = year.getUpsetSum(['64','32'], records) / 48
# 	diffs.append(x)
# 	s = '%s %.4f' % (ii, x)
# 	print(s)


# # Statistics
# diff_mean = numpy.mean(diffs)
# s = '\nmean:   %.4f' % diff_mean
# print(s)

# diff_std = numpy.median(diffs)
# s = 'median: %.4f\n' % diff_std
# print(s)

# print(records['5']['12']['wins'], records['5']['12']['losses'])
# print(records['12']['5']['wins'], records['12']['5']['losses'])
