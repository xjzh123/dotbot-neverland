from typing import Mapping, Self

from attrs import define

from ._filter_attrs import filter_attrs


@define
class Base[T: Mapping]:
    @classmethod
    def parse(cls, _data: T, **extra_kwds) -> Self:
        return cls(**filter_attrs(cls, _data), **extra_kwds)
