import typing
from django import forms
from django.utils.itercompat import is_iterable

from .models import RiskProfile
from .criteria.criteria import Criteria, make_criterion
from .criteria.functions import make_function_spec


def function_from_data(data: typing.Dict):
    """
    Makes a function object from function data

    :param data: A dictionary containing function data
    """
    if not isinstance(data, dict):
        raise ValueError("data must be a dictionary")

    name = data.get("name", None)
    if not name:
        raise ValueError("Function name is required")

    options = data.get("options", {})
    if not isinstance(options, dict):
        raise ValueError("Function options must be a dictionary")
    
    return make_function_spec(name, **options)


def criterion_data(data: typing.Iterable[typing.Dict]):
    """
    Creates and yields criterion objects from iterable of criterion data

    :param data: An iterable of criterion data
    """
    if not is_iterable(data):
        raise ValueError("data must be an iterable")

    for criterion_data in data:
        if not isinstance(criterion_data, dict):
            raise ValueError("Criterion data must be a dictionary")

        func1 = criterion_data.get("func1", None)
        func2 = criterion_data.get("func2", None)
        op = criterion_data.get("op", None)
        if not all((func1, func2, op)):
            raise ValueError("Criterion data must have func1, func2, and op")

        func1 = function_from_data(func1)
        func2 = function_from_data(func2)
        yield make_criterion(func1, func2, op, ignore_unsupported_func=False)


class RiskProfileCreateForm(forms.ModelForm):
    class Meta:
        model = RiskProfile
        fields = ("name", "description", "stocks", "criteria")

    def clean_criteria(self):
        criteria = self.cleaned_data.get("criteria")
        if not criteria:
            return criteria
        
        criterion_list = list(set(criterion_data(criteria)))
        criteria = Criteria(criterion_list)
        return criteria.to_json()
