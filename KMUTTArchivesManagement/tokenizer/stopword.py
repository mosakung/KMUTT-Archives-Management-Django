from pythainlp import corpus as thai_corpus


def load_stopword():
    def readfile():
        path = "./tokenizer/config/stopword"
        with open(path, "r", encoding="utf8") as f:
            return f.read().splitlines()

    stopword = readfile()
    return stopword


STOPWORD_EN = load_stopword()


def filterStopword(word):
    stopwords = []
    stopword_th = thai_corpus.thai_stopwords()
    stopword_en = STOPWORD_EN
    stopwords.extend(stopword_th)
    stopwords.extend(stopword_en)
    if(word in stopwords):
        return False
    else:
        return True
