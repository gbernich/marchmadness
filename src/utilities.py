from bs4 import BeautifulSoup
import sys
import numpy

from objects import *


TIERS = { 'First Round'           : '64',
          'Second Round'          : '32',
          'Sweet 16'              : '16',
          'Elite Eight'           :  '8',
          'Final Four'            :  '4',
          'National Championship' :  '2'
        }

# Parse the HTML data of every tournament game
def parseData(fn):

	fp   = open(fn, 'r')
	html = fp.read()

	tmp = BeautifulSoup(html, "html.parser").findAll('tr')

	# Init data object
	data = Dataset()

	# Init records dictionary
	records = {}

	# Loop trough all raw matchups
	yIdx = -1
	tIdx = -1
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
					yIdx += 1
					tIdx  = -1

				if not data.yearList[yIdx].hasTier(tier):
					newTier = Tier(tier)
					data.yearList[yIdx].addTier(newTier)
					tIdx += 1

				#data.yearList[yIdx].tierList[tIdx].addMatchup(newMatchup)
				data.yearDict[year].tierDict[tier].addMatchup(newMatchup)

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

	for year in data.yearList:
		if year.number in excludeYears:
			continue
		#year = data.yearList[y]
		for tier in year.tierList:
			#tier = year.tierList[t]
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
	means = []

	# Calculate the mean and stdev for each year
	for year in data.yearList:
		stats[year.number] = {'scores':[], 'mean':0, 'std':0, 'zscore':0}
		for tier in year.tierList:
			if tier.number in includeTiers:
				for m in tier.matchups:
					score = 1.0 - prob[m.winner_seed][m.loser_seed]
					stats[year.number]['scores'].append(score)
					stats[year.number]['mean'] = numpy.mean(stats[year.number]['scores'])
					stats[year.number]['std']  = numpy.std( stats[year.number]['scores'])
		means.append(stats[year.number]['mean'])

	# Now get the z-score for each year
	for year in data.yearList:
		for tier in year.tierList:
			if tier.number in includeTiers:
				for m in tier.matchups:
					stats[year.number]['zscore'] = (stats[year.number]['mean'] - numpy.mean(means)) / numpy.std(means)
	
	return stats
