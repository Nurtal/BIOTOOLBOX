"""
Trash file,
place for work in progress
and crazy ideas
"""


### IDEAS
## => reformat file
## => replace whitespace by underscore in file_name

import shutil
import subprocess


def detect_file_format(data_file_name):
	"""
	Because in biology, you always need to check
	if a csv file is a real csv file ...
	
	-> Should return the separator used in
	data file.
	"""

	## A few parameters
	can_analyse_file = False
	separator_list = [",", ";", "\t"]
	separator_to_count = {}
	best_separator = "undef"

	## Count the Number of line in the file
	data_file = open(str(data_file_name), "r")
	cmpt_line = 0
	for line in data_file:
		line = line.split("\n")
		line = line[0]
		cmpt_line += 1
	data_file.close()

	## Test if we can do something with it
	if(cmpt_line > 1):
		can_analyse_file = True

	## Run the analysis if we can
	if(can_analyse_file):
		

		## Initialize the separator_to_count variable:
		for separator in separator_list:
			separator_to_count[separator] = []

		## Re-open the file and parse the lines
		data_file = open(str(data_file_name), "r")
		for line in data_file:
			line = line.split("\n")
			line = line[0]

			## Split line with a few separator
			for separator in separator_list:
				line_in_array = line.split(separator)
				separator_to_count[separator].append(len(line_in_array))


		data_file.close()

		## Perform the analysis
		for separator in separator_to_count.keys():

			## Separate data and header size
			## Because biologists ... well, you know why.
			header_size = separator_to_count[separator][0]
			data_size = separator_to_count[separator][1:]

			max_size = max(data_size)
			min_size = min(data_size)

			## Perform the test
			if(max_size != 1 and max_size == min_size):
				 best_separator = separator

		## return the best separator found
		return best_separator


	## Exit The programm with a warning message
	else:
		print "[!] Less than 2 lines in the file"+str(data_file_name)+", can't run an analysis\n"
		return best_separator




def change_file_format(data_file_name, separator):
	"""
	-> Change the separator used in data_file_name, to separator
	=> TODO:
		- deal with extension in the output file name
	[IN PROGRESS]
	"""

	## Get current separator
	current_separator = detect_file_format(data_file_name)
	if(current_separator != "undef"):
		
		## Re-write file with new separator
		output_file_name = data_file_name.split(".")
		output_file_name = output_file_name[0]
		output_file_name = str(output_file_name)+"_reformated.tmp"

		input_data_file = open(data_file_name, "r")
		output_data_file = open(output_file_name, "w")
		for line in input_data_file:
			line_to_write = line.replace(current_separator, separator)
			output_data_file.write(line_to_write)
		output_data_file.close()
		input_data_file.close()

		# Exit The programm with a validation message
		print "[*] File "+str(data_file_name)+" have been formated, from "+str(current_separator)+ " To "+str(separator)+" separator\n"

	## Exit The programm with a warning message
	else:
		print "[!] Can't determine the separator used in "+str(data_file_name)+", can't reformat file\n"




def fix_file_name(input_file_name):
	"""
	-> for all the spaces and dots in 
	   the wild biology file name ...

	IN PROGRESS
	"""

	## Make sure the file exist

	## Scan for multiple dots in file name
	input_file_name_in_array = input_file_name.split(".")
	output_file_name = ""
	if(len(input_file_name_in_array) > 2):
		
		## Deal with multiple dots in file name
		for element in input_file_name:
			output_file_name += str(element)+"_"
		output_file_name = output_file_name[:-1]

		## get file extension
		file_extension = input_file_name.split(".")
		file_extension = file_extension[-1]

		output_file_name += "."+str(extension)

		## replace spaces and dots by underscores
		output_file_name = input_file_name.replace(" ", "_")

	elif(len(input_file_name_in_array) == 2):
		output_file_name = input_file_name_in_array[0]
	else:
		print "[!] It appears that the input file have no extensions ... "

	## get file extension
	file_extension = input_file_name.split(".")
	file_extension = file_extension[-1]

	






### TEST SPACE ###
#sep = detect_file_format("play.txt")
#print sep
#change_file_format("play.txt", ";")
fix_file_name("play.csv.old.csv")