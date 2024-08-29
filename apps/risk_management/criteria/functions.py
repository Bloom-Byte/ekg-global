import typing
import attrs
from dataclasses import dataclass
from talib import abstract as talib_abstract_api, get_functions as get_talib_functions

from helpers.typing_utils import SupportsRichComparison
from .exceptions import UnsupportedFunction, FunctionSpecValidationError


T = typing.TypeVar("T")
R = typing.TypeVar("R")

TALIB_FUNCTIONS = get_talib_functions()


@attrs.define(auto_attribs=True)
class BaseKwargsType:
    """Specifies the schema for the keywords that a TA-LIB function accepts"""

    pass


def KwargsType(name: str, attributes: typing.Dict[str, typing.Any], **kwargs) -> typing.Type[BaseKwargsType]:
    """
    Make a new class that specifies the schema for the keywords that a TA-LIB function accepts

    By default, the new class is a attrs class with `auto_attribs=True` and `slots=True`
    and is a subclass of `BaseKwargsType`

    :param name: The name of the new class
    :param attributes: The attributes of the new class. 
        A mapping of attribute names to an `attrs.field` or `attrs.ib` instance
    :param kwargs: Additional keyword arguments to pass to `attrs.make_class`
    :return: subclass of `BaseKwargsType` with defined attributes
    """
    kwargs.setdefault("auto_attribs", True)
    kwargs.setdefault("slots", True)
    kwargs.setdefault("bases", (BaseKwargsType,))
    return attrs.make_class(
        name, attributes, **kwargs
    )


@dataclass(slots=True, frozen=True, repr=False)
class FunctionSpec:
    """Specifications for evaluating a TA-LIB function on an object"""

    name: str
    """The name or alias of the TA-LIB function this specification is for. This will be used to lookup the TA-LIB function evaluator"""
    kwargs: typing.Mapping[str, typing.Any]
    """Keyword arguments for the TA-LIB function. Will be utilized when evalating the functio on an object"""

    def __repr__(self) -> str:
        return f"{self.name}({', '.join([f'{k}={v}' for k, v in self.kwargs.items()])})"

    def __str__(self) -> str:
        return self.name


class ArgEvaluator(typing.Generic[T, R]):
    """
    Wraps a function that will later be used to evaluate an argument
    to be passed to a talib function.
    """

    def __init__(
        self,
        eval_func: typing.Callable[[T, FunctionSpec], typing.Any],
        name: str = None,
    ):
        """
        Create a new argument evaluator

        :param eval_func: The function that will be used to evaluate the argument
            This function should take an object and a `FunctionSpec` and return a value
        :param name: The name of the argument evaluator
        """
        self.eval_func = eval_func
        self.name = name

    def __call__(self, o: T, /, function: FunctionSpec) -> R:
        return self.eval_func(o, function)


FunctionAlias = str
"""The name or alias of the TA-LIB function in the functions registry"""
FunctionEvaluator = typing.Callable[[T, FunctionSpec], SupportsRichComparison]
"""Performs the evaluation of a TA-LIB function on an object using the provided `FunctionSpec`. 
Returns a value that supports rich comparison"""


class FunctionData(typing.TypedDict):
    evaluator: FunctionEvaluator
    """The function that will be used to evaluate the TA-LIB function"""
    kwargs_type: typing.Optional[typing.Type[BaseKwargsType]]
    """
    The schema for the keyword arguments that the TA-LIB function accepts.

    Setting this to None means the function does not accept any keyword arguments
    """


FUNCTIONS_REGISTRY: typing.Dict[FunctionAlias, FunctionData] = {}


def make_function_spec(name: str, **kwargs) -> FunctionSpec:
    """
    Helper function to create a TA-LIB function specification

    :param name: The name or alias of the function
    :param kwargs: Keyword arguments for the TA-LIB function.
        These should match the schema of the function's `kwargs_type`
        in the functions registry
    :return: A new function specification
    """
    if name not in FUNCTIONS_REGISTRY:
        raise UnsupportedFunction(f"Unsupported function: {name}")

    if kwargs:
        kwargs_type = FUNCTIONS_REGISTRY[name].get("kwargs_type", None)
        if not kwargs_type:
            raise FunctionSpecValidationError(
                f"Function {name} does not have a kwargs_type defined"
                " and cannot accept keyword arguments"
            )

        kwargs = attrs.asdict(kwargs_type(**kwargs))
    return FunctionSpec(name, kwargs)


