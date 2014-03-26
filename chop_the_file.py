#!/usr/bin/python
# -*- coding: utf-8 -*-

#---------[ Info of this software - Begin ]---------#
# Author: Mehrad Mahmoudian
# Report bug: m.mahmoudian@gmail.com
#
# Created on: Wed Mar 26 16:00:36 2014
# Version Number: 0.0.1.0
# Change Log:
#     - this is the first version and does not have any change YET !!
#
#---------[ Info of this software - End ]---------#


#--------[ Imports - Begin ]--------#
import argparse  # command line argument parser
from os import path # for checking existing directory
from os import makedirs # for creating directory
import time
#--------[ Imports - End ]--------#

#---------[ Functions - Begin]----------#
def write_to_file(the_list, file_name):  # writing each element of array in the output file
    file_name = destination_file_path + file_name
    f = open(file_name, 'w')
    for item in the_list:
            f.write("%s" % str(item))
    f.close()

def printError (inpt_field_name='Input data'): # prints errors related to the action
	print "\nWarning - The",inpt_field_name,"you entered was invalid, try again !\n"


def mkdir (dir_name):  # make directory if it does not exist in the given path
	if dir_name[len(dir_name)-1] != "/" :
		dir_name = dir_name + "/"
	if not path.exists(dir_name):
		makedirs(dir_name)
	return dir_name


def checkFileExists (theFile) :
	# checks if the file exists, and if exists will return True
	try:
		with open(theFile): pass
		return True
	except IOError:
		return False

def getSourceFileName () :  # get existing file name and path from user
	correctFileName = False
	while correctFileName != True :
		FileName = raw_input("\nPlease Type the source file name: { for example: results.csv  or  result }\n  > ")
		if len(FileName) > 0:  # if the input file name be not empty
			correctFileName = True
		else:
			printError('source file name')
	return FileName


def getDestination () :
	correctDestination = False
	while correctDestination != True :
		Destination = raw_input("\nPlease Type the destination path for output files: { for example: ~/Desktop }\n  > ")
		if len(Destination) > 0:  # if the input data be not empty
			correctDestination = True
		else:
			printError('destination path')
	return Destination

def getOutputRow () :
	correctOutputRow = False
	while correctOutputRow != True :
		OutputRow = input("\nPlease Type the number of rows you want in output files: { for example: 20 }\n  > ")
		if OutputRow > 0:  # if the input data be not empty
			correctOutputRow = True
		else:
			printError('number of rows')
	return OutputRow


def checkExtension (outputExtension) :
	outputExtension = str(outputExtension)
	if len(outputExtension) > 1 :  # if the inserted extention was more than one character and the first character was not '.' add the '.' at the begining
		if outputExtension[0] != '.' :
			outputExtension = '.' + outputExtension
	elif len(outputExtension) == 1 :
		if outputExtension[0] != '.' :
			outputExtension = '.' + outputExtension
		else:
			outputExtension = '.txt'
	else:
		outputExtension = '.txt'
	return outputExtension

#---------[ Function - End ]----------#


#---------[ Main Code - Begin ]---------#
# [ getting argument from command line ]
parser = argparse.ArgumentParser(prog='Chop_the_file')  # program name
parser = argparse.ArgumentParser(description='This is program is designed to split massive text based files into smaller peices based on given line number.')  # program description
parser.add_argument('--version', action='version', version='%(prog)s 0.0.1.0')
parser.add_argument('--source', action='store', help='Source file that want to chop')
parser.add_argument('--destination', action='store', help='Destination directory. If not exist, will be created.')
parser.add_argument('--rows', action='store', help='Number of rows in each output file.')
parser.add_argument('--extension', action='store', help='Extension of the output file. By default it will be .txt')

args = parser.parse_args()

# [ getting source file name from user ]
if args.source is None :
	source_file_path = getSourceFileName ()
elif len(args.source) < 1 :
	source_file_path = getSourceFileName ()
else:
	source_file_path = args.source


# [ make sure that the source file exist ]
while checkFileExists(source_file_path) == False :
	source_file_path = getSourceFileName ()


# [ getting destination path from user ]
if args.destination is None :
	destination_file_path = getDestination ()
elif len(args.destination) < 1 :
	destination_file_path = getDestination ()
else:
	destination_file_path = mkdir(args.destination)



# [ getting number of rows in each output from user ]
if args.rows is None :
	row_counter_limit = getOutputRow ()
elif len(args.rows) < 1 :
	row_counter_limit = getOutputRow ()
else:
	row_counter_limit = args.rows



# [ checking the extension for the output file ]
if args.extension is None :
	output_extension = '.txt'
elif len(args.extension) < 1 :
	output_extension = '.txt'
else:
	output_extension = checkExtension(args.rows)



# [ internal variables ]
output_iteration = 0
row_counter = 0
my_stack = list()

# [ iteration ]
for line in open(source_file_path,'r'):  # read the file line by line
	my_stack.append(line)  # append the line to the list
	row_counter += 1
	if row_counter == row_counter_limit:  # if we have reached the maximum line limit for each output
		output_iteration += 1
		thefile = ''.join([str(output_iteration), output_extension])  # creating the output file name
		write_to_file(my_stack, thefile)
		row_counter = 0  # resetting the counter
		my_stack = list()  # flush the list


# writing the last file if any lines remained
if len(my_stack):
	output_iteration += 1
	thefile = ''.join([str(output_iteration), output_extension])  # creating the output file name
        write_to_file(my_stack, thefile)

#---------[ Main Code - End ]---------#



