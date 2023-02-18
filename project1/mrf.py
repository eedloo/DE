import os, logging
import time
import click
import json
import pandas as pd
import parser

__author__ = "Mohsen Eedloo"
__email__ = "Mohsen.eedloo@gmail.com"

def parse(inputfile, outputfile=None):
    return parser.parse(inputfile, outputfile)

def parse_simple(inputfile, outputfile=None):
    data = json.load(open(inputfile))
    output = []
    for item in data:
        name = item.get('name')
        type = item.get('type')
        breed = item.get('breed')
        output.append([name,type,breed])

    df = pd.DataFrame(output, columns=['name','type','breed'])
    if outputfile is not None:
        df.to_csv(outputfile, index=False)

    return df

@click.command()
@click.argument('filename', type=click.Path(exists=True, dir_okay=False))
@click.option('--loglevel', type=click.Choice(['ERROR','WARNING','INFO','DEBUG','NOTSET']), 
                            default='INFO', help='Set logging level')
def run(filename, loglevel):

    logger = logging.getLogger()
    logger.setLevel(loglevel)

    start_ts = time.perf_counter()
    logger.debug(f'Running in DEBUG')
    logger.info(f'Processing file: {filename}')

    if filename[-5:] == '.json':
        outputfile = filename[:-5] + '.csv'
        df = parse(filename,outputfile)

    runtime_sec = int(time.perf_counter() - start_ts)
    logger.info(f'Runtime: {runtime_sec} sec')

    return df

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s():%(lineno)d - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    run()