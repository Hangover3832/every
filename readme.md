# Every

A lightweight Python utility class for executing functions at regular intervals with precise timing control.

## Overview

The `Every` class provides a simple and efficient way to execute functions periodically without the complexity of threading or event loops. It's particularly useful for scenarios where you need to perform actions at regular intervals, such as:

- Sensor reading
- Status updates
- Periodic data logging
- Timed events in games or simulations

## Features

- Simple and intuitive API
- Precise timing control using monotonic time
- Flexible parameter passing
- No external dependencies
- Customizable time function
- Thread-safe execution

## Installation

Simply copy the `every.py` file into your project directory.

## Usage

### Basic Example

```python
from every import Every

def print_hello():
    print("Hello")

# Create an Every instance that runs every 1 second
every_sec = Every(1.0).do(print_hello)

# In your main loop:
executed, result = every_sec()  # Will execute if 1 second has passed
```

### With Parameters

```python
def greet(name):
    print(f"Hello, {name}!")

# Create with default parameters
greeter = Every(2.0).do(greet, name="World")

# Override parameters on call
greeter(name="Alice")  # Will use "Alice" instead of "World"
```

### Custom Timing Function

```python
from time import time

# Use regular time() instead of monotonic()
custom_timer = Every(1.0).do(print_hello).using(time)

# Can also combine with parameters
custom_timer = Every(1.0).do(greet, name="World").using(time)
```

### Use as a decorator
```python
@Every.every(5.0, greets="Holla", timer_function=monotonic, execute_immadeately=True)
def greet(greets, name):
    print(f"{greets}, {name}!")

while True:
    greet(name="Alex") # the parameter 'greets' got past in the decorator
    ...
```

## API Reference

### Class: Every

#### Constructor

```python
Every(interval: float)
```

- `interval`: Time between executions in seconds
- `timer_function`: Custom timer function, defaults to `time.monotonic`
- `execute_immadeately`: Executes the function immediately upon the first call

#### Methods

- `do(action: Callable, **kwargs: Any) -> Every`: Set the function to execute and its arguments
  - Returns: The Every instance for method chaining

- `using(time_func: Callable) -> Every`: Optional - Set the time function (defaults to `monotonic`)
  - Returns: The Every instance for method chaining

- `__call__(**kwargs)`: Check if it's time to execute and run the function
  - Returns: `tuple[bool, Any]`
    - `bool`: Whether the function was executed
    - `Any`: Return value from the function (if executed)

- `reset()`: Resets the timer to start from current moment

#### Properties

- `interval`: Get/set the time interval between executions
- `time_remaining`: Get the remaining time until the next execution (read only)

## Notes

- The class uses `time.monotonic()` by default for precise and reliable timing
- Changing the interval resets the next execution time
- The class maintains consistent intervals by adding the interval to the last scheduled time
- Additional keyword arguments can be passed both during initialization and execution
- pylance seems to have some troubles with type checking the decorated functions

## License

This project is open source and available under the MIT License.