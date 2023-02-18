import os,logging
import pytest
import glob
import pandas as pd
import mrf

# This test script runs any *.json files in the project's /test/ directory
# and compares the resulting CSV with a matching *.valid CSV file

# @pytest.fixture(scope="session")
def inputfiles():
    filelist = []
    for file in glob.glob('./test/*'):
        if file[-5:] == '.json':
            filelist.append(file)
            logging.info(f'Added {file} to test list')

    return filelist

@pytest.mark.parametrize("inputfile", inputfiles())
def test_files(subtests, inputfile):
    with subtests.test(f'Testing {inputfile}'):
        outputfile = inputfile[:-5] + '.csv' 
        if os.path.basename(inputfile)[:6] == 'simple':
            logging.info(f'Processing simple file: {inputfile}')
            mrf.parse_simple(inputfile, outputfile)
        else:
            logging.info(f'Processing real file: {inputfile}')
            mrf.parse(inputfile, outputfile)

        df_test = pd.read_csv(outputfile)
        df_test.sort_values(by = list(df_test.columns), inplace=True)
        df_test.reset_index(drop=True, inplace=True)
        
        validfile = inputfile[:-5] + '.valid'
        df_valid = pd.read_csv(validfile)
        df_valid.sort_values(by = list(df_valid.columns), inplace=True)
        df_valid.reset_index(drop=True, inplace=True)

        logging.info(f'Test file: {len(df_test)}  Valid file: {len(df_test)}')
        assert df_test.equals(df_valid), f'Compare your output in {outputfile} to {validfile}'

