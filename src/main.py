import sys

from utilities import *

from objects import *

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
means = []
for year in statsByYear.keys():
	s = "%s   z-score: %7.4f" % (year, statsByYear[year]['zscore'])
	print(s)
	means.append(statsByYear[year]['mean'])
	

# s = '\nOverall mean: %.4f' % (numpy.mean(means))
# print(s)
# s = 'Overall std:  %.4f\n' % (numpy.std(means))
# print(s)
