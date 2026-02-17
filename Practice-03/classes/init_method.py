# 1
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 5)
print(p.x, p.y)


# 2
class User:
    def __init__(self, name, role="student"):
        self.name = name
        self.role = role

print(User("Ali").role)
print(User("Dana", role="admin").role)


# 3 validation in init
class Age:
    def __init__(self, value):
        if value < 0:
            raise ValueError("age cannot be negative")
        self.value = value

a = Age(18)
print(a.value)


# 4 computing in init
class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.area = w * h

r = Rectangle(4, 7)
print(r.area)


# 5 modifying input
class Email:
    def __init__(self, address):
        self.address = address.strip().lower()

e = Email("  TEST@MAIL.COM  ")
print(e.address)
