try:
    import logging
    import os

except BaseException:
    print('Exception got in importing the module.')


class makeLog:
    def __init__(self):
        current_dir = os.getcwd()
        if 'log_files' in os.listdir(current_dir):
            path = os.path.join(current_dir, 'log_files\\')
            file_path = path + 'logfile.log'
            logging.basicConfig(filename=file_path,
                                format='%(asctime)s %(message)s',
                                filemode='w')
        else:
            path = os.path.join(current_dir, 'log_files\\')
            os.mkdir(path)
            file_path = path + 'logfile.log'
            logging.basicConfig(filename=file_path,
                                format='%(asctime)s %(message)s',
                                filemode='w')

        self.logger = logging.getLogger()

        self.logger.setLevel(logging.DEBUG)

    def debug(self, string):
        self.logger.debug(string)

    def info(self, string):
        self.logger.info(string)

    def warning(self, string):
        self.logger.warning(string)

    def error(self, string):
        self.logger.error(string)

    def debug(self, string):
        self.logger.critical(string)
