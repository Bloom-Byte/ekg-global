import typing
from dataclasses import dataclass

from helpers.typing_utils import SupportsRichComparison
from .exceptions import UnsupportedFunction



@dataclass(slots=True, repr=False)
class Function:
    name: str
    options: typing.Mapping[str, typing.Any]

    def __repr__(self) -> str:
        return (
            f"{self.name}({', '.join([f'{k}={v}' for k, v in self.options.items()])})"
        )

    def __str__(self) -> str:
        return self.name


T = typing.TypeVar("T")
FunctionEvaluator = typing.Callable[[T, Function], SupportsRichComparison]

FUNCTION_EVALUATORS: typing.Dict[str, FunctionEvaluator] = {}


def validate_function(func: Function) -> Function:
    if func.name not in FUNCTION_EVALUATORS:
        raise UnsupportedFunction(f"Unsupported function: {func.name}")
    return func


def make_function(name: str, **options) -> Function:
    kwds = {"name": name, "options": options}
    return Function(**kwds)


def function_evaluator(
    evaluator: typing.Optional[FunctionEvaluator] = None,
    /,
    *,
    name: typing.Optional[str] = None,
):
    def _decorator(evaluator: FunctionEvaluator) -> FunctionEvaluator:
        nonlocal name
        global FUNCTION_EVALUATORS

        name = name or evaluator.__name__
        FUNCTION_EVALUATORS[name] = evaluator
        return evaluator

    if evaluator is None:
        return _decorator
    return _decorator(evaluator)


def evaluate_function(o: T, /, func: Function) -> SupportsRichComparison:
    try:
        func_evaluator = FUNCTION_EVALUATORS[func.name]
    except KeyError as exc:
        raise UnsupportedFunction(f"Unsupported function: {func.name}") from exc
    return func_evaluator(o, func)

