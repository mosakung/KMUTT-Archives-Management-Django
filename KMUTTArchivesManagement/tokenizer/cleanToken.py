import re as regex


def to_lower_case(s):
    if(s[0].isupper()):
        return s
    return str(s).lower()


def delete_unnecessary_words(word):
    filterSet = '\'“”!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'

    if (word in filterSet):
        return False
    elif (word == ''):
        return False
    return True


def delete_space(word):
    return regex.sub(r'\s', '', word)
