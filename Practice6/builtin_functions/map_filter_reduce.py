from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

squared = list(map(lambda x: x ** 2, numbers))
print("Squared numbers using map():", squared)

evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers using filter():", evens)

total = reduce(lambda a, b: a + b, numbers)
print("Sum using reduce():", total)

product = reduce(lambda a, b: a * b, numbers)
print("Product using reduce():", product)