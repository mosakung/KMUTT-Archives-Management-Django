import os
from pdf2image import convert_from_path

#poppler
#pdf2image

def convertPdftoJpg(pathName,pdfName):
    # define the name of the directory to be created
    path = "../images/"+pathName
    try:
        os.mkdir(path)
        print ("Successfully created the directory %s" % path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Already have the directory %s" % path)

    poppler_path = r'./poppler-0.68.0/bin'
    pages = convert_from_path('../pdf/'+ pdfName +'.pdf',dpi=300,poppler_path=poppler_path,size=2000)
    count = 1
    for page in pages:
        page.save(path+'/page'+str(count)+'.jpg', fmt='jpg')
        count = count+1

