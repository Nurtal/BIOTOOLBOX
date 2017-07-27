"""
Trash file,
place for work in progress
and crazy ideas
"""


### IDEAS
## => reformat file
## => replace whitespace by underscore in file_name [DONE]
## => Check and install needed python modules & R packages


import shutil
import subprocess
import os.path
import platform
import os
import glob


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
	-> Delete spaces in lines if space is not the separator 
	"""

	## Define the extension
	extension = "_reformated.tmp"
	if(separator == ","):
		extension = "_reformated.csv"
	elif(separator == "\t"):
		extension = "_reformated.tsv"

	## Get current separator
	current_separator = detect_file_format(data_file_name)
	if(current_separator != "undef"):
		
		## Re-write file with new separator
		output_file_name = data_file_name.split(".")
		output_file_name = output_file_name[0]
		output_file_name = str(output_file_name)+extension
		input_data_file = open(data_file_name, "r")
		output_data_file = open(output_file_name, "w")
		for line in input_data_file:
			line_to_write = line.replace(current_separator, separator)
			if(separator != " "):
				line_to_write = line_to_write.replace(" ", "")
			output_data_file.write(line_to_write)
		output_data_file.close()
		input_data_file.close()

		# Exit The programm with a validation message
		print "[*] File "+str(data_file_name)+" have been formated, from "+str(current_separator)+ " To "+str(separator)+" separator\n"

	## Exit The programm with a warning message
	else:
		print "[!] Can't determine the separator used in "+str(data_file_name)+", can't reformat file\n"




def fix_file_name(input_file):
	"""
	-> for all the spaces and dots in
	   the wild biology file name ...
	-> Deal with path on Windows and Linux, treat onlu the file name
	-> convert dots and spaces in file
	-> copy the input_file with to a file with a valid file name
	"""

	## Make sure the file exist
	if(os.path.exists(input_file)):

		## Separate file name from file path
		input_file_path = ""
		folder_separator = "/"
		if(platform.system() == "Windows"):
			folder_separator = "\\"
		elif(platform.system == "Linux"):
			folder_separator = "/"
		
		input_file_name_path_in_array = input_file.split(folder_separator)
		input_file_name = input_file_name_path_in_array[-1]

		if(len(input_file_name_path_in_array) > 1):
			for folder in input_file_name_path_in_array[:-1]:
				input_file_path += str(folder) + folder_separator

		## Scan for multiple dots in file name
		input_file_name_in_array = input_file_name.split(".")
		output_file_name = ""
		if(len(input_file_name_in_array) > 2):
			
			## Deal with multiple dots in file name
			for element in input_file_name_in_array[:-1]:
				output_file_name += str(element)+"_"
			output_file_name = output_file_name[:-1]

			## get file extension
			file_extension = input_file_name_in_array[-1]

			## replace spaces and dots by underscores
			output_file_name = output_file_name.replace(" ", "_")
			output_file_name = output_file_name.replace(".", "_")

			## init output filename
			output_file_name += "."+str(file_extension)

		elif(len(input_file_name_in_array) == 2):

			## get file extension
			file_extension = input_file_name_in_array[-1]
			
			## init output filename
			output_file_name = input_file_name_in_array[0]
			output_file_name += "."+str(file_extension)

			## replace spaces and dots by underscores
			output_file_name = output_file_name.replace(" ", "_")

		else:
			print "[!] It appears that the input file have no extensions ... "

		## Finalise output file name
		output_file_name = str(input_file_path) + str(output_file_name)
		
		## Check if input file is a valid file name
		## if not copy make a copy of the file with a valid file name.
		if(str(output_file_name) == str(input_file)):
			print "[*] "+str(input_file) +" appears to be a valid file name"
		else:
			print "[*] Create a copy of "+str(input_file) +" \n[~] with the name: "+str(output_file_name)
			shutil.copy(input_file, output_file_name)
	else:
		print "[!] Can't find file "+str(input_file)
		

def clean():
	"""
	IN PROGRESS
	"""

	## Clean images
	images_files = glob.glob("output/images/*.png")
	for element in images_files:
		os.remove(element)



def get_description_of_variables(input_file):
	"""
	-> Try to figure out if variables describe in input_file are
	   qualitative or quantitative.
	-> return a dict with the name of quantitative and qualitative variable
	"""
	type_to_variables = {}
	type_to_variables["qualitative"] = []
	type_to_variables["quantitative"] = []

	## Get the data 
	index_to_variable = {}
	variable_to_value = {}
	input_data = open(input_file, "r")
	cmpt = 0
	for line in input_data:
		line = line.replace("\n", "")
		line_in_array = line.split(",")
		if(cmpt == 0):
			index = 0
			for var in line_in_array:
				index_to_variable[index] = var
				variable_to_value[var] = []
				index += 1
		else:
			index = 0
			for scalar in line_in_array:
				variable_to_value[index_to_variable[index]].append(scalar)
				index += 1
		cmpt += 1
	input_data.close()

	## Test if variable is qualitative or not
	quantitative_variable = []
	qualitative_variable = []
	for key in variable_to_value.keys():
		var_is_quantitative = True
		for scalar in variable_to_value[key]:
			if(scalar != "NA"):
				try:
					scalar = float(scalar)
				except:
					var_is_quantitative = False
		if(var_is_quantitative):
			quantitative_variable.append(key)
		else:
			qualitative_variable.append(key)
	type_to_variables["qualitative"] = qualitative_variable
	type_to_variables["quantitative"] = quantitative_variable

	## return the results
	return type_to_variables



def build_data_file_from(explain_variable, descriptives_variable, data_file):
	"""
	-> Build a new file from data_file
	-> explain_variable is a string, the name of the variable to explain (the first column)
	-> descriptives_variable is a list of descriptives_variable
	TODO:
		- test data position on a small data file
	"""

	data_file_name = data_file.split(".")
	data_file_name = data_file_name[0]
	output_name = "subset_from_"+str(data_file_name)+".csv"
	index_to_variable = {}
	variable_to_index = {}
	index_to_variable_in_new_array = {}

	data = open(data_file, "r")
	output = open(output_name, "w")
	cmpt = 0

	## Prepare header
	header = ""
	header += explain_variable+","
	index_to_variable_in_new_array[0] = explain_variable
	index = 1
	for var in descriptives_variable:
		header += var +","
		index_to_variable_in_new_array[index] = var
		index +=1
	header = header[:-1]
	output.write(header+"\n")
	for line in data:
		line = line.replace("\n", "")
		line_in_array = line.split(",")
		if(cmpt == 0):
			index = 0
			for var in line_in_array:
				if(explain_variable == var):
					index_to_variable[explain_variable] = index
					variable_to_index[var] = index
				elif(var in descriptives_variable):
					index_to_variable[var] = index
					variable_to_index[var] = index
				index += 1
		else:
			line_to_write = ""
			line_to_write += line_in_array[variable_to_index[explain_variable]]+","
			for var in descriptives_variable:
				line_to_write += line_in_array[variable_to_index[var]] + ","
			line_to_write = line_to_write[:-1]
			output.write(line_to_write+"\n")
		cmpt +=1
	output.close()
	data.close()


def drop_patients_with_NA(input_file):
	"""
	-> Create a new file from input_file and
	   drop every line containing NA values
	"""

	data_file_name = input_file.split(".")
	data_file_name = data_file_name[0]
	output_name = str(data_file_name)+"_without_NA.csv"

	input_data = open(input_file, "r")
	output_data = open(output_name, "w")

	for line in input_data:
		line = line.replace("\n", "")
		line_in_array = line.split(",")

		keep_the_line = True

		if("NA" in line_in_array):
			keep_the_line = False

		if(keep_the_line):
			output_data.write(line+"\n")

	output_data.close()
	input_data.close()


def control_subset_file(file_to_test):
	"""
	-> count the number of line in a file
	-> return True if > 10 cases in file, if not return False
	"""

	data = open(file_to_test, "r")
	cmpt = 0
	for line in data:
		cmpt += 1
	data.close()
	enought_patient_in_file = True
	if(cmpt < 10):
		enought_patient_in_file = False

	return enought_patient_in_file


### TEST SPACE ###
#sep = detect_file_format("play.txt")
#print sep
#change_file_format("clinical_i2b2trans.txt", ",")
#fix_file_name("test/play.wth.reformated.csv")
#truc = get_description_of_variables("clinical_i2b2trans_reformated.csv")
#build_data_file_from("\\Clinical\\Lab\\LBHANEMIA", ["\\HLA\\Alleles\\HLADRB10406","\\HLA\\Alleles\\HLAC0202","\\HLA\\Alleles\\HLAA3601"], "clinical_i2b2trans_reformated.csv")
#drop_patients_with_NA("subset_from_clinical_i2b2trans_reformated.csv")
#test = control_subset_file("subset_from_clinical_i2b2trans_reformated.csv")
#clean()