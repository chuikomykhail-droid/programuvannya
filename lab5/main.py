class SentenceError(Exception):
    pass


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
        return text_str

    def __len__(self):
        return len(self.words)

    def __getitem__(self, index):
        return self.words[index]

    def __setitem__(self, index, value):
        if not isinstance(value, str):
            raise SentenceError(f"Помилка заміни: значення '{value}' не є рядком (str). Отримано тип {type(value).__name__}.")
        self.words[index] = value

    def __add__(self, other):
        if isinstance(other, Sentence):
            return Sentence(self.words + other.words)
        elif isinstance(other, str):
            return Sentence(self.words + [other])
        else:
            raise SentenceError(f"Помилка додавання (+): неприпустимий тип правого операнда '{type(other).__name__}'. Очікується Sentence або str.")

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
        else:
            raise SentenceError(f"Помилка віднімання (-): неприпустимий тип правого операнда '{type(other).__name__}'. Очікується Sentence або str.")

    def __contains__(self, item):
        return item in self.words


try:
    with open("text.txt", "r", encoding="utf-8") as f1:
        raw_text = f1.read()
except FileNotFoundError:
    raw_text = "Hello world this is a test text to check how words are replaced and deleted"

text = Sentence(raw_text)

words_to_replace = {}
try:
    with open("replace.txt", "r", encoding="utf-8") as f2:
        lines = f2.readlines()
        for line in lines:
            s = line.split()
            if len(s) >= 2:
                words_to_replace[s[0]] = s[1]
except FileNotFoundError:
    words_to_replace = {"test": "exam"}

try:
    with open("delete.txt", "r", encoding="utf-8") as f3:
        delete_text = f3.read()
except FileNotFoundError:
    delete_text = "world"

words_to_delete = Sentence(delete_text)


for i in range(len(text)):
    current_word = text[i]
    if current_word in words_to_replace:
        text[i] = words_to_replace[current_word]

text = text - words_to_delete

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(f"LENGTH:{len(text)}" + "\n")
    f.write(str(text))

print(f"Кількість слів після обробки: {len(text)}")


test_sentence = Sentence("Це тестове речення")

try:
    test_sentence[0] = 123
except SentenceError as e:
    print(f"Спіймано виключення: {e}")

try:
    res = test_sentence + 42
except SentenceError as e:
    print(f"Спіймано виключення: {e}")

try:
    res = test_sentence - ["тестове"]
except SentenceError as e:
    print(f"Спіймано виключення: {e}")