import inspect
import typing
import attrs


@attrs.define(auto_attribs=True)
class BaseKwargsSchema:
    """Specifies the schema for the keywords that a TA-LIB function accepts"""

    pass


def KwargsSchema(
    cls_name: str, attributes: typing.Dict[str, typing.Any], **kwargs
) -> typing.Type[BaseKwargsSchema]:
    """
    Make a new class that specifies the schema for the keywords that a TA-LIB function accepts

    By default, the new class is a attrs class with `auto_attribs=True` and `slots=True`
    and is a subclass of `BaseKwargsSchema`

    :param cls_name: The name of the new class
    :param attributes: The attributes of the new class.
        A mapping of attribute names to an `attrs.field` or `attrs.ib` instance
    :param kwargs: Additional keyword arguments to pass to `attrs.make_class`
    :return: subclass of `BaseKwargsSchema` with defined attributes
    """
    kwargs.setdefault("auto_attribs", True)
    kwargs.setdefault("slots", True)
    kwargs.setdefault("bases", (BaseKwargsSchema,))
    return attrs.make_class(cls_name, attributes, **kwargs)


def MergeKwargsSchemas(
    *kwargs_schemas: typing.Type[BaseKwargsSchema],
    cls_name: typing.Optional[str] = None,
    new_attributes: typing.Optional[typing.Dict[str, typing.Any]] = None,
    **kwargs,
):
    """
    Merges the attributes of multiple `KwargsSchema` classes into a new `KwargsSchema` class

    The attributes are merged from left to right, in the order in which the classes are passed
    to this function. Meaning that the attributes of the last class will override the attributes
    of the previous classes.

    :param kwargs_schemas: The KwargsSchemas to merge
    :param cls_name: The name of the new KwargsSchema
    :param new_attributes: Additional attributes to add to the new `KwargsSchema` class. Overrides existing attributes
    :param kwargs: Additional keyword arguments to pass to `attrs.make_class`
    :return: A new `KwargsSchema` class that is a merge of the provided `KwargsSchema`s
    """
    if len(kwargs_schemas) < 2:
        raise ValueError("At least two KwargsSchemas must be provided for merging.")

    cls_name = cls_name or "_".join([kt.__name__ for kt in kwargs_schemas])
    new_attributes = new_attributes or {}

    merged_attributes = {}
    for kwargs_schema in kwargs_schemas:
        for name, field in attrs.fields_dict(kwargs_schema).items():
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

    return KwargsSchema(
        cls_name=cls_name,
        attributes={**merged_attributes, **new_attributes},
        **kwargs,
    )


class _KwargsSchemaJSONSchema(typing.TypedDict):
    """JSON representation of a KwargsSchema"""

    type: str
    """The type of the KwargsSchema"""
    properties: typing.Dict[str, typing.Dict[str, typing.Any]]
    """The properties of the KwargsSchema"""
    required: typing.List[str]
    """List of the required properties of the KwargsSchema"""


def kwargs_schema_to_json_schema(kwargs_schema: typing.Type[BaseKwargsSchema]):
    """Converts a KwargsSchema class to a JSON schema"""
    json_schema: _KwargsSchemaJSONSchema = {
        "type": "function_kwargs",
        "arguments": {},
        "required_arguments": [],
    }

    for name, field in attrs.fields_dict(kwargs_schema).items():
        field_type = field.type

        if hasattr(field.default, "factory"):
            default_value = field.default.factory()
        elif callable(field.default):
            default_value = field.default()
        elif field.default == attrs.NOTHING:
            default_value = None
        else:
            default_value = field.default

        json_schema["arguments"][name] = {
            "type": "null" if field_type is type(None) else field_type.__name__,
            "default": default_value,
            "required": field.default == attrs.NOTHING,
            "description": field.metadata.get("description", None),
        }

        if field.default == attrs.NOTHING:
            json_schema["required_arguments"].append(name)

    return json_schema
