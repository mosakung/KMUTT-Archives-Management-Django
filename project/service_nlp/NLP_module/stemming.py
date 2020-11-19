from nltk.stem import WordNetLemmatizer


def lemmatizer(word):
    wordLema = WordNetLemmatizer().lemmatize(word)
    wordLemmatizer = WordNetLemmatizer().lemmatize(wordLema, 'v')
    caseFloding = wordLemmatizer.casefold()

    return caseFloding
