import typing
import cattrs
from django import forms
from django.utils.itercompat import is_iterable

from .models import RiskProfile
from .criteria.criteria import Criteria, make_criterion


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
        return cattrs.unstructure(criteria)
