import pytest
import socket

def has_internet():
    '''Uses 8.8.8.8 to check connectivity'''
    try:
        socket.setdefaulttimeout(1)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM)\
                      .connect(('8.8.8.8',53))
        return True
    except:
        return False

needinternet=pytest.mark.skipif(not has_internet(), reason="This test needs internet")
