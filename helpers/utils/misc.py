from inspect import isclass
from io import BytesIO
from typing import Union, Callable, Any, TypeVar, Dict
import base64
import functools


def is_exception_class(exc):
    return isclass(exc) and issubclass(exc, BaseException)


def str_to_base64(s: str, encoding: str = "utf-8") -> str:
    b = s.encode(encoding=encoding)
    return bytes_to_base64(b)


def bytes_to_base64(b: Union[BytesIO, bytes]) -> str:
    """Convert bytes to a base64 encoded string."""
    return base64.b64encode(b).decode()


def str_is_base64(s: str, encoding: str = "utf-8") -> bool:
    try:
        if not isinstance(s, str):
            return False
        # Encode string to bytes and then decode
        b = s.encode(encoding=encoding)
        decoded = base64.b64decode(b, validate=True)
        # Encode back to base64 to check if it matches original
        return base64.b64encode(decoded).decode() == s.strip()
    except Exception:
        return False


def bytes_is_base64(b: bytes) -> bool:
    try:
        if not isinstance(b, bytes):
            return False
        decoded = base64.b64decode(b, validate=True)
        # Encode back to base64 to check if it matches original
        return base64.b64encode(decoded) == b.strip()
    except Exception:
        return False


Composable = TypeVar("Composable", bound=Callable[..., Any])


def compose(*functions: Composable) -> Composable:
    """
    Compose multiple functions into a single function.

    :param functions: The functions to be composed.
    :return: A composed function.
    """

    def apply(function: Composable, *args, **kwargs):
        return function(*args, **kwargs)

    def composed(*args, **kwargs):
        # initial = apply(functions[0], *args, **kwargs)
        # return functools.reduce(apply, functions, initial)
        ...

    return composed


def get_value_by_traversal_path(
    data: Dict[str, Any], path: str, delimiter: str = "."
) -> Union[Any, None]:
    """
    Get the value from a nested dictionary using a traversal path.

    :param data: The dictionary to traverse.
    :param path: The traversal path to the value.
    :param delimiter: The delimiter used in the traversal path.
    :return: The value at the end of the traversal path.
    """
    path = path.split(delimiter)
    value = data
    for key in path:
        value = value.get(key, None)
        if value is None:
            return None
    return value


def get_attr_by_traversal_path(
    obj: Any, path: str, delimiter: str = "."
) -> Union[Any, None]:
    """
    Get the attribute from an object using a traversal path.

    :param obj: The object to traverse.
    :param path: The traversal path to the attribute.
    :param delimiter: The delimiter used in the traversal path.
    :return: The attribute at the end of the traversal path.
    """
    path = path.split(delimiter)
    value = obj
    for key in path:
        value = getattr(value, key, None)
        if value is None:
            return None
    return value


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merges two (nested) dictionaries."""
    # If either dict is empty, return the other
    if not dict2:
        return dict1
    if not dict1:
        return dict2

    if not (isinstance(dict1, dict) or isinstance(dict2, dict)):
        raise TypeError("Both arguments must be dictionaries")

    merged = dict1.copy()  # Start with a copy of dict1
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            # Recursively merge dictionaries
            merged[key] = merge_dicts(merged[key], value)
        else:
            # If the key is not in dict1 or the value is not a dictionary, override or add the value
            merged[key] = value
    return merged


__all__ = [
    "is_exception_class",
    "str_to_base64",
    "bytes_to_base64",
    "str_is_base64",
    "bytes_is_base64",
    "compose",
    "get_value_by_traversal_path",
    "get_attr_by_traversal_path",
]
