#авторизован ли
is_logged_in = True

if is_logged_in:
    print("Welcome back!")
else:
    print("You need to log in")

#четность / нечетность
a = 16

if (a%2 == 0):
    print("a is even")
else:
    print("a is odd")

#минимальное из двух
a = 10
b = 3

if a<b:
    print(f"min: {a}")
else:
    print(f"min: {b}")


#доступ по возрасту
age = 18

if age >= 18:
    print("Welcome!")
else:
    print("You're not allowed")


#0 или нет?
why = 0

if why:
    print("why variable is some int")
else:
    print("ahh why var is just a zero")

