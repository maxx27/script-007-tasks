#!/usr/bin/env python3
import logging
import logging.config
import sys

import server.FileService as FileService
import utils.Config


def setup_logger(level='NOTSET', filename=None):
    logger_conf = {
        'version': 1,
        'formatters': {
            'default': {
                'format':
                    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': level,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
    if filename:
        logger_conf['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'encoding': 'UTF-8',
            'formatter': 'default',
            'filename': filename,
        }
        logger_conf['root']['handlers'].append('file')
    logging.config.dictConfig(logger_conf)


def main():
    logging.debug('started')
    logging.debug('config %s', utils.Config.data.to_dict())

    FileService.change_dir(utils.Config.data.dir)


if __name__ == '__main__':
    try:
        utils.Config.gather()
        setup_logger(level=logging.getLevelName(utils.Config.data.log.level.upper()),
                     filename=utils.Config.data.log.file)
        main()
    except SystemExit:
        # argparse throws it (even in `-h`)
        sys.exit(1)
    except KeyboardInterrupt:
        print(f'\nERROR: Interrupted by user', file=sys.stderr)
        sys.exit(1)
    except BaseException as err:
        print(f'ERROR: Something goes wrong:\n{str(err)}', file=sys.stderr)
        sys.exit(1)
