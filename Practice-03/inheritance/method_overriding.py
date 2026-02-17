# 1
class Animal:
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "meow"

print(Animal().speak())
print(Cat().speak())


# 2 polymorfism
class Shape:
    def area(self):
        raise NotImplementedError

class Square(Shape):
    def __init__(self, a):
        self.a = a
    def area(self):
        return self.a * self.a

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def area(self):
        return self.w * self.h

shapes = [Square(3), Rectangle(2, 5)]
print([s.area() for s in shapes])


# 3 overriding and expanding the method
class Logger:
    def log(self, msg):
        return f"[LOG] {msg}"

class FileLogger(Logger):
    def log(self, msg):
        base = super().log(msg)
        return base + " -> written to file"

print(FileLogger().log("hello"))


# 4
class User:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"User(name={self.name})"

print(User("Dana"))


# 5 overriding but same method signature
class Base:
    def calc(self, x, y):
        return x + y

class Child(Base):
    def calc(self, x, y):
        return x * y

b = Base()
c = Child()
print(b.calc(3, 4), c.calc(3, 4))
