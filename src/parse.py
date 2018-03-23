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

if len(sys.argv) > 1:
	fn = sys.argv[1]
else:
	fn = 'data.html'

fp   = open(fn, 'r')
html = fp.read()

# tmp = BeautifulSoup(html, "html.parser").findAll('td', {'class': 'year'})
tmp = BeautifulSoup(html, "html.parser").findAll('tr')

# Init data object
data = Dataset()

# Loop trough all raw matchups
for game in tmp:

	try:
		year        = game.find('td', {'class':'year' }).find('a'   ).getText()

		# Only process 2017 and earlier
		if (int(year) < 2019):
			tier        = game.find('td', {'class':'round'}).find('span').getText()
			winner_name = game.find('td', {'class':'win'  }).find('span').getText()
			winner_seed = game.find('td', {'class':'win'  }).findPrevious().getText()
			loser_name  = game.find('td', {'class':'lose' }).find('span').getText()
			loser_seed  = game.find('td', {'class':'lose' }).findPrevious().getText()

			newMatchup = Matchup(winner_name, winner_seed, loser_name, loser_seed)

			tier = TIERS[tier]

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

	except:
		#print('SKIP')
		#print(game)
		continue


# Print results for each year
diffs = []
for ii in data.years.keys():
	year = data.years[ii]
	print(year.number, year.getSeedDiffSum(['64','32']))
	diffs.append(year.getSeedDiffSum(['64','32']))


# Statistics
diff_mean = numpy.mean(diffs)
s = '\nmean: %.1f' % diff_mean
print(s)

diff_std = numpy.std(diffs)
s = 'std:  %.1f\n' % diff_std
print(s)

