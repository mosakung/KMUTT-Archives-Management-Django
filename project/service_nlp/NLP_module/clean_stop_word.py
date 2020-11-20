from pythainlp import corpus as thai_corpus


def load_stopword():
    def readfile():
        path = "./service_nlp/NLP_module/config/stopword"
        with open(path, "r", encoding="utf8") as f:
            return f.read().splitlines()

    stopword = readfile()
    return stopword


def filter_stop_word(word):
    stopwords = []
    stopword_th = thai_corpus.thai_stopwords()
    stopword_en = load_stopword()
    stopwords.extend(stopword_th)
    stopwords.extend(stopword_en)
    if(word in stopwords):
        return False
    else:
        return True