def evaluator(
    func: typing.Optional[FunctionEvaluator] = None,
    *,
    alias: typing.Optional[str] = None,
    kwargs_type: typing.Optional[typing.Type[BaseKwargsType]] = None,
):
    """
    Register a TA-LIB function evaluator

    :param func: The function that will be used to evaluate the TA-LIB function
    :param alias: The alias to use for the TA-LIB function in the functions registry
    :param kwargs_type: The schema for the keyword arguments that the TA-LIB function accepts.
        Setting this to None means the function does not accept any keyword arguments.
    :return: The TA-LIB function evaluator
    """
    if kwargs_type and not issubclass(kwargs_type, BaseKwargsType):
        raise ValueError("kwargs_type must be a subclass of BaseKwargsType")

    def _decorator(func: FunctionEvaluator):
        FUNCTIONS_REGISTRY[alias or func.__name__] = {
            "evaluator": func,
            "kwargs_type": kwargs_type,
        }
        return func

    if func is None:
        return _decorator
    return _decorator(func)


def build_evaluator(
    talib_target: str,
    arg_evaluators: typing.List[ArgEvaluator],
):
    """
    Builds a generic TA-LIB function evaluator, assuming that the target TA-LIB function
    returns only one value.

    If you need a custom evaluator, consider writing one from scratch or write a wrapper
    arround the evaluator returned by this function.

    :param talib_target: The actual name of the TA-LIB function in the `ta-lib` package
    :param arg_evaluators: A list of argument evaluators to be used to evaluate
        the arguments to that will be passed to the TA-LIB function.
        The order of the evaluators in the list should match the order in which
        the arguments are expected by the TA-LIB function.
    :return: A new TA-LIB function evaluator
    """
    if talib_target not in TALIB_FUNCTIONS:
        raise ValueError(f"Invalid TA-LIB function: {talib_target}")
    if not arg_evaluators:
        raise ValueError("At least one argument evaluator is required")

    def _evaluator(o: T, /, spec: FunctionSpec) -> SupportsRichComparison:
        args = [evaluator(o, spec) for evaluator in arg_evaluators]
        return talib_abstract_api.Function(talib_target)(*args, **spec.kwargs)

    return _evaluator


def new_evaluator(
    talib_target: str,
    *,
    arg_evaluators: typing.List[ArgEvaluator],
    kwargs_type: typing.Optional[typing.Type[BaseKwargsType]] = None,
    alias: typing.Optional[str] = None,
) -> FunctionEvaluator:
    """
    Builds and registers a new (generic) TA-LIB function evaluator,
    assuming that the target TA-LIB function returns only one value.

    Write a custom evaluator if the TA-LIB function returns multiple values or
    you need to perform additional pre/post-processing.
    Then register it using the `evaluator` decorator.

    :param talib_target: The actual name of the TA-LIB function in the `ta-lib` package
    :param arg_evaluators: A list of argument evaluators to be used to evaluate
        the arguments to that will be passed to the TA-LIB function.
        The order of the evaluators in the list should match the order in which
        the arguments are expected by the TA-LIB function.
    :param kwargs_type: The schema for the keyword arguments that the TA-LIB function accepts.
        Setting this to None means the function does not accept any keyword arguments.
    :param alias: The alias to use for the TA-LIB function in the functions registry
    :return: The TA-LIB function evaluator
    """
    return evaluator(
        build_evaluator(talib_target, arg_evaluators),
        alias=alias,
        kwargs_type=kwargs_type,
    )


def evaluate(o: T, /, spec: FunctionSpec) -> SupportsRichComparison:
    """
    Run a TA-LIB function evaluation on an object

    :param o: The object to evaluate the function on
    :param spec: The function specification to use for the evaluation
    :return: The result of the function evaluation
    :raises UnsupportedFunction: If the function defined in the specification is not supported
    """
    try:
        evaluator = FUNCTIONS_REGISTRY[spec.name]["evaluator"]
    except KeyError as exc:
        raise UnsupportedFunction(f"Unsupported function: {spec.name}") from exc
    return evaluator(o, spec)
