from dataclasses import dataclass
from typing import Any, Dict, Type, TypeVar

T = TypeVar('T', bound='BaseDTO')


@dataclass
class BaseDTO:
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        valid_fields = {}
        for field, field_type in cls.__annotations__.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            value = data[field]
            if not isinstance(value, field_type):
                raise TypeError(f"Invalid type for {field}: expected {field_type}, got {type(value)}")
            valid_fields[field] = value

        extra_fields = set(data.keys()) - set(cls.__annotations__.keys())
        if extra_fields:
            raise ValueError(f"Unexpected fields: {', '.join(extra_fields)}")

        return cls(**valid_fields)  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if k in self.__class__.__annotations__}
