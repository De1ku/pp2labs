# ф-ия без аргументов 
def say_hi():
    print("Hi!")

say_hi()


# ф-ия с одним арг
def square(x):
    return x * x

print(square(7))


# с двумя арг
def add(a, b):
    return a + b

print(add(10, 5))


# докстринг
def celsius_to_fahrenheit(c):
    """Converts Celsius to Fahrenheit."""
    return c * 9 / 5 + 32

print(celsius_to_fahrenheit(0))


def is_even(n):
    return n % 2 == 0

nums = [1, 2, 3, 4, 5, 6]
print([n for n in nums if is_even(n)])
