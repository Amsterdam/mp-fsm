from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T", bound="StateAware")


class StateMachineException(Exception): ...


class WrongStateException(StateMachineException): ...


class GuardException(StateMachineException): ...


class TransitionNotFoundException(StateMachineException): ...


class StateAware:
    state: str


class BaseGuard(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    async def __call__(self, obj: T) -> bool: ...


class BaseCallback(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    async def __call__(self, obj: T) -> None: ...


class BaseTransition(Generic[T], metaclass=ABCMeta):
    @property
    @abstractmethod
    def from_states(self) -> list[str]: ...

    @property
    @abstractmethod
    def to_state(self) -> str: ...

    @property
    @abstractmethod
    def guards(self) -> list[BaseGuard[T]]: ...

    @property
    @abstractmethod
    def before(self) -> list[BaseCallback[T]]: ...

    @property
    @abstractmethod
    def after(self) -> list[BaseCallback[T]]: ...


class BaseStateMachine(Generic[T], metaclass=ABCMeta):
    @property
    @abstractmethod
    def _states(self) -> list[str]: ...

    @property
    @abstractmethod
    def _transitions(self) -> dict[str, BaseTransition[T]]: ...

    async def transition(self, state_aware: T, transition_name: str) -> None:
        transition = self._transitions.get(transition_name)
        if transition is None:
            raise TransitionNotFoundException(transition_name)

        if state_aware.state not in transition.from_states:
            raise WrongStateException()

        for guard in transition.guards:
            if not await guard(state_aware):
                raise GuardException()

        for before in transition.before:
            await before(state_aware)

        state_aware.state = transition.to_state

        for after in transition.after:
            await after(state_aware)
