import pywemo
import os, sys, time
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython
from gevent.pywsgi import WSGIServer
import re
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import subprocess
subprocess.run("wemo switch Light off")

ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')

print("Current environment directory:" + sys.prefix)
print("System version: "+sys.version)
print("Current working directory: "+os.getcwd())

#devices = pywemo.discover_devices()
#print(devices)


