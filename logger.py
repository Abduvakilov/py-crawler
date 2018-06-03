import os
import logging 

import __main__
main_name = __main__.__file__.split('/')[-1].replace('.py', '')

dir_path = os.path.dirname(os.path.realpath(__file__))
LOGGING_DIR = 'logs/'


if 'LOG' in os.environ:
    LOGGING_DIR = os.environ['LOG']
class Logger(object):

    def __init__(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            file_name = os.path.join(dir_path, LOGGING_DIR, '{}.log'.format(main_name))
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            if 'nostream' not in os.environ:
                stream_handler = logging.StreamHandler()
                logger.addHandler(stream_handler)
        self._logger = logger

    def get(self):
        return self._logger