from dataclasses import dataclass
from enum import StrEnum

import pytest

from mp_fsm.statemachine import (BaseCallback, BaseGuard, BaseStateMachine,
                                 BaseTransition, StateAware, T)


class MyStates(StrEnum):
    START = "start"
    STOP = "stop"


@dataclass
class MyObject(StateAware): ...


class MyGuard(BaseGuard[MyObject]):
    async def __call__(self, obj: T) -> bool:
        return True


class MyCallback(BaseCallback[MyObject]):
    async def __call__(self, obj: T) -> None:
        print("HELLO")


class MyTransition(BaseTransition[MyObject]):
    @property
    def from_states(self) -> list[str]:
        return [MyStates.START]

    @property
    def to_state(self) -> str:
        return MyStates.STOP

    @property
    def guards(self) -> list[BaseGuard[MyObject]]:
        return [MyGuard()]

    @property
    def before(self) -> list[BaseCallback[MyObject]]:
        return [MyCallback()]

    @property
    def after(self) -> list[BaseCallback[MyObject]]:
        return [MyCallback()]


class MyStateMachine(BaseStateMachine[MyObject]):
    @property
    def _states(self) -> list[str]:
        return [state for state in MyStates]

    @property
    def _transitions(self) -> dict[str, BaseTransition[MyObject]]:
        return {"my_transition": MyTransition()}


@pytest.mark.asyncio
async def test_statemachine() -> None:
    my_object = MyObject()
    my_object.state = MyStates.START

    state_machine = MyStateMachine()
    await state_machine.transition(my_object, "my_transition")

    assert my_object.state == MyStates.STOP
