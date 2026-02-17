# 1
nums = [1, 2, 3, 4]
res = list(map(lambda x: x + 1, nums))
print(res)


# 2
nums = [2, 5, 7]
res = list(map(lambda x: x * x, nums))
print(res)


# 3
strings = ["10", "20", "003"]
res = list(map(lambda s: int(s), strings))
print(res)


# 4 using two lists
a = [1, 2, 3]
b = [10, 20, 30]
res = list(map(lambda x, y: x + y, a, b))
print(res)


# 5 get name value from dicts in list users
users = [{"name": "Ali", "age": 17}, {"name": "Dana", "age": 19}]
names = list(map(lambda u: u["name"], users))
print(names)
