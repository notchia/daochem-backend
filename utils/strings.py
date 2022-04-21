import re
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer


def tokenize(text):
    tokenizer = RegexpTokenizer('\w+')
    text_tokenized = tokenizer.tokenize(text.lower())
    return text_tokenized


def camel_to_snake(s):
    words = re.findall('[a-zA-Z][^A-Z]*', s)
    s_new = "_".join([w.lower() for w in words])
    return s_new


def snake_to_camel(s, upper=False):
    words = s.split("_")
    if upper:
        words_camel = [w.capitalize() for w in words]
    else:
        words_camel = [words[0]]
        if len(words) > 1:
            words_camel.extend([w.capitalize() for w in words[1:]])

    s_new = "".join(words_camel)
    return s_new


def camel_to_plain(s):
    return s


def snake_to_plain(s):
    return s


def plain_to_camel(s, upper=False):
    return s


def plain_to_snake(s):
    return s


if __name__ == "__main__":
    assert camel_to_snake("articulatedTrace") == "articulated_trace"
    assert camel_to_snake("test") == "test"
    assert camel_to_snake("DummyClass") == "dummy_class"

    assert snake_to_camel("articulated_trace") == "articulatedTrace"
    assert snake_to_camel("test") == "test"
    assert snake_to_camel("dummy_class", upper=True) == "DummyClass"

    print("All tests passed")