# Modern Python Finite State Machine
This package provides a simple means
of defining [Finite State Machines](https://en.wikipedia.org/wiki/Finite-state_machine).

# Motivation
The landscape of available Finite State Machine libraries in Python is vast. However, many existing solutions suffer from various drawbacks that don't align well with modern development practices and specific requirements we have for projects within the Gemeente Amsterdam. Some of the common issues encountered with existing FSM libraries include:

- Lack of maintenance over extended periods, leading to potential compatibility and reliability concerns.
- Requirements to implement logic directly within the database model, which conflicts with the preferred usage of dataclasses in a Domain-Driven Design (DDD) context.
- Absence of strong typing support, while the project enforces strict typing using tools like mypy.
- Inadequate asynchronous support, hindering integration with asyncio-based applications.
- Reliance on decorators, making it challenging to implement with an abstraction layer in between.
- Combinations of the above issues, further complicating adoption and maintenance efforts.

# Features
Fully typed: This package is designed with robust type annotations throughout, ensuring type safety and compatibility with type-checking tools like mypy.
Asynchronous support: Utilizes Python's asyncio for asynchronous execution, enabling seamless integration with asyncio-based applications.
Dataclass compatibility: Works seamlessly with Python's dataclasses, aligning with modern Pythonic practices and Domain-Driven Design (DDD) principles.
Customizable transitions: Define transitions between states flexibly, allowing for complex state transition logic with ease.
Guard conditions: Implement guards to enforce conditions that must be met for a state transition to occur, enhancing control over state transitions.
Callbacks: Execute custom code before or after a state transition, facilitating integration with existing systems and workflows.

A simple example of how to implement a state machine using this package:
```python
import asyncio
from dataclasses import dataclass
from enum import StrEnum

from mp_fsm.statemachine import BaseStateMachine, BaseTransition, StateAware


class MyStates(StrEnum):
    START = "start"
    STOP = "stop"


class MyTransitions(StrEnum):
    MY_TRANSITION = "my_transition"


@dataclass
class MyObject(StateAware): ...


class MyTransition(BaseTransition[MyObject]):
    @property
    def from_states(self) -> list[str]:
        return [MyStates.START]

    @property
    def to_state(self) -> str:
        return MyStates.STOP

class MyStateMachine(BaseStateMachine[MyObject]):
    @property
    def _transitions(self) -> dict[str, BaseTransition[MyObject]]:
        return {MyTransitions.MY_TRANSITION: MyTransition()}


async def do_it() -> None:
    my_object = MyObject()
    my_object.state = MyStates.START
    
    state_machine = MyStateMachine()
    
    await state_machine.transition(my_object, MyTransitions.MY_TRANSITION)
    
    print(my_object.state) # Prints: "stop"

asyncio.run(do_it())
```

It's also possible to implement guards to prevent a state transition under certain conditions,
and callbacks that can be executed right before or right after a transition.
Please refer to [the tests](tests/test_statemachine.py) for complete examples on how to do that.
