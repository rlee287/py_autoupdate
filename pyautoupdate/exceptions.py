class PyautoupdateBaseException(Exception):
    """Base exception for all pyautoupdate errors"""

class ProcessRunningException(PyautoupdateBaseException):
    """Exception when process is already running"""
