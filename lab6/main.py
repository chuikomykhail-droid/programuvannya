class SentenceIterator:
    def __init__(self, words):
        self.sorted_words = sorted(words)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.sorted_words):
            word = self.sorted_words[self.index]
            self.index += 1
            return word
        else:
            raise StopIteration

class Sentence:
    def __init__(self, data=None):
        if isinstance(data, Sentence):
            self.words = list(data.words)
        elif isinstance(data, str):
            self.words = data.split()
        elif isinstance(data, list):
            self.words = list(data)
        else:
            self.words = []

    def __str__(self):
        text_str = " ".join(self.words)
        count_str = str(len(self.words))
        return text_str

    def __len__(self):
        return len(self.words)

    def __getitem__(self, index):
        return self.words[index]

    def __setitem__(self, index, value):
        self.words[index] = str(value)

    def __add__(self, other):
        if isinstance(other, Sentence):
            return Sentence(self.words + other.words)
        elif isinstance(other, str):
            return Sentence(self.words + [other])
        return Sentence(self.words)

    def __sub__(self, other):
        if isinstance(other, Sentence):
            new_words = []
            for w in self.words:
                if w not in other.words:
                    new_words.append(w)
            return Sentence(new_words)
        elif isinstance(other, str):
            new_words = []
            for w in self.words:
                if w != other:
                    new_words.append(w)
            return Sentence(new_words)
        return Sentence(self.words)

    def __contains__(self, item):
        return item in self.words

    def __iter__(self):
        return SentenceIterator(self.words)


with open("text.txt", "r", encoding="utf-8") as f1:
    raw_text = f1.read()
    f1.close()

text = Sentence(raw_text)


with open("result.txt", "w", encoding="utf-8") as f:
    for word in text:
        f.write(word + "\n")

    f.close()