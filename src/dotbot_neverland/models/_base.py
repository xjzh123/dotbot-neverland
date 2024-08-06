from typing import Mapping, Self

from attrs import define

from ._filter_attrs import filter_attrs


@define
class Base[T: Mapping]:
    @classmethod
    def parse(cls, _data: T, **extra_kwds) -> Self:
        try:
            return cls(**filter_attrs(cls, _data), **extra_kwds)
        except Exception as e:
            raise ValueError(
                f"Error during parsing\n{_data=}, {filter_attrs(cls, _data)=}, {extra_kwds=}\nException info: {e}"
            )
