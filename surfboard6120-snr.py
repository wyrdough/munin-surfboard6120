#!/usr/bin/env python

import urllib
import re
import sys

config_text = """graph_title Cable Modem Signal to Noise Ratio
graph_vlabel dB (decibels)
graph_category network"""

if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        print config_text
        sys.exit(0)


cmOutput = urllib.urlopen("http://192.168.100.1/cmSignalData.htm").read()
cmOutput = re.sub('\n','', cmOutput)
cmOutput = re.sub('&nbsp;', '', cmOutput)
cmOutput = re.sub(r'<.*?>', '', cmOutput)

dOutput = re.search(r"Downstream(.*)Upstream", cmOutput).group(1)

snrOutput = re.search(r"Signal to Noise Ratio(.*dB).*Downstream", dOutput).group(1)

counter = 0
# Iterate over SNR Values
for current in re.finditer(r"\d+", snrOutput):
    print "snr%d.value %s" % (counter, current.group(0))
    counter = counter + 1

# Iterate over Downstream Channels
smChannels = re.search(r"Channel ID([0-9\s]+)", dOutput).group(1)
counter = 0
for current in re.finditer(r"\d+\s", smChannels):
    print "channel%d.value %s" % (counter, current.group(0))
    counter = counter + 1
