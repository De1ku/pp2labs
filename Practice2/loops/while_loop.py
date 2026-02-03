i = 1
while i <= 5: #счетчик
    print(i)
    i += 1

n = 5
while n > 0: #обратный
    print(n)
    n-=1

n = 10
i = 1
s = 0
while i <= n: #сумма чисел 1..n
    s += i
    i += 1
print(s)

while True: #ввод пока не введут q
    text = input("Type something (q to quit)")
    if text == "q":
        break
    print(f"You typed: {text}")

x = 1
while x % 7 != 0: #поиск первого числа, кратного 7
    x += 1
print(f"First multiple of 7: {x}")
