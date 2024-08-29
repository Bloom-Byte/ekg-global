import typing
import enum

from helpers.typing_utils import SupportsRichComparison
from .exceptions import ComparisonExecutorNotFound


class ComparisonOperator(enum.Enum):
    GREATER_THAN = ">"
    LESS_THAN = "<"
    EQUALS = "="
    GREATER_OR_EQUALS = ">="
    LESS_OR_EQUALS = "<="


ComparisonExecutor = typing.Callable[
    [SupportsRichComparison, SupportsRichComparison], bool
]
COMPARISON_EXECUTORS: typing.Dict[ComparisonOperator, ComparisonExecutor] = {}


def comparison_executor(op: ComparisonOperator):
    op = ComparisonOperator(op)

    def _decorator(executor: ComparisonExecutor):
        global COMPARISON_EXECUTORS

        COMPARISON_EXECUTORS[op] = executor
        return executor

    return _decorator


def get_comparison_executor(
    op: typing.Union[ComparisonOperator, str], *, raise_not_found: bool = True
) -> typing.Optional[ComparisonExecutor]:
    op = ComparisonOperator(op)
    try:
        return COMPARISON_EXECUTORS[op]
    except KeyError:
        if not raise_not_found:
            return None
        raise ComparisonExecutorNotFound(
            f"No executor was found for operator, '{op.value}'."
        )


@comparison_executor(ComparisonOperator.GREATER_THAN)
def greater_than(a: SupportsRichComparison, b: SupportsRichComparison) -> bool:
    return a > b


@comparison_executor(ComparisonOperator.LESS_THAN)
def less_than(a: SupportsRichComparison, b: SupportsRichComparison) -> bool:
    return a < b


@comparison_executor(ComparisonOperator.EQUALS)
def equals(a: SupportsRichComparison, b: SupportsRichComparison) -> bool:
    return a == b


@comparison_executor(ComparisonOperator.GREATER_OR_EQUALS)
def greater_or_equals(a: SupportsRichComparison, b: SupportsRichComparison) -> bool:
    return a >= b


@comparison_executor(ComparisonOperator.LESS_OR_EQUALS)
def less_or_equals(a: SupportsRichComparison, b: SupportsRichComparison) -> bool:
    return a <= b
