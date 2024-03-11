# Modern Python Finite State Machine
This package provides a simple means
of defining [Finite State Machines](https://en.wikipedia.org/wiki/Finite-state_machine).

It is fully typed and works asynchronously using Python's [asyncio](https://docs.python.org/3/library/asyncio.html).

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
