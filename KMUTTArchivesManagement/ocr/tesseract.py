import cv2
import os
import sys
import numpy as np
from multiprocessing import Pool
import pytesseract
from pytesseract import Output
import logging
import re

import ocr.Pdf2img as P2i
import ocr.document as Doc
import ocr.imageprocessing as Imp
from KMUTTArchivesManagement import settings

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

### Global variable ###
ROOT = os.path.abspath(os.getcwd())
PATH_REPORT = os.path.join(ROOT, 'document-report')

TEXT_MIN_WIDTH = 15      # min reduced px width of detected text contour
TEXT_MIN_HEIGHT = 2      # min reduced px height of detected text contour
TEXT_MIN_ASPECT = 1.5    # filter out text contours below this w/h ratio
TEXT_MAX_THICKNESS = 10  # max reduced px thickness of detected text contour
TEXT_MAX_HEIGHT = 100 

def sortTextOCR(externalBox, widthImage):
    sortCnt = sorted(
        externalBox, key=lambda ctr: ctr[0] + ctr[1] * widthImage)
    return sortCnt


def listDirectory(path):
    listDir = False
    try:
        listDir = [os.path.join(path, f)
                   for f in os.listdir(path) if f.endswith(".jpg")]
    except OSError:
        print("Error: path Error maybe wrong name!!!!")
    return listDir


def tesseractOcr(picture):
    custom_config = r'--oem 1'
    config = custom_config
    text = pytesseract.image_to_string(
        picture, lang='tha+eng', config=custom_config)
    # for add context docx to check error
    cleanText = Doc.cleanTextRegex(text)
    if cleanText:
        return cleanText
    return False


def pipelineOCR(image, page, fileName):
    imageText = Imp.removeBG(image)
    cnts = Imp.findContours(imageText)
    boundaryBox = []
    for cnt in cnts:
        boundaryBox.append(cv2.boundingRect(cnt))
    sortCnts = sortTextOCR(boundaryBox, image.shape[1])
    imageText = cv2.bitwise_not(imageText)
    # imageRepair = repairImage(imageText)
    fulltext = ''
    for inx, box in enumerate(sortCnts):
        x, y, w, h = box
        if h < TEXT_MIN_HEIGHT or w < TEXT_MIN_WIDTH:
            pass
        # repairOCR = imageRepair[y:y+h, x:x+w].copy()
        cropToOCR = imageText[y:y+h, x:x+w].copy()
        text = tesseractOcr(cropToOCR)
        if text:
            fulltext = fulltext + " " + text
    Doc.addReportText(fulltext, page, fileName)


def main(fileName, name, startPage):
    page = int(startPage)
    path = P2i.convertPdftoJpg(name, fileName, page)
    Doc.createDirectory(PATH_REPORT)
    Doc.createDirectory(PATH_REPORT+"/"+fileName)
    poolOCR = Pool(processes=8)
    listPathImage = listDirectory(path)
    for pathImage in listPathImage:
        pageNumber = re.search('page(.*).jpg', pathImage).group(1)
        image = cv2.imread(pathImage)
        poolOCR.apply_async(pipelineOCR, args=(image, pageNumber, fileName, ))
    poolOCR.close()
    poolOCR.join()
    print('FinishOCR: ', fileName)


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