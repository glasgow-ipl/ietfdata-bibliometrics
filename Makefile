# =================================================================================================
# ietfdata-bibliometrics
#
# Copyright (C) 2020 University of Glasgow
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
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

# Output directory and subdirectories
OUTPUT_DIR = output
OUTPUT_SUBDIR_PLOTS = plots
OUTPUT_SUBDIR_DATA =  data

DATA_FILES = rfc-annual-publications.csv \
	         rfc-annual-publications-streams.csv \
	         rfc-annual-publications-areas.csv \
	         rfc-annual-publications-status.csv \
			 rfc-monthly-publications.csv \

DATA = $(DATA_FILES:%=$(OUTPUT_DIR)/$(OUTPUT_SUBDIR_DATA)/%)

PLOT_FILES = rfc-annual-publications.png \
	         rfc-annual-publications-streams.png \
	         rfc-annual-publications-areas.png \
	         rfc-annual-publications-status.png \
			 rfc-annual-publications-areas-norm.png \
			 rfc-monthly-publications.png \
			 rfc-monthly-publications-norm.png \
			 rfc-annual-publications-streams-norm.png \
			 rfc-annual-publications-status-norm.png \

PLOTS = $(PLOT_FILES:%=$(OUTPUT_DIR)/$(OUTPUT_SUBDIR_PLOTS)/%)

HTML = $(OUTPUT_DIR)/index.html

all: $(DATA) $(PLOTS) $(HTML)

# =================================================================================================
# Generate data

$(OUTPUT_DIR)/$(OUTPUT_SUBDIR_DATA)/rfc-%.csv: bin/fetch-rfc-metrics.py
	pipenv run python bin/fetch-rfc-metrics.py $(OUTPUT_DIR)/$(OUTPUT_SUBDIR_DATA)

# =================================================================================================
# Generate plots

$(OUTPUT_DIR)/$(OUTPUT_SUBDIR_PLOTS)/rfc-%.png: $(DATA) bin/plot-rfc-metrics.py
	pipenv run python bin/plot-rfc-metrics.py $(OUTPUT_DIR)/$(OUTPUT_SUBDIR_PLOTS) $(OUTPUT_DIR)/$(OUTPUT_SUBDIR_DATA)

# =================================================================================================
# Generate HTML

$(OUTPUT_DIR)/%.html: bin/generate-html-output.py templates/index.html $(PLOTS)
	cp templates/bootstrap.min.css $(OUTPUT_DIR)/bootstrap.min.css
	cp templates/bootstrap.min.js  $(OUTPUT_DIR)/bootstrap.min.js
	cp templates/jquery.min.js     $(OUTPUT_DIR)/jquery.min.js
	pipenv run python bin/generate-html-output.py $(OUTPUT_DIR) $(OUTPUT_SUBDIR_PLOTS)

# =================================================================================================
# Clean

clean:
	rm -rf $(OUTPUT_DIR)
