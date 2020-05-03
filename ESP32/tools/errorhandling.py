"""
.. module:: tools.errorhandling
   :platform: Unix, Windows
   :synopsis: Contains the functions and decorators use to handle errors in runtime.

.. moduleauthor:: Pablo Crotti <pablo.crotti@outlook.com>

"""

import signal


class TimeoutException(Exception):
    def __init__(self, signum):
        self.signum = 'Signal handler called with signal: {}'.format(signum)

    def __str__(self):
        return repr(self.signum)


def timeout(s):
    """ Time out decorator. The decorator prevents a function to exceed s seconds in runtime.
    """
    def handler(signum, frame):
        raise TimeoutException(signum)
    # Beginning of the wrapper.

    def wrapper(func):
        def outer_func(*args, **kwargs):
            # Set the signal to execute the handler in case the alarm is triggered.
            signal.signal(signal.SIGALRM, handler)
            # Set the timer on the alarm for s seconds.
            signal.alarm(s)
            try:
                # Execute the outer function.
                outerfunc_output = func(*args, **kwargs)
            finally:
                # Reset the alarm to 0 (i.e., cancel the alarm).
                signal.alarm(0)
            # Return the outer function output to the system.
            return outerfunc_output
        # Return the outer function.
        return outer_func
    return wrapper
