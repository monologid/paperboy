from core.log import Log
import signal


class Graceful:
    """
    Graceful class
    For handling graceful shutdown
    """

    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        Log('Shutting down, see you next time! :)').info()
        self.kill_now = True
