#!/usr/local/bin/python

# Allow imports from parent dir
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

# Imports
from Partis import Partis
import os
import pprint

# Tests
pp = pprint.PrettyPrinter()
partis = Partis(os.environ['PARTIS_USERNAME'], os.environ['PARTIS_PASSWORD'])

torrents = partis.search('black mirror', 'series')
pp.pprint(torrents)

torrents = partis.search('overboard 2018', 'movies')
pp.pprint(torrents)