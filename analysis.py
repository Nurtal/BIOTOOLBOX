"""
ANALYSIS STUFF
"""

import os
import shutil

def run_afd(input_data):
	"""
	IN PROGRESS
	"""

	## Prepare the file for R script
	shutil.copy(input_data, "input/data.csv")

	## Run the R script
	os.system("Rscript scripts/afd.R > trash.txt")





## TEST SPACE
run_afd("input_test2.csv")