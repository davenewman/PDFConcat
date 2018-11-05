PDFConcatenator is a command line tool written in Python 3 used to concatenate
PDFs, rotate PDFs, and perform combinations of concatenation and rotation on PDF 
files within the local directory. The numeric inputs below are clockwise rotations 
in degrees.

To concatenate and rotate files in the current directory:
PDFConcat -c <filename> <0 | 90 | 180 | 270 > <filename>....

To concatenate all PDF files in the current directory (sorting is alphanumeric
based on filename):
PDFConcat -a

To rotate individual pages within a single PDF:
PDFConcat -i <filename> <page number> |
	<pagenumber1-pagenumber2> |
	<pagenumber1,pagenumber2,...>
	<90 | 180 | 270> 
	

