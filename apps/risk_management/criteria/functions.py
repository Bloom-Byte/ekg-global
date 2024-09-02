import functools
import typing
import numpy as np
import attrs
from concurrent.futures import ThreadPoolExecutor
import talib
import copy
from talib import get_functions as get_talib_functions

from helpers.typing_utils import SupportsRichComparison
from .exceptions import UnsupportedFunction, FunctionSpecValidationError
from .kwargs_schemas import BaseKwargsSchema, kwargs_schema_to_json_schema


T = typing.TypeVar("T")
R = typing.TypeVar("R")
P = typing.ParamSpec("P")

TALIB_FUNCTIONS = get_talib_functions()


@attrs.define(auto_attribs=True, slots=True, frozen=True, repr=False)
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


_FunctionName = str
"""The name or alias of the TA-LIB function in the functions registry"""
FunctionEvaluator = typing.Callable[[T, FunctionSpec], SupportsRichComparison]
"""
Performs the evaluation of a TA-LIB function on an object using the provided `FunctionSpec`. 
Returns a value that supports rich comparison.

**An evaluator should be thread-safe and stateless. It should not modify the object it is evaluating, or
any external state**.
"""


class _FunctionData(typing.TypedDict):
    evaluator: FunctionEvaluator
    """The function that will be used to evaluate the TA-LIB function"""
    kwargs_schema: typing.Optional[typing.Type[BaseKwargsSchema]]
    """
    The schema for the keyword arguments that the TA-LIB function accepts.

    Setting this to None means the function does not accept any keyword arguments
    """
    description: typing.Optional[str]
    """Short description of the (TA-LIB) function"""
    group: typing.Optional[str]
    """Function group of the (TA-LIB) function"""


FUNCTIONS_REGISTRY: typing.Dict[_FunctionName, _FunctionData] = {}


def make_function_spec(name: str, **kwargs) -> FunctionSpec:
    """
    Helper function to create a TA-LIB function specification

    :param name: The name or alias of the function
    :param kwargs: Keyword arguments for the TA-LIB function.
        These should match the schema of the function's `kwargs_schema`
        in the functions registry
    :return: A new function specification
    """
    if name not in FUNCTIONS_REGISTRY:
        raise UnsupportedFunction(f"Unsupported function: {name}")

    if kwargs:
        kwargs_schema = FUNCTIONS_REGISTRY[name].get("kwargs_schema", None)
        if not kwargs_schema:
            raise FunctionSpecValidationError(
                f"Function {name} does not have a kwargs_schema defined"
                " and cannot accept keyword arguments"
            )

        kwargs = attrs.asdict(kwargs_schema(**kwargs))
    return FunctionSpec(name, kwargs)


def generate_function_schema(function_name: str):
    """
    Generate a JSON schema for the function with the given name

    :param function_name: The name of the function to generate the schema for
    :return: The JSON schema for the function
    :raises UnsupportedFunction: If the function is unregistered/unsupported
    """
    if function_name not in FUNCTIONS_REGISTRY:
        raise UnsupportedFunction("Unsupported function: {function_name}")

    function_data = copy.deepcopy(FUNCTIONS_REGISTRY[function_name])
    function_data.pop("evaluator")
    schema = {
        "type": "function",
        "name": function_name,
        "description": function_data["description"],
        "group": function_data["group"],
        "kwargs": None,
    }

    if function_data["kwargs_schema"]:
        schema["kwargs"] = kwargs_schema_to_json_schema(function_data["kwargs_schema"])
    return schema


def generate_functions_schema(*, grouped: bool = False):
    schemas = {}
    
    for function in FUNCTIONS_REGISTRY:
        function_schema = generate_function_schema(function)
        function_name = function_schema["name"]

        if grouped:
            group = function_schema.get("group", None)
            if group:
                group_functions = schemas.get(group, None) or {}
                group_functions[function] = function_schema
                schemas[group] = group_functions
            else:
                schemas[function_name] = function_schema
        else:
            schemas[function_name] = function_schema
    return schemas


def evaluator(
    func: typing.Optional[FunctionEvaluator] = None,
    /,
    *,
    alias: typing.Optional[str] = None,
    kwargs_schema: typing.Optional[typing.Type[BaseKwargsSchema]] = None,
    description: typing.Optional[str] = None,
    group: typing.Optional[str] = None,
):
    """
    Register a TA-LIB function evaluator

    :param func: The function that will be used to evaluate the TA-LIB function
    :param alias: The alias to use for the TA-LIB function in the functions registry
    :param kwargs_schema: The schema for the keyword arguments that the TA-LIB function accepts.
        Setting this to None means the function does not accept any keyword arguments.
    :param description: Short description of the (TA-LIB) function the evaluator is for.
    :param group: Function group of the (TA-LIB) function the evaluator is for.
    :return: The TA-LIB function evaluator
    """
    if kwargs_schema and not issubclass(kwargs_schema, BaseKwargsSchema):
        raise ValueError("kwargs_schema must be a subclass of BaseKwargsSchema")

    def _decorator(func: FunctionEvaluator):
        func.__doc__ = func.__doc__ or description

        FUNCTIONS_REGISTRY[alias or func.__name__] = {
            "evaluator": func,
            "kwargs_schema": kwargs_schema,
            "description": description,
            "group": group,
        }
        return func

    if func is None:
        return _decorator
    return _decorator(func)


