import nltk
import os

# NLTK Dowload all


def initNLTKCorpus():
    print("\nINIT NLTK Corpus")
    nltk.download('all')
    print()


initNLTKCorpus()

# create directory


def initDirectoryDocument():
    root = os.getcwd()

    pathImage = root + "\\document-image"
    pathPdf = root + "\\document-pdf"
    pathReport = root + "\\document-report"

    print("\nINIT Directory Document")

    if not os.path.isdir(pathImage):
        try:
            os.mkdir(pathImage)
        except OSError:
            print("Creation of the directory <%s> failed" % pathImage)
        else:
            print("Successfully created the directory <%s> " % pathImage)
    else:
        print("Already DIR <%s>" % pathImage)

    if not os.path.isdir(pathPdf):
        try:
            os.mkdir(pathPdf)
        except OSError:
            print("Creation of the directory <%s> failed" % pathPdf)
        else:
            print("Successfully created the directory <%s> " % pathPdf)
    else:
        print("Already DIR <%s>" % pathPdf)

    if not os.path.isdir(pathReport):
        try:
            os.mkdir(pathReport)
        except OSError:
            print("Creation of the directory <%s> failed" % pathReport)
        else:
            print("Successfully created the directory <%s> " % pathReport)
    else:
        print("Already DIR <%s>" % pathReport)

    print()


initDirectoryDocument()
