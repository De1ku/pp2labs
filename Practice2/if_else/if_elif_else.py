# сравнение
a = int(input())
b = int(input())

print(f"a = {a} ; b = {b}")

if a > b:
    print("a>b")
elif b > a:
    print("b>a")
else:
    print("a = b")

#Оценка
score = 78

if (score >= 90):
    print("A")
elif (score >= 75):
    print("B")
elif (score >= 60):
    print("C")
else:
    print("F")

#доступ по возрасту
age = 16

if (age >= 18):
    print("Доступ есть")

elif (age >= 16):
    print("Ограниченный доступ")

else:
    print("Доступ запрещен")


#что надеть по температуре
temp = 5
if (temp >= 25):
    print("Футболка")

elif (temp >= 10):
    print("Легкая куртка")

elif (temp >= 0):
    print("Теплая куртка")

else:
    print("Очень тепло одеться (ШАПКА!!!)")


 # "авторизация"
credentials = {"admin": 1234}
login = "admin"
password = "1234"
if login not in credentials.keys():
    print("Неверный логин")

elif password != credentials[login]:
    print("Неверный пароль")

else:
    print("welcome back!")