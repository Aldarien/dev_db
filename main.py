import argparse, logging, json, logging.config

from aconfig import config
from src.db import db
from filters.level import LevelFilter

def main(args={}):
    logger = logging.getLogger('DevDB.main')
    logger.info('Starting to migrate {} into {}'.format(config('databases.source.name'), config('databases.destination.name')))
    logger.debug('{} and {} are set in config/databases.yml file'.format(config('databases.source.name'), config('databases.destination.name')))
    
    try:
        t = db()
        logger.info('Finished in {:.2f} seconds'.format(t))
    except Exception as e:
        logger.error(e)
    
if __name__ == '__main__':
    # Define arguments
    parser = argparse.ArgumentParser('Copy mysql databases.')
    parser.add_argument('-t', '--time', help='Show time spent.', action='store_true')
    parser.add_argument('-l', '--log', help='Log debug output to file.', action='store_true')
    args = parser.parse_args()
    
    with open("logging.json", 'r') as logging_configuration_file:
        config_dict = json.load(logging_configuration_file)

    logging.config.dictConfig(config_dict)
    
    logger = logging.getLogger('DevDB')
    if args.time:
        logger.setLevel(logging.INFO)
    if args.log:
        logger.setLevel(logging.DEBUG)
    
    logger.info('Started logging')
    
    # Run main script
    main(args)