import mne
import csv
import pandas as pd
from datetime import datetime as dt
import os
import argparse as ap
import glob
import io
import logging
import numpy as np

logger = logging.getLogger(os.path.basename(__file__))

def main():
    parser = ap.ArgumentParser('EDW Extraction Pipeline')
    parser.add_argument('--study', nargs='+', help='Study name', default=['CSDP'])
    parser.add_argument('--subject', nargs='+', help='Subject ID')
    parser.add_argument('--activedir', default = '/eris/sbdp/PHOENIX/')

    args = parser.parse_args()

    directory = args.activedir
    study = args.study[0]
    subject = args.subject[0]
    files = glob.glob(directory + 'GENERAL/' + study + '/' + subject + '/edf/raw' + '/*edf')
    print('Active directory: ' + directory)
    print('Study: ' + study)
    print('Subject: ' + subject)

    for full_fn in files:
        print('Analyzing file ' + full_fn)
        # Load EDF
        edf_data = mne.io.read_raw_edf(full_fn, preload=False, verbose=False)
        print('Succesfully loaded EDF data.')

        # Parse EDF data
        print('Parsing EDF data...')
        raw_data = edf_data.get_data()
        print(raw_data)
        #info = edf_data.info
        channels = edf_data.ch_names

        print('Writing raw data to ' + full_fn.replace('.edf','-output.csv') + ' . . .')
        np.savetxt(full_fn.replace('.edf','-output.csv'), raw_data.T, delimiter=',')
        del raw_data

        # Convert to DataFrame with PANDAS
        #print('Converting to dataframe...')
        #df_edw = pd.DataFrame(columns=channels)
        #for ind in range(len(channels)):
        #    print('Running on channel ' + str(ind) + ' . . .')
        #    df_edw[channels[ind]] = raw_data[ind]
        #    #df_edw[channels[ind]] = edf_data.get_data()[ind]

        # Update the metadata, put into dataframe
        print('Updating metadata...')
        df_meta = pd.DataFrame()
        df_meta = df_meta.from_dict({'Variable': edf_data.info.keys(), 'Value': edf_data.info.values()},orient='index')

        # Write  to CSV
        #output_fn = full_fn.replace('.edf','-output.csv')
        output_fn_meta = full_fn.replace('.edf','-metadata.csv')
        #print('Writing raw data to ' + output_fn + ' . . .')
        #print('Process might take awhile.')
        #t0 = dt.now()
        #df_edw.to_csv(output_fn, sep=',', index=False)
        #print('Completed in ' + str((dt.now()-t0).seconds) + ' seconds. Successfully wrote raw data in ' + str(len(channels)) + ' channels to ' + output_fn)

        print('Writing metadata to ' + output_fn_meta + ' . . .')
        #t0 = dt.now()
        df_meta.T.to_csv(output_fn_meta, sep=',', index=False)
        #print('Completed in ' + str((dt.now()-t0).seconds) + ' seconds. Successfully wrote metadata to ' + output_fn_meta)


main()