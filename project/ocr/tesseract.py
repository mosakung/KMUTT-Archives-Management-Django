import numpy as np
import pytesseract
from pytesseract import Output
import sys
import os
import cv2
import concurrent.futures as cf

import ocr.Pdf2img as PI
import ocr.document as Doc
import ocr.imageprocessing as Imp

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

### Global variable ###

FILENAME = ""
ROOT = os.path.abspath(os.getcwd())
PATH_IMAGE = ROOT+"/project/images/"+FILENAME
PATH_REPORT = ROOT + "/report/"
PATH_DOC = PATH_REPORT + "report-"+FILENAME + ".docx"


def CalculateTextConfident(Text):
    textConcat = ''
    for i in range(len(Text['text'])):
        if int(Text['conf'][i]) >= 35:
            textConcat = textConcat+Text['text'][i]
    return textConcat


def tesseractOcr(picture, page, reportName, reportDoc=False):
    imageOCR = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
    custom_config = r'--oem 1'
    config = custom_config
    # textconfident = pytesseract.image_to_data(
    # imageOCR, lang = 'tha+eng', output_type = Output.DICT, config = custom_config)
    # textcon = CalculateTextConfident(textconfident)
    text = pytesseract.image_to_string(
        imageOCR, lang='tha+eng', config=custom_config)
    # for add context docx to check error
    cleanText = Doc.cleanTextRegex(text)
    if cleanText:
        return cleanText
    return False


def setGlobalVariable(fileName):
    global FILENAME
    global PATH_IMAGE
    global PATH_DOC
    FILENAME = fileName
    PATH_DOC = PATH_REPORT + "report-"+FILENAME + ".docx"
    PATH_IMAGE = ROOT+"/project/images/"+FILENAME


def prepareOCR(imagePrepare, page, mydoc=False):
    skipPage = Imp.skipPage(imagePrepare)
    if not skipPage:
        # remove picture & line & get angle to rotated
        imageOnlyText, angleBox, externalBox = Imp.prepareRotated(imagePrepare)
        imageRemoveLine = Imp.removeLine(imageOnlyText)
        # rotated & OCR image
        fulltext = ''
        if mydoc:
            mydoc.add_heading("Page: "+str(page), 0)
        for inx, box in enumerate(externalBox):
            imageRotated = Imp.rotated(imageRemoveLine, angleBox, inx, box)
            text = tesseractOcr(imageRotated, page, FILENAME, mydoc)
            if text:
                fulltext = fulltext + " " + text
                if mydoc:
                    Doc.addReportDoc(text, imageRotated, mydoc, PATH_DOC)
        # add text to file for TF/IDoc
        Doc.createDirectory(PATH_REPORT)
        Doc.addReportText(fulltext, page, FILENAME)
        return fulltext


def main(fileName, name):
    PI.convertPdftoJpg(name, fileName)
    setGlobalVariable(name)
    Doc.createDirectory(PATH_REPORT)
    Doc.createDirectory(PATH_REPORT+"/"+FILENAME)
    # report
    # mydoc = Doc.createDoc(PATH_DOC)
    ####
    poolOCR = cf.ThreadPoolExecutor(max_workers=2)
    while(True):
        loopPage = Doc.checkFile(PATH_IMAGE + "/page"+str(page)+".jpg")
        if loopPage:
            image = cv2.imread(PATH_IMAGE + "/page"+str(page)+".jpg")
            imagePrepare = image.copy()
            poolOCR.submit(prepareOCR, imagePrepare, page)
            # prepareOCR(imagePrepare, page, mydoc)
        else:
            break


# Handle Ctrl-C Interrupt
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted ..')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
