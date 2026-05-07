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


with open("text.txt", "r", encoding="utf-8") as f1:
    raw_text = f1.read()
    f1.close()

text = Sentence(raw_text)

words_to_replace = {}
with open("replace.txt", "r", encoding="utf-8") as f2:
    lines = f2.readlines()
    f2.close()
    for line in lines:
        s = line.split()
        words_to_replace[s[0]] = s[1]

with open("delete.txt", "r", encoding="utf-8") as f3:
    delete_text = f3.read()
    f3.close()

words_to_delete = Sentence(delete_text)


for i in range(len(text)):
    current_word = text[i]
    if current_word in words_to_replace:
        text[i] = words_to_replace[current_word]

text = text - words_to_delete
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(f"LENGTH:{len(text)}" + "\n")
    f.write(str(text))
    f.close()
print(len(text))