# 1
class Dog:
    pass

d = Dog()
print(d)


# 2 class, adding an attribute
class Student:
    pass

s = Student()
s.name = "Aruzhan"
s.grade = 95
print(s.name, s.grade)


# 3 using method
class Counter:
    def inc(self):
        if not hasattr(self, "value"):
            self.value = 0
        self.value += 1

c = Counter()
c.inc()
c.inc()
print(c.value)


# 4 method using class attribute
class BankAccount:
    def deposit(self, amount):
        if not hasattr(self, "balance"):
            self.balance = 0
        self.balance += amount

acc = BankAccount()
acc.deposit(1000)
acc.deposit(250)
print(acc.balance)


# 5 different objects with same class
class Lamp:
    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

a = Lamp()
b = Lamp()
a.turn_on()
b.turn_off()
print(a.is_on, b.is_on)
