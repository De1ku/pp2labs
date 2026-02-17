# 1
square = lambda x: x * x
print(square(6))


# 2
add = lambda a, b: a + b
print(add(10, 5))


# 3
def make_multiplier(k):
    return lambda x: x * k

times3 = make_multiplier(3)
print(times3(7))


# 4
to_last_char = lambda s: s[-1]
print(to_last_char("hello"))


# 5 lambda in condition
sign = lambda x: "pos" if x > 0 else ("zero" if x == 0 else "neg")
print(sign(5), sign(0), sign(-2))
