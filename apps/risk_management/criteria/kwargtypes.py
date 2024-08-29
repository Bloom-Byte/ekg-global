import typing
import attrs


@attrs.define(auto_attribs=True)
class BaseKwargsType:
    """Specifies the schema for the keywords that a TA-LIB function accepts"""

    pass


def KwargsType(
    cls_name: str, attributes: typing.Dict[str, typing.Any], **kwargs
) -> typing.Type[BaseKwargsType]:
    """
    Make a new class that specifies the schema for the keywords that a TA-LIB function accepts

    By default, the new class is a attrs class with `auto_attribs=True` and `slots=True`
    and is a subclass of `BaseKwargsType`

    :param cls_name: The name of the new class
    :param attributes: The attributes of the new class.
        A mapping of attribute names to an `attrs.field` or `attrs.ib` instance
    :param kwargs: Additional keyword arguments to pass to `attrs.make_class`
    :return: subclass of `BaseKwargsType` with defined attributes
    """
    kwargs.setdefault("auto_attribs", True)
    kwargs.setdefault("slots", True)
    kwargs.setdefault("bases", (BaseKwargsType,))
    return attrs.make_class(cls_name, attributes, **kwargs)


def MergeKwargsTypes(
    *kwargstypes: typing.Type[BaseKwargsType],
    cls_name: typing.Optional[str] = None,
    new_attributes: typing.Optional[typing.Dict[str, typing.Any]] = None,
    **kwargs,
):
    """
    Merges the attributes of multiple `KwargsType` classes into a new `KwargsType` class

    The attributes are merged from left to right, in the order in which the classes are passed
    to this function. Meaning that the attributes of the last class will override the attributes
    of the previous classes.

    :param kwargstypes: The KwargsTypes to merge
    :param cls_name: The name of the new KwargsType
    :param new_attributes: Additional attributes to add to the new `KwargsType` class. Overrides existing attributes
    :param kwargs: Additional keyword arguments to pass to `attrs.make_class`
    :return: A new `KwargsType` class that is a merge of the provided `KwargsType`s
    """
    if len(kwargstypes) < 2:
        raise ValueError("At least two KwargsTypes must be provided for merging.")

    cls_name = cls_name or "_".join([kt.__name__ for kt in kwargstypes])
    new_attributes = new_attributes or {}

    merged_attributes = {}
    for kwargstype in kwargstypes:
        for name, field in attrs.fields_dict(kwargstype).items():
            # Manually copy the relevant attributes from the field
            merged_attributes[name] = attrs.field(
                default=field.default
                if field.default != attrs.NOTHING
                else attrs.Factory(lambda: None),
                validator=field.validator,
                repr=field.repr,
                hash=field.hash,
                init=field.init,
                metadata=field.metadata,
                converter=field.converter,
                on_setattr=field.on_setattr,
                kw_only=field.kw_only,
                eq=field.eq,
                order=field.order,
                alias=field.alias,
                type=field.type,
            )

    return KwargsType(
        cls_name=cls_name,
        attributes={**merged_attributes, **new_attributes},
        **kwargs,
    )

