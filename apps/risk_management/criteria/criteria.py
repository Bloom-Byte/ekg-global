import asyncio
import typing
from dataclasses import asdict, dataclass, field
import uuid
import enum
from dataclasses_json import dataclass_json

from helpers.models.db import database_sync_to_async
from .functions import Function, validate_function, evaluate_function
from .comparisons import ComparisonOperator, get_comparison_executor
from .exceptions import UnsupportedFunction


T = typing.TypeVar("T")


class CriterionStatus(enum.IntEnum):
    PASSED = 1
    FAILED = 0


@dataclass_json
@dataclass(slots=True, frozen=True, repr=False)
class Criterion:
    id: uuid.UUID = field(default=uuid.uuid4, kw_only=True)
    func1: Function
    func2: Function
    op: ComparisonOperator

    def __repr__(self) -> str:
        return f"<Criterion_{self.id.hex}: {repr(self.func1)} {self.op.value} {repr(self.func2)}>"

    def __str__(self) -> str:
        return f"{self.func1.name} {self.op.value} {self.func2.name}"

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass_json
@dataclass(slots=True)
class Criteria:
    criterion_list: typing.List[Criterion] = field(default=list)

    # Allows iteration over criterion_list directly with the criteria object
    def __iter__(self) -> typing.Iterator[Criterion]:
        return iter(self.criterion_list)

    def __add__(self, other) -> "Criteria":
        if isinstance(other, Criteria):
            return merge_criterias(self, other)

        elif isinstance(other, Criterion):
            return add_criterion(self, other)
        raise TypeError

    def __sub__(self, other) -> "Criteria":
        if isinstance(other, Criterion):
            return remove_criterion(self, other)
        raise TypeError

    __iadd__ = __add__
    __isub__ = __sub__


def add_criterion(criteria: Criteria, criterion: Criterion) -> Criteria:
    criterion_set = set(criteria)
    criterion_set.add(criterion)
    return Criteria(list(criterion_set))


def remove_criterion(criteria: Criteria, criterion: Criterion) -> Criteria:
    criterion_set = set(criteria)
    diff_criterion_set = criterion_set - [criterion]
    return Criteria(list(diff_criterion_set))


def merge_criterias(*criterias: Criteria) -> Criteria:
    criterion_list = []
    for criteria in criterias:
        criterion_list.extend(criteria)

    # Convert to set to remove duplicate,
    # since criterion with the same id have the same hash
    criterion_set = set(criterion_list)
    return Criteria(list(criterion_set))


def make_criterion(
    func1: Function,
    func2: Function,
    op: typing.Union[ComparisonOperator, str],
    *,
    id: typing.Optional[uuid.UUID] = None,
    ignore_unsupported_func: bool = False,
) -> Criterion:
    try:
        func1 = validate_function(func1)
        func2 = validate_function(func2)
    except UnsupportedFunction:
        if not ignore_unsupported_func:
            raise
        pass

    kwds = {
        "func1": func1,
        "func2": func2,
        "op": op,
    }
    if id:
        kwds["id"] = id
    return Criterion(**kwds)


def update_criterion(criterion: Criterion, **kwds) -> Criterion:
    kwds.setdefault("ignore_unsupported_func", True)
    kwds.pop("id", None)

    old_attrs = asdict(criterion)
    kwargs = {**old_attrs, **kwds}
    return make_criterion(**kwargs)


def evaluate_criterion(
    o: T, /, criterion: Criterion, *, ignore_unsupported_func: bool = False
):
    try:
        a = evaluate_function(o, criterion.func1)
        b = evaluate_function(o, criterion.func2)
    except UnsupportedFunction:
        if ignore_unsupported_func:
            return CriterionStatus.FAILED
        raise
    
    comparison_executor = get_comparison_executor(criterion.op)
    return CriterionStatus.PASSED if comparison_executor(a, b) else CriterionStatus.FAILED


def evaluate_criteria(
    o: T, /, criteria: Criteria, *, ignore_unsupported_func: bool = False
) -> typing.Dict[Criterion, CriterionStatus]:
    async def main() -> typing.List[CriterionStatus]:
        async_evaluate_criterion = database_sync_to_async(evaluate_criterion)
        tasks = []
        for criterion in criteria:
            task = asyncio.create_task(
                async_evaluate_criterion(
                    o, criterion, ignore_unsupported_func=ignore_unsupported_func
                )
            )
            tasks.append(task)
        return await asyncio.gather(*tasks)

    statuses = asyncio.run(main)
    result = {}
    for criterion, status in zip(criteria, statuses):
        result[criterion] = status
    return result
