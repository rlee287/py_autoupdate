import socket
import pytest

def has_internet():
    '''Uses 8.8.8.8 to check connectivity'''
    try:
        socket.setdefaulttimeout(1)
        test_connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_connection.connect(('8.8.8.8',53))
        test_connection.close()
        return True
    except OSError:
        return False

needinternet=pytest.mark.skipif(not has_internet(), reason="This test needs internet")
