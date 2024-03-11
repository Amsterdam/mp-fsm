from dataclasses import dataclass
from enum import StrEnum

import pytest
from pytest_mock import MockerFixture

from mp_fsm.statemachine import (
    BaseCallback,
    BaseGuard,
    BaseStateMachine,
    BaseTransition,
    StateAware,
)


class MyStates(StrEnum):
    START = "start"
    STOP = "stop"


@dataclass
class MyObject(StateAware): ...


@pytest.mark.asyncio
async def test_statemachine(mocker: MockerFixture) -> None:
    class MyGuard(BaseGuard[MyObject]):
        async def __call__(self, obj: MyObject) -> bool:
            return True

    guard_spy = mocker.spy(MyGuard, "__call__")
    guard = MyGuard()

    class MyCallback(BaseCallback[MyObject]):
        async def __call__(self, obj: MyObject) -> None:
            print("HELLO")

    callback_spy = mocker.spy(MyCallback, "__call__")
    callback = MyCallback()

    class MyTransition(BaseTransition[MyObject]):
        @property
        def from_states(self) -> list[str]:
            return [MyStates.START]

        @property
        def to_state(self) -> str:
            return MyStates.STOP

        @property
        def guards(self) -> list[BaseGuard[MyObject]]:
            return [guard]

        @property
        def before(self) -> list[BaseCallback[MyObject]]:
            return [callback]

        @property
        def after(self) -> list[BaseCallback[MyObject]]:
            return [callback]

    class MyStateMachine(BaseStateMachine[MyObject]):
        @property
        def _transitions(self) -> dict[str, BaseTransition[MyObject]]:
            return {"my_transition": MyTransition()}

    my_object = MyObject()
    my_object.state = MyStates.START

    state_machine = MyStateMachine()
    await state_machine.transition(my_object, "my_transition")

    assert my_object.state == MyStates.STOP
    assert guard_spy.call_count == 1
    assert callback_spy.call_count == 2
