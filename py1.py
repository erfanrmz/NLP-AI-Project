def getTrainSet(file):
    dictionary = dict()
    while True:
        fs = file.readline()
        if len(fs) == 0:
            break
        words = fs.split()
        for word in words:
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1
    return dictionary


f = open("./train_set/ferdowsi_train.txt", "r", encoding='UTF-8')
h = open("./train_set/hafez_train.txt", "r", encoding='UTF-8')
m = open("./train_set/molavi_train.txt", "r", encoding='UTF-8')
ferdowsiVoc = {key: val for key, val in getTrainSet(f).items() if val > 2}
hafezVoc = {key: val for key, val in getTrainSet(h).items() if val > 2}
molaviVoc = {key: val for key, val in getTrainSet(m).items() if val > 2}

print(ferdowsiVoc)
print(hafezVoc)
print(molaviVoc)
