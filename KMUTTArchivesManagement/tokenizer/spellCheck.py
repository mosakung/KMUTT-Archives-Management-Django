from pythainlp.util import isthai

from pythainlp.spell import NorvigSpellChecker
from pythainlp.corpus import ttc

from spellchecker import SpellChecker

spell = SpellChecker()
corpus = ttc.word_freqs()
thai = NorvigSpellChecker(custom_dict=corpus)


def load_corpus_thai():
    def readfile():
        path = "./tokenizer/config/corpus_thai_spellcheck"
        with open(path, "r", encoding="utf8") as f:
            return f.read().splitlines()

    corpus_thai = readfile()
    return corpus_thai


corpus_thai = load_corpus_thai()


def spellCheckAuto(word):
    exception = ['ฯ', 'ๆ']

    if(word[0].isupper()):
        return word

    if (word in exception):
        return word

    isThai = isthai(word)
    if isThai:
        if(word in corpus_thai):
            return word
        return thai.correct(word)
    return spell.correction(word)


def spellCheckSpecific(word, corpus):
    def minimun_edit_distance(word, compare):
        word_len = len(word)
        compare_len = len(compare)
        dp = [[0 for x in range(compare_len + 1)] for x in range(word_len + 1)]

        for i in range(word_len + 1):
            for j in range(compare_len + 1):

                if i == 0:
                    dp[i][j] = j

                elif j == 0:
                    dp[i][j] = i

                elif word[i-1] == compare[j-1]:
                    dp[i][j] = dp[i-1][j-1]

                else:
                    dp[i][j] = 1 + min(dp[i][j-1],
                                       dp[i-1][j],
                                       dp[i-1][j-1])
        return dp[word_len][compare_len]

    if(word[0].isupper()):
        return word

    for row in corpus:
        med = minimun_edit_distance(word, row['term'])
        if(med <= int(row['threshold'])):
            # print("SPEEL CHECK DETECT <MY> >> " + word + " => " + row['term'])
            return row['term']

    return word
