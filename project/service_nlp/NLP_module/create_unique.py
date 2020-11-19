def unique(words):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for x in words:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list
