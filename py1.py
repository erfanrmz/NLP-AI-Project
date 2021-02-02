dictionary = dict()
def word_count(str):
    words = str.split()
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1

    return
f = open("hello1.txt", "r",encoding='UTF-8')
while True:
    fs = f.readline()
    if len(fs) == 0:
        break
    word_count(fs)
print(dictionary)
