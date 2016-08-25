import sys
from task import *

# python task.py loop
if len(sys.argv) > 1 and sys.argv[1] == "loop":
    print "starting task loop"
    monitor_infinite()
else:
    monitor_once()
