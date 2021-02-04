landa1 = 0.1
landa2 = 0.4
landa3 = 0.5
epsilon = 0.3


def getTrainSetUnigram(path):
    file = open(path, "r", encoding='UTF-8')
    dictionary = dict()
    while True:
        fs = file.readline()
        if len(fs) == 0:
            break
        fs = fs[:-1]
        fs = "<s> " + fs + " </s>"
        words = fs.split()
        for word in words:
            dictionary[word] = dictionary.get(word, 0) + 1
    return dictionary


def getTrainSetBigram(path):
    file = open(path, "r", encoding='UTF-8')
    dictionary = dict()
    while True:
        fs = file.readline()
        if len(fs) == 0:
            break
        fs = fs[:-1]  # deleting \n from end of sentence
        fs = "<s> " + fs + " </s>"
        words = fs.split()
        preWord = None
        for word in words:
            if preWord is not None:
                dictionary[(preWord, word)] = dictionary.get((preWord, word), 0) + 1
            preWord = word
    return dictionary


def getTestSet(path):
    file = open(path, "r", encoding='UTF-8')
    dictionary = dict()
    while True:
        fs = file.readline()
        if len(fs) == 0:
            break
        split = fs.split("\t")

        poem = "<s> " + split[1][:-1] + " </s>"
        dictionary[poem] = int(split[0])
    return dictionary


class UnigramModel:
    def __init__(self, path):
        self.dictionary = {key: val for key, val in getTrainSetUnigram(path).items() if val > 0}
        self.uniqueWordSize = len(self.dictionary)
        self.wordsSize = sum(self.dictionary.values())

    def unigramWordProb(self, word):
        wordNo = self.dictionary.get(word, 0)
        if wordNo == 0 or self.wordsSize == 0:
            return 0
        else:
            return float(wordNo) / float(self.wordsSize - self.dictionary.get("<s>") - self.dictionary.get("</s>"))

    def unigramSentenceProb(self, sentence):
        probSum = 1
        words = sentence.split(" ")
        for i in words:
            probSum *= self.unigramWordProb(i)
        return probSum


class BigramModel(UnigramModel):
    def __init__(self, path):
        UnigramModel.__init__(self, path)
        self.Bidictionary = {key: val for key, val in getTrainSetBigram(path).items() if val > 0}

    def bigramWordProb(self, preWord, word):
        WordsNo = self.Bidictionary.get((preWord, word), 0)
        WordNo = self.dictionary.get(preWord, 0)
        if WordsNo == 0 or self.dictionary.get(word, 0) == 0:
            return 0
        return float(WordsNo) / float(WordNo)

    def bigramSentenceProb(self, sentence):
        sentence = "<s> " + sentence + " </s>"
        words = sentence.split(" ")
        preWord = None
        probSum = float(1)
        for word in words:
            if preWord is not None:
                probSum *= self.bigramWordProb(preWord, word)
            preWord = word
        return probSum

    def backOffWordProb(self, preWord, word):
        return (self.bigramWordProb(preWord, word) * landa3) + (self.unigramWordProb(word) * landa2) + (landa1 * epsilon)

    def backOffSentenceProb(self, sentence):
        sentence = "<s> " + sentence + " </s>"
        words = sentence.split(" ")
        preWord = None
        probSum = float(1)
        for word in words:
            if preWord is not None:
                probSum *= self.backOffWordProb(preWord, word)
            preWord = word
        return probSum





print(getTestSet("./test_set/test_file.txt"))
ferdowsiDictionary = BigramModel("./train_set/ferdowsi_train.txt")
hafezDictionary = BigramModel("./train_set/hafez_train.txt")
molavaiDictionary = BigramModel("./train_set/molavi_train.txt")
testSet = getTestSet("./test_set/test_file.txt")
rightAnswer = 0
for key, value in testSet.items():
    answer = 0
    ferdowsiProb = ferdowsiDictionary.backOffSentenceProb(key)
    hafezProb = hafezDictionary.backOffSentenceProb(key)
    molaviProb = molavaiDictionary.backOffSentenceProb(key)
    maxProb = max(ferdowsiProb, hafezProb, molaviProb)
    if maxProb == ferdowsiProb:
        answer = 1
    elif maxProb == hafezProb:
        answer = 2
    else:
        answer = 3
    if answer == value:
        rightAnswer += 1
print("Right Answers : " + str(rightAnswer))
print(float(rightAnswer)/float(len(testSet)))




