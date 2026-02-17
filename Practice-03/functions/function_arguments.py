# positional
def power(base, exp):
    return base ** exp

print(power(2, 5))


# keyword args
def rectangle_area(width, height):
    return width * height

print(rectangle_area(height=4, width=10))


# default arg
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Iskander"))
print(greet("Iskander", greeting="Salem"))


# pos+keyword
def format_user(name, age, city="Almaty"):
    return f"{name}, {age}, {city}"

print(format_user("Aruzhan", 19))
print(format_user("Aruzhan", 19, city="Astana"))


def create_account(username, *, is_admin=False, is_active=True):
    return {"username": username, "is_admin": is_admin, "is_active": is_active}

print(create_account("neo"))
print(create_account("root", is_admin=True))
