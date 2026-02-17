# 1 sort using absolute ('-' doesn't make sense)
nums = [3, -10, 2, -7, 5]
print(sorted(nums, key=lambda x: abs(x)))


# 2 sort by len
words = ["banana", "kiwi", "apple", "fig"]
print(sorted(words, key=lambda w: len(w)))


# 3 sort by second element
pairs = [("A", 3), ("B", 1), ("C", 2)]
print(sorted(pairs, key=lambda p: p[1]))


# 4 sort by age value
users = [{"name": "Ali", "age": 17}, {"name": "Dana", "age": 19}, {"name": "Tim", "age": 18}]
print(sorted(users, key=lambda u: u["age"]))  # по возрасту


# 5 firstly by age, second by name
users = [{"name": "Bob", "age": 18}, {"name": "Ali", "age": 18}, {"name": "Dana", "age": 17}]
print(sorted(users, key=lambda u: (u["age"], u["name"])))
