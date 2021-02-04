landa1 = 0.1
landa2 = 0.5
landa3 = 0.4
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
        print((self.bigramWordProb(preWord, word) * landa3))
        print((self.unigramWordProb(word) * landa2))
        print((landa1 * epsilon))
        return (self.bigramWordProb(preWord, word) * landa3) + (self.unigramWordProb(word) * landa2) + (landa1 * epsilon)





ferdos = BigramModel("hello1.txt")
print(ferdos.dictionary)
print(ferdos.Bidictionary)
# print(ferdos.bigramWordProb("<s>", "a"))
# print(ferdos.bigramWordProb("a", "a"))
# print(ferdos.bigramWordProb("a", "b"))
# print(ferdos.bigramWordProb("b", "b"))
# print(ferdos.unigramWordProb("a"))
# print(ferdos.unigramWordProb("b"))
# print(ferdos.bigramWordProb("b", "a"))
print(ferdos.backOffWordProb("b", "a"))
# print(ferdos.bigramSentenceProb("b a a"))
# print("yes")
# print(ferdos.dictionary)
