def word_count(str):
    dictionary  = dict()
    words = str.split()

    for word in words:
        if word in dictionary :
            dictionary [word] += 1
        else:
            dictionary [word] = 1

    return dictionary

print(word_count('سحر سحر یک دو سه کرد ما را چنین چنان چنان'))