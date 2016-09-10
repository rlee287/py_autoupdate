class PyautoupdateBaseException(Exception):
    """Base exception for all pyautoupdate errors"""


class PyautoupdateBaseWarning(Warning):
    """Base warning for all pyautoupdate errors"""


class ProcessRunningException(PyautoupdateBaseException):
    """Exception when process is already running"""


class CorruptedFileWarning(PyautoupdateBaseWarning):
    """Warning that critical files are corrupted"""
