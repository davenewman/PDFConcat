#!/usr/bin/python3
import sys
import os
import PyPDF2
import re

def main(argv):
# main() is responsible for parsing the command line
	method = argv[0]
	args = argv[1:]
	
	if method == '-c':
	# This method involves combination concatenation and rotation of PDFs
	# Failure modes with which to write tests:
	# (1) no files in directory, (2) no PDF files in directory,
	# (3) not a matching state for every PDF
		filenames = []
		states = []
		filenames = [args[ind] for ind in range(0,len(args),2)]
		states = [int(args[ind]) for ind in range(1,len(args),2)]
		concatenate_and_rotate(filenames,states)
	
	elif method == '-a':
	# This method involves concatenation of all PDF files within current dir
	# Failure modes with which to write tests:
	# (1) no files in directory, (2) no PDF files in directory
		filenames = [filename for filename in os.listdir('.') if filename.endswith('.pdf')]
		filenames = sort_alphanumeric(filenames)
		concatenate_all(filenames)
		
	else:
	# This method will take individual pages within a PDF and rotate them
	# Failure modes with which to write tests:
	# (many)
		filename = args[0]
		pagenumbers = []
		states = []
		# will need to turn these into ints later
		pagesep = [args[ind] for ind in range(1,len(args),2)]
		statesep = [int(args[ind]) for ind in range(2,len(args),2)]
		# should have two lists now - something like
		# ['1,55,65','68-74','87']
		# [90, 90, 180]
		# And we need to turn them into something like
		# [1,55,65,68,69,70,71,72,73,74,87]
		# [90,90,90,90,90,90,90,90,90,90,180]
		for ind,string_val in enumerate(pagesep):
			if '-' not in string_val:
				tmp = string_val.split(',')
				for num in tmp:
					pagenumbers.append(int(num))
					states.append(statesep[ind])
			else:
				tmp = string_val.split('-')
				first_page = int(tmp[0])
				last_page = int(tmp[1])
				for num in range(first_page,last_page+1):
					pagenumbers.append(num)
					states.append(statesep[ind])
		# Call the function
		rotate_within_pdf(filename, pagenumbers, states)
	
def concatenate_and_rotate(filenames, states):
# Concatenates and/or rotates pdfs as specified from command line
# Not sure if this will work on PDFs with more than one page, check!	
	information = zip(filenames, states)
	PDFWriteObj = PyPDF2.PdfFileWriter()
	for info in information:
		with open(info[0],'rb') as PDFFileObj:
			PDFReadObj = PyPDF2.PdfFileReader(PDFFileObj)
			for pagenum in range(PDFReadObj.numPages):
				page = PDFReadObj.getPage(pagenum)
				page.rotateClockwise(info[1])
				PDFWriteObj.addPage(page)
			outputObj = open('output.pdf','wb')
			PDFWriteObj.write(outputObj)
			outputObj.close()
	
def concatenate_all(filenames):
# Concatenates all PDF files in the given directory
	PDFWriteObj = PyPDF2.PdfFileWriter()
	for filename in filenames:
		with open(filename,'rb') as PDFFileObj:
			PDFReadObj = PyPDF2.PdfFileReader(PDFFileObj)
			for pagenum in range(PDFReadObj.numPages):
				page = PDFReadObj.getPage(pagenum)
				PDFWriteObj.addPage(page)
			outputObj = open('output_cat.pdf','ab')
			PDFWriteObj.write(outputObj)
			outputObj.close()
	
def rotate_within_pdf(filename, pagenumbers, states):	
	pagenumbers_index = [number - 1 for number in pagenumbers]
	PDFWriteObj = PyPDF2.PdfFileWriter()
	with open(filename, 'rb') as PDFFileObj:
		PDFReadObj = PyPDF2.PdfFileReader(PDFFileObj)
		for pagenum in range(PDFReadObj.numPages):
			page = PDFReadObj.getPage(pagenum)
			if pagenum in pagenumbers_index:
				index = pagenumbers_index.index(pagenum)
				page.rotateClockwise(states[index])
			PDFWriteObj.addPage(page)
		outputObj = open('output_single.pdf','wb')
		PDFWriteObj.write(outputObj)
		outputObj.close()
		
def sort_alphanumeric(filenames):
# Sorts a list in alphanumeric fashion - numbers first then letters
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)',key)]
	return sorted(filenames, key=alphanum_key)				

if __name__ == "__main__":
	main(sys.argv[1:])
