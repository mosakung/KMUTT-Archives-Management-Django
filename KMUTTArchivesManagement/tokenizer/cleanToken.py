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


def delete_latin(word):
    return regex.sub(r'[\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', '', word)
