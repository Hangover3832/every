from every import Every
from time import sleep, perf_counter, monotonic
from random import random


def simple_interval():

    counter = 0
    def do_print(char:str, end_at:int) -> bool:
        nonlocal counter
        print(char, end='', flush=True)
        counter += 1
        return counter > end_at

    interval_timer = Every(0.2).do(do_print).among(end_at=10)
    while True:
        if interval_timer('#') and interval_timer.result:
            break
        sleep(0.001)

    print("Simple interval")


def decorator_interval():

    #Decoreator usage:
    counter = 0

    @Every.every(0.2)
    def do_print(char:str):
        print(char, end='', flush=True)
        return "Decorator usage"

    while True:
        if do_print('@'):
            counter += 1
            if counter > 15:
                break
        sleep(0.001)

    print(do_print.result)


def timed_loop():

    counter = 0
    my_loop = Every(5)

    def loop_funtion(message:str, stop_at:int = 0):
        nonlocal counter
        counter += 1
        if counter % 100000 == 0:
            print(f"{message=}, {counter=}, time remaining: {my_loop.time_remaining}")
        if stop_at > 0 and counter >= stop_at:
            my_loop.break_loop()

    my_loop.do(loop_funtion).among(stop_at=1_000_000).do_while("#Timed loop")
    print()


def decorator_loop():

    counter = 0

    @Every.While(2, message="@Decorator loop")
    def loop_funtion(message:str):
        nonlocal counter
        counter += 1
        if counter % 100000 == 0:
            print(f"{message=}, {counter=}")
        return "End of decorated timed loop"
    
    print(loop_funtion.result)


def combined_run():

    @Every.While(30)
    def run():
        simple_interval()
        decorator_interval()
        timed_loop()
        decorator_loop()


if __name__ == "__main__":
    combined_run()
