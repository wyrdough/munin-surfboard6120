#!/usr/bin/env python

import urllib
import re
import sys

def print_config(channel_output):
    config_text = """graph_title SB6120 Signal to Noise (dB)
graph_vlabel dB (decibels)
graph_category network
%s""" % channel_output
    print config_text

snr_output = ""
channel_output = ""
cmOutput = urllib.urlopen("http://192.168.100.1/cmSignalData.htm").read()

# Pull apart and put back together the ugly HTML output from the SB6120
cmOutput = re.sub('\n','', cmOutput)
cmOutput = re.sub('&nbsp;', '', cmOutput)
cmOutput = re.sub(r'<.*?>', '', cmOutput)
cmOutput = " ".join(cmOutput.split())

dOutput = re.search(r"(Downstream.*)(Upstream Bonding Channel.*)", cmOutput).group(1)
uOutput = re.search(r"(Downstream.*)(Upstream Bonding Channel.*)", cmOutput).group(2)

downstreamSnrOutput = re.search(r"Signal to Noise Ratio(.*dB).*Downstream", dOutput).group(1)
upstreamSnrOutput = re.search(r"Power Level.*Upstream Modulation", uOutput).group(0)

counter = 0
# Iterate over DOWNSTREAM SNR Values
for current in re.finditer(r"\d+", downstreamSnrOutput):
    snr_output = snr_output + "downstreamsnr%d.value %s\n" % (counter, current.group(0))
    counter = counter + 1

# Iterate over UPSTREAM SNR Values
counter = 0
for current in re.finditer(r"\d+", upstreamSnrOutput):
    snr_output = snr_output + "upstreamsnr%d.value %s\n" % (counter, current.group(0))
    counter = counter + 1

# Iterate over Downstream Channels
smChannels = re.search(r"Channel ID([0-9\s]+)", dOutput).group(1)
counter = 0
for current in re.finditer(r"\d+\s", smChannels):
    channel_output = channel_output + "downstreamsnr%d.label Downstream Channel %s\n" % (counter, current.group(0))
    counter = counter + 1

# Iterate over Upstream Channels
smChannels = re.search(r"Channel ID([0-9\s]+)", uOutput).group(1)
counter = 0
for current in re.finditer(r"\d+\s", smChannels):
    channel_output = channel_output + "upstreamsnr%d.label Upstream Channel %s\n" % (counter, current.group(0))
    counter = counter + 1

if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        print_config(channel_output)
        sys.exit(0)

print snr_output
sys.exit(0)
