#!/usr/bin/python

# Attribution for pdf text extraction:
# http://stackoverflow.com/questions/12571905/finding-on-which-page-a-search-string-is-located-in-a-pdf-document-using-python

import requests, re, sys, os, hashlib, _thread
from urllib.request import urlopen
import PyPDF2 as pyPdf
from threading import Thread

cur_search_path = "" # keeps track of current search directory
hash_dict = {} # dict of hashes to urls
dirents = [] # list of websites already downloaded 

def getPDFLinks(website):
    """
    Using the provided website, finds all PDF links and returns list 
    of well formed PDF urls. 
    """
    response = requests.get(website)
    absolute_pdf = re.findall(r'http([^ <>]*).pdf', str(response.content))
    for idx, link in enumerate(absolute_pdf):
        absolute_pdf[idx] = "http" + link + ".pdf"
    relative_pdf = re.findall(r'href=\"([^ <>]*).pdf', str(response.content))
    for idx, link in enumerate(relative_pdf):
        relative_pdf[idx] = website + link + ".pdf"
    return list(set(absolute_pdf).union(relative_pdf))

def confirmDownload(links):
    """
    Asks user to confirm download and provides the number of files that will 
    be downloaded. 
    """
    while (True):
        user_resp = input("  There are " + str(len(links)) + " links, would you like to continue [y/n]? ")
        if (user_resp == "y"):
            break
        elif (user_resp == "n"):
            exitProgram()
        else:
            print("    please enter 'y' or 'n'")

def overwriteDirectory(path):
    """
    Asks user to authenticate an overwrite of the 
    temp directory left over from an interrupted search. 
    """
    while (True):
        user_resp = input(("You already have a directory named pdf_temp/"
                            " that pyPDFSearch needs to use, would you " 
                            "like to overwrite this directory [y/n]? "))
        if (user_resp == "y"):
            os.system("\\rm -r pdf_temp/")
            os.makedirs(path)
            break
        elif (user_resp == "n"):
            sys.exit(0) # exits without deleting directory
        else:
            print("    please enter 'y' or 'n'")

def makeTempDirectory(path):
    """
    If a temp directory doesn't exist, creates one. If one 
    exists from an interrupted search, asks to overwrite it. 
    """
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        overwriteDirectory(path)

def downloadFile(link):
    """
    Downloads a PDF from url that leads to a PDF. 
    Opens the link, then uses the hash of the file url 
    as identifier, stores the hash and url pair in the 
    hash dictionary for lookup in the query phase. 
    """
    try:
        response = urlopen(link)
    except:
        return
    file_name = str(abs(hash(link)))
    hash_dict[file_name] = link
    try: 
        file = open(cur_search_path + "/" + file_name, 'xb')
    except: 
        print("could not open" + file_name)
        raise
    file.write(response.read())
    file.close()
    print("Finished downloading pdf: " + link)

def downloadAllFiles(links):
    """
    Makes a directory to store PDFs to be downloaded in. 
    Downloads each PDF in separate thread and then joins 
    the threads. 
    """
    makeTempDirectory(cur_search_path)
    threads = []
    for pdf_url in links:
        t = Thread(target=downloadFile, args=(pdf_url, ))
        threads.append(t)
        t.start()
    for t in threads: t.join()

def searchFiles(query):
    """
    Searches all PDF files in the current search directory, 
    getting contents of PDF and doing search using the provided 
    query term. If the term is found, prints out the page and 
    PDF it was found in. 
    """
    PageFound = -1
    for pdf_file in os.listdir(cur_search_path):
        try:
            doc = pyPdf.PdfFileReader(open(cur_search_path + "/" + pdf_file, "rb"))
        except:
            continue
        for i in range(0, doc.getNumPages()):
            content = ""
            content += doc.getPage(i).extractText() + "\n"
            content1 = content.encode('ascii', 'ignore').lower()
            ResSearch = re.search(query, str(content1))
            if ResSearch is not None:
                PageFound = i + 1   # 1 index instead of 0-indexed
                print("    Query found on page: " + str(PageFound) + " of PDF with url: " + hash_dict[pdf_file])
    if PageFound == -1:
        print("Sorry, we didn't find anything.\n")

def search(website, query):
    """
    Updates the directory path for the current search, creating a 
    subdirectory for the search using the hash of the website url. 
    Confirms download from the user, downloads files, and then 
    searches. 
    """
    url_hash = str(abs(hash(website)))
    global cur_search_path 
    cur_search_path = os.getcwd() + "/pdf_temp" + "/" + url_hash
    # only downloads if it's a new website
    if not url_hash in dirents:
        dirents.append(url_hash)
        pdf_links = getPDFLinks(website)
        confirmDownload(pdf_links)
        downloadAllFiles(pdf_links)
    searchFiles(query)

def exitProgram():
    """
    Exits the main thread of execution, first deleting the 
    temporary directory used to store downloaded PDF files
    """
    if os.path.exists(os.getcwd() + "/pdf_temp/"):
        os.system("\\rm -r pdf_temp/")
    print("Thanks for searching!")
    sys.exit(0)

if __name__ == '__main__':
    """
    First makes a temporary directory to store downloaded PDFs, 
    makes a new subdirectory for each webpage. Prompts user for a 
    website to scrape for PDFs and a query term to search them 
    """
    makeTempDirectory(os.getcwd() + "/pdf_temp")
    print("Welcome to pyPDFSearch!")
    while (True):
        website = input("Website to search, please include full url (or ENTER to exit): ")
        if not website: break
        while (True):
            query = input("Search pdfs for (input search term or ENTER to search a different webpage): ")
            if not query: break
            search(website, query.lower())
    exitProgram()
