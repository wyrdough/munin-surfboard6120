#!/usr/bin/env python

import urllib
import re
import sys

def print_config_snr(channel_output):
    config_text = """graph_title SB6120 Signal to Noise (dB)
graph_vlabel dB (decibels)
graph_category network
%s""" % channel_output
    print config_text

def print_config_pwr(channel_output):
    config_text = """graph_title SB6120 Power Level (dBmV)
graph_vlabel dBmV
graph_category network
%s""" % channel_output
    print config_text

if re.match(r".*_pwr.py$", sys.argv[0]):
    graph_type = "pwr"
else:
    graph_type = "snr"

snr_output = ""
pwr_output = ""
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
downstreamPwrOutput = re.search(r"new reading (.*dBmV).* $", dOutput).group(1)
upstreamSnrOutput = re.search(r"Power Level.*Upstream Modulation", uOutput).group(0)

counter = 0
# Iterate over DOWNSTREAM SNR Values
for current in re.finditer(r"\d+", downstreamSnrOutput):
    snr_output = snr_output + "downstreamsnr%d.value %s\n" % (counter, current.group(0))
    counter = counter + 1

# Iterate over DOWNSTREAM power Values
counter = 0
for current in re.finditer(r"\d+", downstreamPwrOutput):
    pwr_output = pwr_output + "downstreampwr%d.value %s\n" % (counter, current.group(0))
    counter = counter + 1

# Iterate over UPSTREAM power Values
counter = 0
for current in re.finditer(r"\d+", upstreamSnrOutput):
    pwr_output = pwr_output + "upstreampwr%d.value %s\n" % (counter, current.group(0))
    counter = counter + 1

# Iterate over Downstream Channels
smChannels = re.search(r"Channel ID([0-9\s]+)", dOutput).group(1)
counter = 0
for current in re.finditer(r"\d+\s", smChannels):
    channel_output = channel_output + "downstream%s%d.label Downstream Channel %s\n" % (graph_type, counter, current.group(0))
    counter = counter + 1

# Iterate over Upstream Channels
smChannels = re.search(r"Channel ID([0-9\s]+)", uOutput).group(1)
counter = 0
for current in re.finditer(r"\d+\s", smChannels):
    if graph_type == "pwr":
        channel_output = channel_output + "upstream%s%d.label Upstream Channel %s\n" % (graph_type, counter, current.group(0))
        counter = counter + 1

print '"' + sys.argv[0] + '"'

if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        if graph_type == "pwr":
            print_config_pwr(channel_output)
        else:
            print_config_snr(channel_output)

        sys.exit(0)

if graph_type == "pwr":
    print pwr_output
else:
    print snr_output

sys.exit(0)

