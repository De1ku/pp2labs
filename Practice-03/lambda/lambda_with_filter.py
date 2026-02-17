# 1 only even
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)


# 2 only pos
nums = [-2, 0, 5, -1, 7]
pos = list(filter(lambda x: x > 0, nums))
print(pos)


# 3 strs with len >= 5
words = ["cat", "tiger", "wolf", "horse"]
long_words = list(filter(lambda w: len(w) >= 5, words))
print(long_words)


# 4 users above 18
users = [{"name": "Ali", "age": 17}, {"name": "Dana", "age": 19}, {"name": "Tim", "age": 18}]
adults = list(filter(lambda u: u["age"] >= 18, users))
print(adults)


# 5 ints which % 3 and % 5 == 0
nums = list(range(1, 31))
special = list(filter(lambda x: x % 3 == 0 or x % 5 == 0, nums))
print(special)
