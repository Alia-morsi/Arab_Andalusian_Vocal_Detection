#should be run from top level directory for the paths to make sense

import parselmouth
from parselmouth.praat import call
from os.path import isfile, join 
from os import listdir
from math import floor
import numpy as np
import pandas as pd
import csv

path_to_annot = "preprocessing/csv/"
path_to_music = "preprocessing/audio/"
path_to_intervals = "preprocessing/scripts/"

f0min = 50
f0max = 600

#load the frame intervals file
#load audio files with parselmouth

annot_files = [fi for fi in listdir(path_to_annot) if isfile(join(path_to_annot, fi))]
music_files = [fi for fi in listdir(path_to_music) if isfile(join(path_to_music, fi))]
interval_files = [fi for fi in listdir(path_to_intervals) if isfile(join(path_to_intervals, fi)) and fi[-4:] == ".csv"]

sound = parselmouth.Sound(path_to_music +'7448d9c2-5261-4e70-bd98-6ed8416f908f.wav')

#split the interval file names
#make a dictionary of intervals by mbid name: to vocal vs instrumental

intervals = {}
print("Number of Interval Files: {}".format(len(interval_files)))

for fi in interval_files:
	df = pd.read_csv(path_to_intervals + fi)
	#print(df)
	print(path_to_intervals + fi)
	interval_type = fi.split('_')
	mbid_name = interval_type[1].split('.')
	if mbid_name[0] not in intervals:
		intervals[mbid_name[0]] = {}
	intervals[mbid_name[0]][interval_type[0]] = list(zip(df.iloc[:, 0], df.iloc[:, 1]))
	
print(len(intervals))
print(len(intervals['f7bcb9af-6abb-4192-ae3d-37fa811034ce']))
	 
#setting an mbid index:
#matrix_pd = matrix_pd.assign(mbid=mbids)
#matrix_pd.set_index('mbid', inplace=True)
#matrix_pd.columns = subgenres


	
for key, value in intervals.items(): #for all files
	sound = parselmouth.Sound(path_to_music + key + '.wav')
	for inner_key, inner_value in intervals[key].items(): #vocal and instrumental
		#make the size of the matrix for speed considerations
		x = np.empty(shape=(len(inner_value), 2)) # because we only will calculate 2 values from parselmouth
		df = pd.DataFrame(x)
		col_labels = ['local_jitter', 'local_shimmer'] 	#labels we will set as the column title in the dataframes
		df.columns = col_labels

		#add the column names to the dataframe
		#so that we can add the rows one by one
		filename = "{}-{}-parsel.csv".format(inner_key, key)
		for i, item in enumerate(inner_value):	#going over the interval tuples
			start = item[0]
			end = item[1]
			snippet = sound.extract_part(from_time=start, to_time=end, preserve_times=True)
			pitch = call(snippet, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
			pointProcess = call(snippet, "To PointProcess (periodic, cc)", f0min, f0max)
			localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
			localShimmer =  call([snippet, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
			df.iloc[i, 0] = localJitter
			df.iloc[i, 1] = localShimmer
			print("snippet {} of file {}".format(i, filename))

		df.to_csv(path_to_intervals + filename)



