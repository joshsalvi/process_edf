import mne
import csv
import pandas as pd
from datetime import datetime as dt

directory = '/Users/jq210/Documents/GitHub/process_edf/example/'
fn = 'CRFS50_24Hr(at1Wk)RecordingScored.edf'

full_fn = directory + fn

# Load EDF
edf_data = mne.io.read_raw_edf(full_fn)

# Parse EDF data
raw_data = edf_data.get_data()
info = edf_data.info
channels = edf_data.ch_names

# Convert to DataFrame with PANDAS
df_edw = pd.DataFrame(columns=channels)
for ind in range(len(channels)):
	df_edw[channels[ind]] = raw_data[ind]

# Update the metadata, put into dataframe
df_meta = pd.DataFrame()
df_meta = df_meta.from_dict({'Variable': info.keys(), 'Value': info.values()},orient='index')

# Write  to CSV
output_fn = directory + fn.replace('.edf','-output.csv')
output_fn_meta = directory + fn.replace('.edf','-metadata.csv')
print('Writing raw data to ' + output_fn + ' . . .')
print('Process might take awhile.')
t0 = dt.now()
df_edw.to_csv(output_fn, sep=',', index=False) 
print('Completed in ' + str((dt.now()-t0).seconds) + ' seconds. Successfully wrote raw data in ' + str(len(channels)) + ' channels to ' + output_fn)

print('Writing metadata to ' + output_fn_meta + ' . . .')
t0 = dt.now()
df_meta.T.to_csv(output_fn_meta, sep=',', index=False)
print('Completed in ' + str((dt.now()-t0).seconds) + ' seconds. Successfully wrote metadata to ' + output_fn_meta)
