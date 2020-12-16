import re as regex


def delete_unnecessary_words(array_word):
    unnecessary_words = [" ", '\r\n', '', ',',
                         '-', '_', '(', ')', '\'', '\"', '.', "/"]

    # loop unnecessary_words
    for un_word in unnecessary_words:
        # loop delete word
        count = array_word.count(un_word)
        for index in range(count):
            array_word.remove(un_word)

    return array_word


def delete_space_regex(word):
    filter_word = regex.sub(r'\s', '', word)
    return filter_word
