import re as regex


def loadSpecific():
    def readfile():
        path = "./tokenizer/config/term_specific"
        with open(path, "r", encoding="utf8") as f:
            return f.read().splitlines()

    regex_pattern = ",\s*"
    terms = readfile()
    result = []
    for item in terms:
        split_item = regex.split(regex_pattern, item)
        result.append({
            'term': split_item[0],
            'threshold': split_item[1]
        })
    return result
