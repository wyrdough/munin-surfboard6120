#!/usr/bin/env python

import urllib
import re

cmOutput = urllib.urlopen("http://192.168.100.1/cmSignalData.htm").read()
cmOutput = re.sub('\n','', cmOutput)
cmOutput = re.sub('&nbsp;', '', cmOutput)

snrOutput = re.search(r"<TR><TD>Signal to Noise Ratio</TD>.*dB</TD></TR>", cmOutput).group(0)

for current in re.finditer(r"\d+", snrOutput):
    print current.group(0)
