# 1
def abs_value(x):
    return x if x >= 0 else -x

print(abs_value(-12))


# 2
def safe_div(a, b):
    if b == 0:
        return None
    return a / b

print(safe_div(10, 2))
print(safe_div(10, 0))


# 3
def min_max(nums):
    return min(nums), max(nums)

mn, mx = min_max([5, 1, 9, 3])
print(mn, mx)


# 4
def classify_score(score):
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    return "F"

print(classify_score(82))


# 5
def only_positive(nums):
    return [x for x in nums if x > 0]

print(only_positive([-2, 0, 5, 7, -1]))
