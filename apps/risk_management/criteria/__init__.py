import uuid
import typing
import cattrs
from helpers.attrs import type_cast as type_cast_factory, cast_on_set_factory


_T = typing.TypeVar("_T", bound=type)

# Create the default converter (can still be overridden)
converter = cattrs.Converter()
type_cast = type_cast_factory(converter)
cast_on_set = cast_on_set_factory(converter)

def UUID_to_string(uuid_obj: uuid.UUID) -> str:
    """Stringify a UUID object."""
    if callable(uuid_obj):
        uuid_obj = uuid_obj()
    return str(uuid_obj)


def string_to_UUID(uuid_str: str, _) -> uuid.UUID:
    """Converts a stringified UUID to a UUID object."""
    return uuid.UUID(uuid_str)


# Register a unstructure hook to convert UUIDs to strings
converter.register_unstructure_hook(uuid.UUID, UUID_to_string)
# Register a structure hook to convert strings to UUIDs
converter.register_structure_hook(uuid.UUID, string_to_UUID)
