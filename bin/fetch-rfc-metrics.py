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

from pathlib  import Path
from ietfdata import rfcindex

def yearly_pub_data(monthly_data, output_filename):
    with open(output_filename, "w") as output_file:
        for year in sorted(list(monthly_data.keys())):
            annual_count = 0
            for month in monthly_data[year]:
                annual_count += monthly_data[year][month]["pubs"]
            output_file.write("%d,%d\n" % (year, annual_count))

def yearly_pub_data_streams(monthly_data, output_filename):
    annual_counts = {}
    streams = []
    for year in sorted(list(monthly_data.keys())):
        for month in monthly_data[year]:
            if year not in annual_counts:
                annual_counts[year] = {}
            for stream in monthly_data[year][month]["stream"]:
                if stream not in streams:
                    streams.append(stream)
                if stream not in annual_counts[year]:
                    annual_counts[year][stream] = 0
                annual_counts[year][stream] += monthly_data[year][month]["stream"][stream]
    with open(output_filename, "w") as output_file:
        for year in annual_counts:
            for stream in streams:
                output_file.write("%d,%s,%d\n" % (year, stream, annual_counts[year].get(stream, 0)))

def yearly_pub_data_areas(monthly_data, output_filename):
    annual_counts = {}
    areas = []
    for year in sorted(list(monthly_data.keys())):
        for month in monthly_data[year]:
            if year not in annual_counts:
                annual_counts[year] = {}
            for area in monthly_data[year][month]["area"]:
                if area not in areas:
                    areas.append(area)
                if area not in annual_counts[year]:
                    annual_counts[year][area] = 0
                annual_counts[year][area] += monthly_data[year][month]["area"][area]
    with open(output_filename, "w") as output_file:
        for year in annual_counts:
            for area in areas:
                output_file.write("%d,%s,%d\n" % (year, area, annual_counts[year].get(area, 0)))

def yearly_pub_data_pubstatus(monthly_data, output_filename):
    annual_counts = {}
    statuses = []
    for year in sorted(list(monthly_data.keys())):
        for month in monthly_data[year]:
            if year not in annual_counts:
                annual_counts[year] = {}
            for status in monthly_data[year][month]["publ_status"]:
                if status not in statuses:
                    statuses.append(status)
                if status not in annual_counts[year]:
                    annual_counts[year][status] = 0
                annual_counts[year][status] += monthly_data[year][month]["publ_status"][status]
    with open(output_filename, "w") as output_file:
        for year in annual_counts:
            for status in statuses:
                output_file.write("%d,%s,%d\n" % (year, status, annual_counts[year].get(status, 0)))

def monthly_pub_data(monthly_data, output_filename):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    with open(output_filename, "w") as output_file:
        for year in sorted(list(monthly_data.keys())):
            annual_count = 0
            for month in months:
                output_file.write("%d,%s,%d\n" % (year, month, monthly_data[year].get(month, {"pubs": 0})["pubs"]))

def main():
    ri = rfcindex.RFCIndex()
    rfcs = ri.rfcs()

    monthly_data = {}

    output_dir = sys.argv[1]
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for rfc in rfcs:
        if rfc.year not in monthly_data:
            monthly_data[rfc.year] = {}
        if rfc.month not in monthly_data[rfc.year]:
            monthly_data[rfc.year][rfc.month] = {"pubs": 0, "stream": {}, "wg": {}, "area": {}, "publ_status": {}, "curr_status": {}}
        monthly_data[rfc.year][rfc.month]["pubs"] += 1
        monthly_data[rfc.year][rfc.month]["stream"][rfc.stream] = monthly_data[rfc.year][rfc.month]["stream"].get(rfc.stream, 0) + 1
        monthly_data[rfc.year][rfc.month]["wg"][rfc.wg] = monthly_data[rfc.year][rfc.month]["wg"].get(rfc.wg, 0) + 1
        monthly_data[rfc.year][rfc.month]["area"][rfc.area] = monthly_data[rfc.year][rfc.month]["area"].get(rfc.area, 0) + 1
        monthly_data[rfc.year][rfc.month]["publ_status"][rfc.publ_status] = monthly_data[rfc.year][rfc.month]["publ_status"].get(rfc.publ_status, 0) + 1

    yearly_pub_data(monthly_data, "%s/rfc-annual-publications.csv" % (output_dir))
    yearly_pub_data_streams(monthly_data, "%s/rfc-annual-publications-streams.csv" % (output_dir))
    yearly_pub_data_areas(monthly_data, "%s/rfc-annual-publications-areas.csv" % (output_dir))
    yearly_pub_data_pubstatus(monthly_data, "%s/rfc-annual-publications-status.csv" % (output_dir))
    monthly_pub_data(monthly_data, "%s/rfc-monthly-publications.csv" % (output_dir))

if __name__ == "__main__":
    main()
