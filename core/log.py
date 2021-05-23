import coloredlogs, logging


class Log:
    """
    Log class
    Custom log for PaperBoy
    """
    msg: str = None
    logger: any = None

    def __init__(self, msg):
        self.msg = msg
        self.logger = logging.getLogger('PaperBoy')
        coloredlogs.install(level='DEBUG', logger=self.logger)

    def info(self):
        self.logger.info(self.msg)

    def warn(self):
        self.logger.warning(self.msg)

    def error(self):
        self.logger.error(self.msg)
