def linebreak(string, charlimit=48):
    if len(string) < charlimit:
        return string
    else:
        words = string.split(' ')
        chunks = ['']
        for word in words:
            if chunks == [] or len(chunks[-1])+len(word) > charlimit:
                chunks.append(word + ' ')
            else:
                chunks[-1] += word + ' '
        return chunks

def i18n(string, chars, charcodes):
    for char in chars:
        string = string.replace(char, charcodes[chars.index(char)])
    return string