_ArgEvaluator = typing.Callable[[T, FunctionSpec], typing.Union[np.ndarray, R]]
"""
Takes an object and a `FunctionSpec`. 
Evaluates and returns an argument to be passed to a TA-LIB function, using the
given object and/or `FunctionSpec`

**This function should be thread-safe and stateless.
It should not modify the object, or any external state.**
"""
_EvaluatorBuilder = typing.Callable[
    [str, typing.List[_ArgEvaluator]], FunctionEvaluator
]
"""Builds a TA-LIB function evaluator"""

_EvaluatorResultHandler = typing.Callable[[R], SupportsRichComparison]
"""
Handles the result of a TA-LIB function evaluator

Performs additional pre/post-processing on the result of the evaluator
"""

_dtype = typing.TypeVar("_dtype", bound=np.dtype)


def ensure_ndarray(
    *,
    array_dtype: typing.Type[_dtype],
):
    """
    Returns a decorator that ensures the result of the argument evaluator is a numpy array

    :param array_dtype: The preferred numpy data type for the array
    """

    def _decorator(arg_evaluator: _ArgEvaluator):
        """Wraps the argument evaluator to ensure the result is a numpy array"""

        @functools.wraps(arg_evaluator)
        def _wrapper(*args, **kwargs) -> np.ndarray[typing.Type[_dtype]]:
            result = arg_evaluator(*args, **kwargs)

            if not isinstance(result, np.ndarray):
                result = np.array(list(result), dtype=array_dtype)
            return result

        return _wrapper

    return _decorator


def build_evaluator(
    talib_target: str,
    arg_evaluators: typing.List[_ArgEvaluator],
    *,
    result_handler: typing.Optional[_EvaluatorResultHandler] = None,
    use_multithreading: bool = False,
) -> FunctionEvaluator:
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
    :param result_handler: A callable to be used to handle the result of the TA-LIB function evaluator.
        This can be used to perform additional pre/post-processing on the result before it is returned.
    :param use_multithreading: If True, the evaluator will run it argument evaluator concurrently.
        Else, they will be run sequentially. You can change this behaviour directly on the evaluator returned,
        by modifying th `use_multithreading` attribute of the evaluator.
    :return: A new TA-LIB function evaluator
    """
    if talib_target not in TALIB_FUNCTIONS:
        raise ValueError(f"Invalid TA-LIB function: {talib_target}")
    if not arg_evaluators:
        raise ValueError("At least one argument evaluator is required")

    def _evaluator(o: T, /, spec: FunctionSpec) -> SupportsRichComparison:
        if len(arg_evaluators) == 1:
            args = [arg_evaluators[0](o, spec)]

        else:
            if getattr(_evaluator, "use_multithreading", False):
                with ThreadPoolExecutor() as executor:
                    args = executor.map(
                        lambda arg_evaluator: arg_evaluator(o, spec), arg_evaluators
                    )
            else:
                args = [arg_evaluator(o, spec) for arg_evaluator in arg_evaluators]

        result = getattr(talib, talib_target)(*args, **spec.kwargs)
        if result_handler:
            result = result_handler(result)
        return result

    _evaluator.__name__ = talib_target
    _evaluator.use_multithreading = use_multithreading
    return _evaluator


build_multithreaded_evaluator = functools.partial(
    build_evaluator, use_multithreading=True
)


def new_evaluator(
    talib_target: str,
    *,
    arg_evaluators: typing.List[_ArgEvaluator],
    kwargs_schema: typing.Optional[typing.Type[BaseKwargsSchema]] = None,
    alias: typing.Optional[str] = None,
    description: typing.Optional[str] = None,
    group: typing.Optional[str] = None,
    evaluator_builder: _EvaluatorBuilder = build_multithreaded_evaluator,
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
    :param kwargs_schema: The schema for the keyword arguments that the TA-LIB function accepts.
        Setting this to None means the function does not accept any keyword arguments.
    :param alias: The alias to use for the TA-LIB function in the functions registry
    :param description: Short description of the (TA-LIB) function the evaluator is for.
    :param group: Function group of the (TA-LIB) function the evaluator is for.
    :param evaluator_builder: Callable to be used to build the new evaluator.
        Uses the generic builder by default. You can pass your custom builder to this.
    :return: The TA-LIB function evaluator
    """
    return evaluator(
        evaluator_builder(talib_target, arg_evaluators),
        alias=alias,
        kwargs_schema=kwargs_schema,
        description=description,
        group=group,
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
