from cStringIO import StringIO
import sys
from StringIO import StringIO

class Capturing(StringIO):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self
        return self
    def __exit__(self, *args):
        sys.stdout = self._stdout


def run_python(code):
    with Capturing() as output:
        try:
            exec (code, globals())
            return output.getvalue()
        except SystemExit:
            pass
    
