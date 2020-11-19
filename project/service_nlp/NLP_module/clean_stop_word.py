import pythainlp

def filter_stop_word(word):
    stopword = pythainlp.corpus.thai_stopwords()
    if(word in stopword):
        return False
    else:
        return True
