import re


def task1(s):
    return bool(re.fullmatch(r'ab*', s))


def task2(s):
    return bool(re.fullmatch(r'ab{2,3}', s))


def task3(s):
    return re.findall(r'\b[a-z]+_[a-z]+\b', s)


def task4(s):
    return re.findall(r'\b[A-Z][a-z]*\b', s)


def task5(s):
    return bool(re.fullmatch(r'a.*b', s))


def task6(s):
    return re.sub(r'[ ,.]', ':', s)


def task7(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def task8(s):
    return re.split(r'(?=[A-Z])', s)


def task9(s):
    return re.sub(r'([A-Z])', r' \1', s).strip()


def task10(s):
    return re.sub(r'([A-Z])', r'_\1', s).lower()


if __name__ == '__main__':
    print("1:", task1("abbb"))
    print("2:", task2("abb"))
    print("3:", task3("abc_def test"))
    print("4:", task4("Hello WORLD Test"))
    print("5:", task5("axxxb"))
    print("6:", task6("Hello, world. Hi"))
    print("7:", task7("my_variable_name"))
    print("8:", task8("SplitAtUpperCase"))
    print("9:", task9("InsertSpacesHere"))
    print("10:", task10("camelCaseString"))