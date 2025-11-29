from enum import Enum


class LogLevel(Enum):
    """Enumeration of the available logging levels.

    The logging level determines the verbosity of the log output. More critical
    levels include messages from less critical ones.

    Attributes
    ----------
    VERBOSE : int
        The most verbose logging level, including all messages.
    DEBUG : int
        Includes debug messages and all more critical levels.
    INFO : int
        Includes informational messages and all more critical levels.
    WARNING : int
        Includes warnings and errors.
    ERROR : int
        Includes only error messages.
    """
    VERBOSE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
