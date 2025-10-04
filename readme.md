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
every_sec = Every(1.0, print_hello)

# In your main loop:
executed, result = every_sec()  # Will execute if 1 second has passed
```

### With Parameters

```python
def greet(name):
    print(f"Hello, {name}!")

# Create with default parameters
greeter = Every(2.0, greet, name="World")

# Override parameters on call
greeter(name="Alice")  # Will use "Alice" instead of "World"
```

### Custom Timing Function

```python
from time import time

# Use regular time() instead of monotonic()
custom_timer = Every(1.0, print_hello, time_func=time)
```

## API Reference

### Class: Every

#### Constructor

```python
Every(interval: float, do: Callable, *, time_func: Callable = monotonic, **kwargs: Any)
```

- `interval`: Time between executions in seconds
- `do`: Function to execute periodically
- `time_func`: Optional function to get current time (defaults to `time.monotonic`)
- `**kwargs`: Default arguments to pass to `do`

#### Methods

- `__call__(**kwargs)`: Check if it's time to execute and run the function
  - Returns: `tuple[bool, Any]`
    - `bool`: Whether the function was executed
    - `Any`: Return value from the function (if executed)

#### Properties

- `interval`: Get/set the time interval between executions

## Notes

- The class uses `time.monotonic()` by default for precise and reliable timing
- Changing the interval resets the next execution time
- The class maintains consistent intervals by adding the interval to the last scheduled time
- Additional keyword arguments can be passed both during initialization and execution

## License

This project is open source and available under the MIT License.