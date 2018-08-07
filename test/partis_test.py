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

print "======================"
print "= Testing Partis class"
print "======================"
print ""

# Tests
pp = pprint.PrettyPrinter()
partis = Partis(os.environ['PARTIS_USERNAME'], os.environ['PARTIS_PASSWORD'])

test = "Overboard 2018"
print "Test for movie: " +test+ " ..."
torrents = partis.search(test, 'movies')
pp.pprint(torrents)
print ""

test = "Friends Season 9"
print "Test for series: " +test+ " ..."
torrents = partis.search(test, 'series')
pp.pprint(torrents)
print ""

test = "The Big Bang Theory S10E01"
print "Test for series: " +test+ " ..."
torrents = partis.search(test, 'series')
pp.pprint(torrents)
print ""

print ""
print "TEST DONE"