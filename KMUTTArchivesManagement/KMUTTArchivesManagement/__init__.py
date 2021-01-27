# import nltk
# import os

# # NLTK Dowload all


# def initNLTKCorpus():
#     print("\nINIT NLTK Corpus")
#     nltk.download('all')
#     print()


# initNLTKCorpus()

# # create directory


# def initDirectoryDocument():
#     root = os.getcwd()

#     pathImage = root + "\\document-image"
#     pathPdf = root + "\\document-pdf"
#     pathReport = root + "\\document-report"

#     print("\nINIT Directory Document")

#     if not os.path.isdir(pathImage):
#         try:
#             os.mkdir(pathImage)
#         except OSError:
#             print("Creation of the directory <%s> failed" % pathImage)
#         else:
#             print("Successfully created the directory <%s> " % pathImage)
#     else:
#         print("Already DIR <%s>" % pathImage)

#     if not os.path.isdir(pathPdf):
#         try:
#             os.mkdir(pathPdf)
#         except OSError:
#             print("Creation of the directory <%s> failed" % pathPdf)
#         else:
#             print("Successfully created the directory <%s> " % pathPdf)
#     else:
#         print("Already DIR <%s>" % pathPdf)

#     if not os.path.isdir(pathReport):
#         try:
#             os.mkdir(pathReport)
#         except OSError:
#             print("Creation of the directory <%s> failed" % pathReport)
#         else:
#             print("Successfully created the directory <%s> " % pathReport)
#     else:
#         print("Already DIR <%s>" % pathReport)

#     print()


# initDirectoryDocument()

import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)
