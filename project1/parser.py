import pandas as pd
import json

# File open
def file_open(path):
    with open(path) as f:
        data = json.load(f)
    return data

# Extracting information of Provider Groups ID
# Building a dictionary of each Provider Group ID with npis
# The function output a dictionary with keys as Provider Group IDs and values as npis
# Later we can lookup npis in the dictionary based on Provider Group IDs
def pgid(data):
    n_groups = len(data['provider_references'])
    npi_dic = {}
    for i in range(n_groups):
        keys = data['provider_references'][i]['provider_group_id']
        values = []
        npi = data['provider_references'][i]['provider_groups']
        for j in range(len(npi)):
            for k in range(len(npi[j]['npi'])):
                values.append(npi[j]['npi'][k])
        npi_dic[keys] = values
    return npi_dic

# Extracting information of in_network attribute
# The function look for same "Provider_references" in "in_network" attribute based on npis dictionary
# It finds "provider_references"'s information and returns a list of wanted info
def inn(data, npis):
    pgs = list(npis.keys())
    output = []
    for p in range(len(pgs)):
        for i in range(len(data['in_network'])):
            if data['in_network'][i].get('negotiated_rates') != None:
                for j in range(len(data['in_network'][i]['negotiated_rates'])):
                    if pgs[p] == data['in_network'][i]['negotiated_rates'][j]['provider_references'][0]:
                        n_type = data['in_network'][i]['negotiated_rates'][j]['negotiated_prices'][0]['negotiated_type']
                        n_rate = data['in_network'][i]['negotiated_rates'][j]['negotiated_prices'][0]['negotiated_rate']
                        s_code = data['in_network'][i]['negotiated_rates'][j]['negotiated_prices'][0]['service_code']
                        b_class = data['in_network'][i]['negotiated_rates'][j]['negotiated_prices'][0]['billing_class']
                        n_arrangement = data['in_network'][i]['negotiation_arrangement']
                        bc_type = data['in_network'][i]['billing_code_type']
                        b_code = data['in_network'][i]['billing_code']
                        if data['in_network'][i]['negotiated_rates'][j]['negotiated_prices'][0].get('billing_code_modifier') != None:
                            bc_modifier = data['in_network'][i]['negotiated_rates'][j]['negotiated_prices'][0].get('billing_code_modifier')
                        else:
                            bc_modifier = ''
                        output.append([
                            data['reporting_entity_name'],
                            pgs[p],
                            n_arrangement,
                            bc_type,
                            b_code,
                            bc_modifier,
                            n_type,
                            b_class,
                            s_code,
                            n_rate])
    return output

# Attach the list of npis of each provider group to it
def attach(output, npis):
    for key in npis:
        npi = npis[key]
        for i in output:
            if i[1] == key:
                i.insert(1, npi)
    return output

# Building dataframe with output data
def make_df(output):
    pd.set_option('display.precision', 10)
    df = pd.DataFrame(
        columns=[
            'payer', 'npi', 'provider_group_id', 'negotiated_arrangement', 
            'code_type', 'code', 'modifier', 'negotiated_type', 
            'billing_class', 'place_of_service_code', 'rate'
            ],
        data = output)
    return df

# The refine function unnest lists in the dataframe, set index, and drop provider_group_id column as it is not needed in output
def refine(df):
    df = df.explode('modifier').explode('place_of_service_code').explode('npi').set_index('payer')
    df = df.drop('provider_group_id', axis=1)
    return df

# The result function output the refined dataframe as a "csv" file
def result(df, name_of_file):
    return df.to_csv(name_of_file)

def parse(filename, output_file):
    data = file_open(filename)
    npis = pgid(data)
    output = attach(inn(data, npis), npis)
    df = refine(make_df(output))
    result(df, output_file)