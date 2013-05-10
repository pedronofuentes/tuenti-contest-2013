from sys import stdin


class Suggestor():
    def __init__(self, words, dictionary_file):
        self.words = words
        self.dictionary_file = dictionary_file
        self.index = {}
        self.suggested_words = []

        self.processDictionary()

    def processDictionary(self):
        position = 0
        with open(self.dictionary_file, 'r') as the_dictionary:
            for line in the_dictionary.readlines():
                word = line.rstrip()
                self.addToIndexInPosition(word, position)
                position += 1

    def addToIndexInPosition(self, word, position):
        number_of_letters = len(word)
        hash_string = self.getHashStringFromWord(word)
        self.addWordToIndexWithHashString(
            word,
            number_of_letters,
            hash_string
        )

    def getHashStringFromWord(self, word):
        hash_dictionary = {}
        for letter in word:
            if not letter in hash_dictionary:
                hash_dictionary[letter] = 1
            else:
                hash_dictionary[letter] += 1

        hash_string = ''
        for key in sorted(hash_dictionary.iterkeys()):
            hash_string = "%s%s%d" % (hash_string, key, hash_dictionary[key])

        return hash_string

    def addWordToIndexWithHashString(self,
                                     word,
                                     number_of_letters,
                                     hash_string):
        if not number_of_letters in self.index:
            self.index[number_of_letters] = {
                hash_string: [word],
            }
        else:
            if not hash_string in self.index[number_of_letters]:
                self.index[number_of_letters][hash_string] = [word]
            else:
                self.index[number_of_letters][hash_string].append(word)

    def printSuggestedWords(self):
        self.findSuggestedWords()
        for word in self.suggested_words:
            print "%s -> %s" % (word[0], ' '.join(word[1]))

    def findSuggestedWords(self):
        for word in self.words:
            words_found = self.getSuggestedWords(word)
            if word in words_found:
                i = words_found.index(word)
                del words_found[i]
            self.suggested_words.append([word, words_found])

    def getSuggestedWords(self, word):
        len_word = len(word)
        if len_word in self.index:
            word_hash_string = self.getHashStringFromWord(word)
            if word_hash_string in self.index[len_word]:
                return self.index[len_word][word_hash_string]

        return []

    def printStats(self):
        len_hashes = 0
        for key in self.index:
            len_hashes += len(self.index[key])
        print "Index with %d entries and %d hashes" % (len(self.index),
                                                       len_hashes)
        print "Index:", self.index

if __name__ == '__main__':
    dictionary_file = ''
    suggestion_numbers = 0
    words = []
    i = 0

    for line in stdin.readlines():
        if line.rstrip() and line[0] != '#':
            if not dictionary_file:
                dictionary_file = line.rstrip()
            elif not suggestion_numbers:
                suggestion_numbers = int(line.rstrip())
            elif i < suggestion_numbers:
                words.append(line.rstrip())

    suggestor = Suggestor(words, dictionary_file)
    suggestor.printSuggestedWords()
