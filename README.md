#pyPDFSearch -- v.CHARLIE

##Overview
pyPDFSearch is a solution to aggregate web PDF search. Instead of opening 
each PDF on a webpage, pyPDFSearch allows you to download and search all 
PDFs concurrently. 


##Installation
You can run pyPDFSearch with Python3 by invoking the following at 
command line:\n
    `$ python3 pyPDFSearch.py`

Note that you must have the following packages installed: requests, re, sys, 
os, hashlib, _thread, threading, urllib, and PyPDF2. Dependencies can be 
installed with the following:\n
    `$ pip install -r requirements.txt`


##Technical
Also, pyPDFSearch will download online PDFs to your local machine to 
search in the working directory where it is installed. When you are 
finished searching, pyPDFSearch will automatically delete the local 
directory it creates to store your files.

However, if you run into an unexpected runtime error, it is possible that
the directory will not be deleted. In such an event, the next time you try
to use pyPDFSearch, the program will recognize that the directoy exists and
ask if you would like to overwrite it - if you do not, you will not be able
to run pyPDFSearch since a local directory is needed.


##Limitations
Given the nonuniform generation of PDF documents, pyPDFSearch is limited 
to PDFs that are well-formatted according to PDF standards. For non-standard 
PDFs, the PyPDF2 module that pyPDFSearch relies on will not be able to extract 
data from the file so search will not function properly. Even though search will 
not be able to find anything, it will still iterate over all files (although they 
will all have empty contents) and eventually return a valid message that no term 
was found. 


###Contact
tlanham@cs.stanford.edu

