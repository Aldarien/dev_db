import argparse, logging

from aconfig import config
from src.db import db

def main(args={}):
    if args.time:
        print('Starting to migrate ' + config('databases.source.name') + ' into ' + config('databases.destination.name'))
    t = db()
    if args.time:
        print('Finished in {:.2f} seconds'.format(t))
    if args.log:
        file = 'devdb.log'
        if 'log-file' in args:
            file = args.log-file
        logger = logging.getLogger('DevDB')
        hdlr = logging.FileHandler(file)
        formatter = logging.Formatter('[%(asctime)s] %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)
        logger.info('Starting to migrate {} into {}'.format(config('databases.source.name'), config('databases.destination.name')))
        logger.info('Finished in {:.2f} seconds'.format(t))
    
if __name__ == '__main__':
    # Define arguments
    parser = argparse.ArgumentParser('Copy mysql databases.')
    parser.add_argument('-t', '--time', help='Show time spent.', action='store_true')
    parser.add_argument('-l', '--log', help='Log output to file.', action='store_true')
    parser.add_argument('-f', '--log-file', help='Set log file. Default: devdb.log')
    args = parser.parse_args()
    
    # Run main script
    main(args)