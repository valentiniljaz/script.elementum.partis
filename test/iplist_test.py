#!/usr/local/bin/python

# Allow imports from parent dir
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

print "======================"
print "= Testing iplist class"
print "======================"
print ""

# Imports
from iplist import iplist
import os
import pprint

fileOrig = 'resources/pack-iplist'
fileNew = 'resources/pack-iplist.new'

iplistOrig = iplist()

print "Parsing orig file ..."
rangesOrig = iplistOrig.parseFromFile(fileOrig)
print "  Orig len: " + str(len(rangesOrig))

print "Writing new file ..."
iplistOrig.writeToFile(fileNew, rangesOrig)

print "Parsing new file ..."
iplistNew = iplist()
rangesNew = iplistNew.parseFromFile(fileNew)
print "  New len: " + str(len(rangesNew))

print "Comparing ..."
found = False
for i in range(0, len(rangesOrig)):
    if rangesOrig[i]['lower'] != rangesNew[i]['lower'] or rangesOrig[i]['upper'] != rangesNew[i]['upper'] or rangesOrig[i]['desc'] != rangesNew[i]['desc']:
        print "  Found diff at: " + str(i)
        print rangesOrig[i]
        print rangesNew[i]
        found = True
if not found:
    print "  Both are the same"

domain = 'announce.partis.si'
ip = iplistOrig.getIpFromDomain(domain)
ipv6 = iplistOrig.getIpv6FromDomain(domain)
print "Find IP of " +domain+ ": " + ip + " ..."
foundOrigRange, foundOrigPos = iplistOrig.findRange(ipv6, rangesOrig)
if foundOrigRange:
    print "  Found at pos: " + str(foundOrigPos)
    print foundOrigRange
else:
    print "  Not found"

print "Remove IP of " +domain+ ": " + ip + " ..."
foundOrigRange, foundOrigPos, newRangesOrig = iplistOrig.findAndRemove(ipv6, rangesOrig)
print "  New orig len: " + str(len(newRangesOrig))

print "Find IP of " +domain+ ": " + ip + " in new ranges ..."
foundNewOrigRange, foundNewOrigPos = iplistOrig.findRange(ipv6, newRangesOrig)
if foundNewOrigRange:
    print "  Found at pos: " + str(foundNewOrigPos)
    print foundNewOrigRange
else:
    print "  Not found"

print ""
print "TEST DONE"