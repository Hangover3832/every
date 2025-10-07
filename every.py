"""
executing a function at regular intervals
Author: AlexL
License: MIT
Github: https://github.com/Hangover3832/every
"""

from time import monotonic
from typing import Callable, Any
from functools import wraps


class Every:
    """A simple class for executing a function at regular intervals.
    The Every class provides a mechanism to control periodic execution of a function,
    allowing for flexible timing control and parameter passing.
    Args:
        interval (float): The time interval in seconds between function executions.
        execute_immediately (bool): If True, the function will be executed immediately upon the first call.
    Attributes:
        interval (float): The time interval between executions (readable/writable)
        time_func (Callable): The function used to get the current time (default is monotonic)
    Methods:
        do(action: Callable, **kwargs) -> 'Every': Sets the function to be executed and optional keyword arguments.
        using(time_func: Callable) -> 'Every': Sets a custom time function (default is monotonic).
        Note: When calling the instance, any keyword arguments passed will override those set in do().
    Returns:
        tuple[bool, Any]: A tuple containing:
            - bool: True if function was executed, False otherwise
            - Any: Return value from do() if executed, None otherwise
    Example:
        icluded in Demo() function below
    """

    @classmethod # decorator for class Every
    def every(cls, interval: float, *, 
            timer_function: Callable = monotonic, 
            execute_immadeately: bool = False, **kwargs: Any
            ) -> Callable:
        """Decorator to create an Every instance and set the kwargs.
        Args:
            interval (float): The time interval in seconds between function executions.
            **kwargs: Additional keyword arguments to pass to the function.
        """
        @wraps(cls)
        def wrapper(func: Callable) -> Every:
            return cls(interval, execute_immediately=execute_immadeately).do(func, **kwargs).using(timer_function)
        
        return wrapper


    def __init__(self, interval: float, *, execute_immediately: bool = False) -> None:
        if interval <= 0:
            raise ValueError("Interval must be positive")

        self._interval = interval
        self._time_func = monotonic
        self._action = None
        self._kwargs = {}
        self._next_time = self._time_func() if execute_immediately else self._time_func() + interval


    def do(self, action: Callable, **kwargs: Any) -> 'Every':
        """Sets the function to be executed and optional keyword arguments."""
        self._kwargs.update(kwargs)
        self._action = action
        return self
 

    def using(self, time_func: Callable) -> 'Every':
        """Sets a custom time function (default is monotonic)."""
        self._time_func = time_func
        return self


    def reset(self) -> None:
        """Reset the timer to start from current moment."""
        self._next_time = self._time_func() + self._interval


    @property
    def time_remaining(self) -> float:
        """Get the time remaining until next execution."""
        return max(0.0, self._next_time - self._time_func())


    def __call__(self, **kwargs: Any) -> tuple[bool, Any]:
        """
        Checks if the scheduled interval has passed and executes the stored function if so.

        Args:
            **kwargs: Additional keyword arguments to pass to the stored function.

        Returns:
            tuple[bool, Any]: A tuple containing:
                - bool: True if the function was executed, False otherwise.
                - Any: The return value from the function if executed, or None otherwise.
        """
        if self._action is None:
            raise ValueError("No action has been set. Use the 'do' method to set a function to execute.")
        
        if self._time_func() >= self._next_time:
            self._next_time += self._interval # keep time interval consistent 
            merged_kwargs = {**self._kwargs, **kwargs}
            result = self._action(**merged_kwargs)
            return True, result
        return False, None


    @property
    def interval(self) -> float:
        return self._interval
    
    @interval.setter
    def interval(self, value: float) -> None:
        """
        Sets a new interval value and resets the next execution time.

        Args:
            value (float): The new time interval in seconds.
        """
        if value <= 0:
            raise ValueError("Interval must be positive")
        self._interval = value
        self._next_time = self._time_func() + value



def Demo():
    from time import sleep, perf_counter
    # from every import Every

    # simplest usage:
    @Every.every(5.0)
    def VerySimple():
        print("A very simple function has been executed")


    # decorator usage:
    @Every.every(2.71, param1=10, param2=20, timer_function=monotonic, execute_immadeately=True) # static param1 and param2, execute on first call
    def MyFunction1(param1, param2, param3): # param3 is required dynamically when calling the function
        print(f"Function executed with {param1=}, {param2=} and {param3=}")
        return param1 + param2 + param3
    
    
    # direct usage:
    def MyFunction2(a, b):
        print(f"MyFunction2 executed with {a=} and {b=}")
        return a * b
    my_function2_timer = Every(3.14).do(MyFunction2, a=5, b=6).using(perf_counter) # static parameter a and b & use different timer

    while True:
        VerySimple()

        executed, res = MyFunction1(param3=30) # Add param3 dynamically
        if executed:
            print(f"Function1 returned: {res}, function2 time remaining: {my_function2_timer.time_remaining:.2f}s")

        executed, res = my_function2_timer(b=2) # Override b dynamically
        if executed:
            print(f"Function2 returned: {res}, function1 time remaining: {MyFunction1.time_remaining:.2f}s")

        sleep(0.01)


if __name__ == "__main__":
    Demo()
