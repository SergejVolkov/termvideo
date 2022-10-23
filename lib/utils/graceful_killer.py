import signal


class GracefulKiller:
    """
    Gracefully exit the program upon receiving a signal.

    By Mayank Jaiswal https://stackoverflow.com/a/31464349

    """
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True
