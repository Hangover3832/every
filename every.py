from time import monotonic
from typing import Callable, Any


class Every:
    """A simple class for executing a function at regular intervals.
    The Every class provides a mechanism to control periodic execution of a function,
    allowing for flexible timing control and parameter passing.
    Args:
        interval (float): The time interval in seconds between function executions.
    Attributes:
        interval (float): The time interval between executions (readable/writable)
        time_func (Callable): The function used to get the current time (default is monotonic)
    Methods:
        do(action: Callable, **kwargs) -> 'Every': Sets the function to be executed and optional keyword arguments.
        using(time_func: Callable) -> 'Every': Sets a custom time function (default is monotonic).
        process(**kwargs) -> tuple[bool, Any]: Checks if the interval has passed and executes the function if so.
    Returns:
        tuple[bool, Any]: A tuple containing:
            - bool: True if function was executed, False otherwise
            - Any: Return value from do() if executed, None otherwise
    Example:
        >>> import time
        >>> from every import Every
        >>> def my_function(param1, param2):
        ...     print(f"Function executed with {param1} and {param2}")
        ...     return param1 + param2
        ...
        >>> every = Every(2.0).do(my_function, param1=10, param2=20)
        >>> while True:
        ...     executed, result = every.process()
        ...     if executed:
        ...         print(f"Function returned: {result}")
        ...     time.sleep(0.5)  # Simulate doing other work
    """

    def __init__(self, interval: float) -> None:
        self._interval = interval
        self._time_func = monotonic
        self._action = None
        self._kwargs = {}
        self._next_time = self._time_func() + interval


    def do(self, action: Callable, **kwargs: Any) -> 'Every':
        self._action = action
        self._kwargs.update(kwargs)
        return self


    def using(self, time_func: Callable) -> 'Every':
        self._time_func = time_func
        return self


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
        self._interval = value
        self._next_time = self._time_func() + value
