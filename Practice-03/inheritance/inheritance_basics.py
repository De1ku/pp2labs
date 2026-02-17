# 1
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    pass

d = Dog()
print(d.speak())


# 2
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, uni):
        super().__init__(name)
        self.uni = uni

s = Student("Ali", "KBTU")
print(s.name, s.uni)


# 3 new method in child
class Vehicle:
    def move(self):
        return "moving"

class Car(Vehicle):
    def honk(self):
        return "beep!"

c = Car()
print(c.move(), c.honk())


# 4 isinstance
print(isinstance(c, Car))
print(isinstance(c, Vehicle))


# 5 chain inheritance
class A:
    def f(self):
        return "A"

class B(A):
    pass

class C(B):
    pass

x = C()
print(x.f())
