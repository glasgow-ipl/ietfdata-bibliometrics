# Copyright (C) 2017-2020 University of Glasgow
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import matplotlib.pyplot as plt

from pathlib  import Path

input_dir = sys.argv[2]
output_dir = sys.argv[1]
Path(output_dir).mkdir(parents=True, exist_ok=True)

annual_pub_data = {}

def plot_stack(x, y, ylim_top, labels, output_filename):
    plt.figure(figsize=(15,4))
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    ax.grid(True, linewidth=0.5, color='grey', linestyle="dashed")
    plt.xticks(rotation=90)
    plt.xlabel("Publication Year")
    plt.ylabel("Publication Count")
    plt.ylim(top=ylim_top)
    bars = []
    bottom = [0]*len(y[0])
    for i in range(len(y)):
        bars.append(plt.bar(x, y[i], bottom=bottom))
        bottom = [a + b for a, b in zip(bottom, y[i])]
    #if labels is not None:
    #    plt.stackplot(x, y, labels=labels)
    #    fig.legend(ncol=len(labels))
    #else:
    #    plt.stackplot(x, y)
    if labels is not None:
        ax.legend([bar[0] for bar in bars], labels, ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.10))
    ax.yaxis.set_ticks_position('both')
    fig.set_size_inches(12, 8)
    fig.savefig(output_filename, bbox_inches='tight')

with open("%s/rfc-annual-publications.csv" % (input_dir), "r") as annualRfcDataFile:
    for annualData in annualRfcDataFile:
        year, count = annualData[:-1].split(',')
        annual_pub_data[year] = int(count)

x = sorted(list(annual_pub_data.keys()))
y = [[annual_pub_data[year] for year in x]]

plt.figure(figsize=(15,4))
fig, ax = plt.subplots()
ax.set_axisbelow(True)
ax.grid(True, linewidth=0.5, color='grey', linestyle="dashed")
plt.xticks(rotation=90)
plt.xlabel("Publication Year")
plt.ylabel("Publication Count")
plt.stackplot(x, y)
ax.yaxis.set_ticks_position('both')
fig.set_size_inches(12, 8)
fig.savefig('%s/rfc-annual-publications.png' % (output_dir), bbox_inches='tight')

plot_stack(x, y, 550, None, '%s/rfc-annual-publications.png' % (output_dir))

annual_pub_data_streams = {}
streams = []

with open("%s/rfc-annual-publications-streams.csv" % (input_dir), "r") as annualRfcStreamsDataFile:
    for annualData in annualRfcStreamsDataFile:
        year, stream, count = annualData[:-1].split(',')
        if year not in annual_pub_data_streams:
            annual_pub_data_streams[year] = {}
        if stream not in streams:
            streams.append(stream)
        annual_pub_data_streams[year][stream] = int(count)

x = sorted(list(annual_pub_data_streams.keys()))
y = [[annual_pub_data_streams[year][stream] for year in x] for stream in streams]

plot_stack(x, y, 550, streams, '%s/rfc-annual-publications-streams.png' % (output_dir))

annual_pub_data_areas = {}
areas = []

with open("%s/rfc-annual-publications-areas.csv" % (input_dir), "r") as annualRfcAreasDataFile:
    for annualData in annualRfcAreasDataFile:
        year, area, count = annualData[:-1].split(',')
        if year not in annual_pub_data_areas:
            annual_pub_data_areas[year] = {}
        if area not in areas:
            areas.append(area)
        annual_pub_data_areas[year][area] = int(count)

x = sorted(list(annual_pub_data_areas.keys()))
y = [[annual_pub_data_areas[year][area] for year in x] for area in areas]

plot_stack(x, y, 550, areas, '%s/rfc-annual-publications-areas.png' % (output_dir))

annual_pub_data_status = {}
statuses = []

with open("%s/rfc-annual-publications-status.csv" % (input_dir), "r") as annualRfcStatusDataFile:
    for annualData in annualRfcStatusDataFile:
        year, status, count = annualData[:-1].split(',')
        if year not in annual_pub_data_status:
            annual_pub_data_status[year] = {}
        if status not in statuses:
            statuses.append(status)
        annual_pub_data_status[year][status] = int(count)

x = sorted(list(annual_pub_data_status.keys()))
y = [[annual_pub_data_status[year][status] for year in x] for status in statuses]

plot_stack(x, y, 550, statuses, '%s/rfc-annual-publications-status.png' % (output_dir))
