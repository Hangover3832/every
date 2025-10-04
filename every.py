from time import monotonic
from typing import Callable, Any


class Every:
    """A simple class for executing a function at regular intervals.
    The Every class provides a mechanism to control periodic execution of a function,
    allowing for flexible timing control and parameter passing.
    Args:
        interval (float): The time interval between executions in seconds
        do (Callable): The function to be executed periodically
        time_func (Callable, optional): Function that returns a time in [s]. Defaults to monotonic.
        **kwargs: Additional keyword arguments to pass to the do function
    Attributes:
        interval (float): The time interval between executions (readable/writable)
        time_func (Callable): Function used to get current time
        do (Callable): The function to be executed
        kwargs (dict): Stored keyword arguments for the do() function
        next_time (float): Timestamp for next scheduled execution
    Methods:
        __call__(**kwargs): Check if it's time to execute and run the function if so
    Returns:
        tuple[bool, Any]: A tuple containing:
            - bool: True if function was executed, False otherwise
            - Any: Return value from do() if executed, None otherwise
    Example:
        >>> def print_hello():
        ...     print("Hello")
        >>> every_sec = Every(1.0, print_hello)
        >>> executed, result = every_sec()  # Will execute if 1 second has passed
    """

    def __init__(self, interval: float, do: Callable, *, time_func: Callable = monotonic, **kwargs: Any) -> None:
        self._interval = interval
        self.time_func = time_func
        self.do = do
        self.kwargs = dict(kwargs)
        self.next_time = time_func() + interval


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
        if self.time_func() >= self.next_time:
            self.next_time += self._interval # keep time interval consistent 
            merged_kwargs = {**self.kwargs, **kwargs}
            result = self.do(**merged_kwargs)
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
        self.next_time = self.time_func() + value
