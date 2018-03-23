import sys

from utilities import *

from objects import Matchup
from objects import Tier
from objects import Year
from objects import Dataset

# Get data source
if len(sys.argv) > 1:
	fn = sys.argv[1]
else:
	fn = './data/data.html'

# Parse the Data into a data structure
data = parseData(fn)

# Get statistics on data
prob        = getProbabilityOfOutcomes(data, ['2018'])
statsByYear = getStatistics(data, prob, ['64', '32']) #, '16', '8', '4', '2'])

# Print
tmp = []
for year in statsByYear.keys():
	s = "%s   mean: %.4f" % (year, statsByYear[year]['mean'])
	tmp.append(statsByYear[year]['mean'])
	print(s)

s = '\nOverall mean: %.4f' % (numpy.mean(tmp))
print(s)
s = 'Overall std:  %.4f\n' % (numpy.std(tmp))
print(s)
