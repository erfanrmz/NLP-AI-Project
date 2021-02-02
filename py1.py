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


class UnigramModel:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.uniqueWordSize = len(self.dictionary)
        self.wordsSize = sum(dictionary.values())

    def wordProb(self,word):
        wordNo = self.dictionary.get(word,0)
        if wordNo == 0 or self.wordsSize == 0:
            return 0
        else:
            return float(wordNo)/float(self.wordsSize)
    def sentenceProb(self,sentence):
        probSum = 1
        words = probSum.split(" ")
        for i in words:
            probSum *= self.wordProb(i)
        return probSum


print(ferdowsiVoc)
print(hafezVoc)
print(molaviVoc)
