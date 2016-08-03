class pyautoupdateBaseException(Exception):
    """Base exception for all pyautoupdate errors"""

class ProcessRunningException(pyautoupdateBaseException):
    """Exception when process is already running"""
