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

from jinja2   import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from pathlib  import Path

plot_subdir = sys.argv[2]
output_dir = sys.argv[1]
Path(output_dir).mkdir(parents=True, exist_ok=True)

env = Environment(
    loader=FileSystemLoader(searchpath="templates"),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('index.html')

plot_groups = [
            {"name": "RFCs",
             "subtitle": "Annual publications",
             "plots" : [{"name": "All publications", "path": "%s/rfc-annual-publications.png" % (plot_subdir), "shortname": "rfc-annual-pub"},
                        {"name": "By status", "path": "%s/rfc-annual-publications-status.png" % (plot_subdir), "shortname": "rfc-annual-pub-status"},
                        {"name": "By stream", "path": "%s/rfc-annual-publications-streams.png" % (plot_subdir), "shortname": "rfc-annual-pub-streams"},
                        {"name": "By area", "path": "%s/rfc-annual-publications-areas.png" % (plot_subdir), "shortname": "rfc-annual-pub-areas"},
                        {"name": "By month", "path": "%s/rfc-monthly-publications.png" % (plot_subdir), "shortname": "rfc-monthly-publications"},
                       ]
            },
            {"name": "RFCs",
             "subtitle": "Annual publications, normalised",
             "plots" : [{"name": "By status, normalised", "path": "%s/rfc-annual-publications-status-norm.png" % (plot_subdir), "shortname": "rfc-annual-pub-status-normalised"},
                        {"name": "By stream, normalised", "path": "%s/rfc-annual-publications-streams-norm.png" % (plot_subdir), "shortname": "rfc-annual-pub-streams-normalised"},
                        {"name": "By area, normalised", "path": "%s/rfc-annual-publications-areas-norm.png" % (plot_subdir), "shortname": "rfc-annual-pub-areas-normalised"},
                        {"name": "By month, normalised", "path": "%s/rfc-monthly-publications-norm.png" % (plot_subdir), "shortname": "rfc-monthly-publications-normalised"},
                       ]
            }
        ]

with open('%s/index.html' % (output_dir), 'w') as indexHtmlFile:
    indexHtmlFile.write(template.render(generation_ts=datetime.now(), plot_groups=plot_groups))
