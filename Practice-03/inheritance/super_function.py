# 1 super() in __init__
class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):
    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = salary

e = Employee("Timur", 500000)
print(e.name, e.salary)


# 2 super() in method
class Printer:
    def print_line(self, text):
        return text

class FancyPrinter(Printer):
    def print_line(self, text):
        return ">>> " + super().print_line(text) + " <<<"

fp = FancyPrinter()
print(fp.print_line("hello"))


# 3 super() in chain inheritance
class A:
    def f(self):
        return "A"

class B(A):
    def f(self):
        return super().f() + " -> B"

class C(B):
    def f(self):
        return super().f() + " -> C"

print(C().f())


# 4 super() with overriding
class Account:
    def __init__(self, balance):
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount

class SafeAccount(Account):
    def deposit(self, amount):
        if amount <= 0:
            return
        super().deposit(amount)

a = SafeAccount(100)
a.deposit(-5)
a.deposit(20)
print(a.balance)


# 5
class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def area(self):
        return self.w * self.h

class Square(Rectangle):
    def __init__(self, a):
        super().__init__(a, a)

sq = Square(6)
print(sq.area())
