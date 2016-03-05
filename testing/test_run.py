from __future__ import absolute_import

from ..launcher import Launcher

class TestRunProgram:
    def test_run(self):
        l = Launcher("")
        l.run()
