colors = ["red", "green", "blue"]
for c in colors: #перебор и вывод массива
    print(c)


for i in range(5):
    print(i)



nums = [1, 2, 3, 4]
s = 0
for x in nums: #сумма эл-ов
    s += x
print(s)



word = "hello"
for ch in word: #вывод посимвольно
    print(ch)



scores = {"Ann": 5, "Bob": 3}
for name, score in scores.items(): #перебор и вывод
    print(name, score)