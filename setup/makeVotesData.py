##  filename:   MakeVotesData.py
##  directory:  2016Election/code/setup
##  author:     dwzhang@princeton.edu

import pandas as pd
import numpy as np

# (0) Do cleaning on each of the election vote data files:
DataDrt = "../../data/votes/"
Years = ["2012", "2016"]

for year in Years:
	# (0.1) load data as dataframe 
	DataLoc = DataDrt + year + "CountyVotesRaw.csv"
	df_raw = pd.read_csv(DataLoc, header=1)

	# (0.2) keep only necessary columns & rename to add year info
	keep_vars = ['fips', 'name', 'totalvote', 'vote1', 'vote2']
	df = df_raw.loc[:, keep_vars]
	df = df.rename(columns = {'name': 'county_name',
							  'totalvote': 'vote_tot' + year,
							  'vote1': 'vote_dem' + year,
							  'vote2': 'vote_rep' + year})

	# (0.3) compute stats that we'll use in our analysis
	df['vote_2party' + year] = df['vote_dem' + year] + df['vote_rep' + year]
	df['vote_alt' + year] = df['vote_tot' + year] - df['vote_2party' + year]
	# non-dem, non-rep vote as a share of total votes
	df['vote_alt_share' + year] = df['vote_alt' + year] / df['vote_tot' + year]
	# dem and rep votes as a share of votes for two major parties
	for party in ['dem', 'rep']:
		df['vote_' + party + '_share' + year] = (df['vote_' + party + year] /
			df['vote_2party' + year])
	df['vote_rd_margin' + year] = (df['vote_rep_share' + year] -
		df['vote_dem_share' + year])

	# (0.4) export data as csv
	OutLoc = DataDrt + year + "CountyVotes.csv"
	df.to_csv(OutLoc, index=False)



# (1) Merge the 2012 & 2016 vote data files created in (0.4)
# (1.0) read the two dataframes 
df12 = pd.read_csv(DataDrt + '2012' + 'CountyVotes.csv')
df16 = pd.read_csv(DataDrt + '2016' + 'CountyVotes.csv')
# drop the 'county_name' column from 2016 data, to merge only on fips
df16 = df16.drop('county_name', 1)

# (1.1) do merge
# http://pandas.pydata.org/pandas-docs/stable/merging.html
del(df)
df = pd.merge(df12, df16, on='fips', indicator=True)
# can get a tabulation on a series using my_series.value_counts()