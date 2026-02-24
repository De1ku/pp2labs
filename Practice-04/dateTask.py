import datetime
from time import sleep


def task_1() -> None:
    print(datetime.datetime.now().date() - datetime.timedelta(days=5))

def task_2() -> None:
    one_day = datetime.timedelta(days=1)
    print(datetime.datetime.now().date() - one_day)
    print(datetime.datetime.now().date())
    print(datetime.datetime.now().date() + one_day)

def task_3() -> None:
    print(datetime.datetime.now().replace(microsecond=0))

def task_4(d1: datetime, d2:datetime) -> None:
    print(abs((d1 - d2).total_seconds()))


if __name__ == "__main__":
    task_1()
    task_2()
    task_3()
    a = datetime.datetime.now()
    sleep(1)
    task_4(a, datetime.datetime.now())