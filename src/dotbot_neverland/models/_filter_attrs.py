from typing import Any, Collection, Mapping, cast

from attrs import AttrsInstance, Attribute, fields


def filter_attrs(
    cls: type[AttrsInstance], data: Mapping[str, Any]
) -> Mapping[str, Any]:
    field_names = [field.name for field in cast(Collection[Attribute], fields(cls))]
    return {k: v for k, v in data.items() if (k in field_names)}
