"""Fixtures and mocks for the pydantic CLI prompt tests."""

from enum import Enum
from itertools import chain, combinations
from typing import List, Optional, Union

from pydantic import BaseModel


class MockEnum(Enum):
    """Mock enum for testing."""

    A = "A"
    B = "B"
    C = "C"


class MockIntEnum(int, Enum):
    """Mock int enum for testing."""

    A = 1
    B = 2
    C = 3


class MockInternalModel(BaseModel):
    """Mock internal model for testing."""

    enum_field: MockEnum
    enum_int_field: MockIntEnum
    union_enum_field: Union[MockEnum, MockIntEnum]

    bool_field: bool

    int_field: int
    int_field_optional: Optional[int] = None

    float_field: float
    float_field_optional: Optional[float] = None

    str_field: str
    str_field_optional: Optional[str] = None

    list_str_field: List[str]
    list_str_field_optional: Optional[List[str]] = None
    list_union_field: List[Union[str, int]]


class MockModel(MockInternalModel):
    """Mock model for testing."""

    sub_model: MockInternalModel
    sub_model_optional: Optional[MockInternalModel] = None


MOCK_INTERNAL_MODEL_EXAMPLE_INSTANCE = MockInternalModel(
    enum_field=MockEnum.A,
    enum_int_field=MockIntEnum.A,
    union_enum_field=MockEnum.A,
    bool_field=True,
    int_field=1,
    int_field_optional=2,
    float_field=1.0,
    float_field_optional=2.0,
    str_field="A",
    str_field_optional="B",
    list_str_field=["A", "B"],
    list_str_field_optional=["C", "D"],
    list_union_field=["A", 1],
)

MOCK_MODEL_EXAMPLE_INSTANCE = MockModel(
    sub_model=MOCK_INTERNAL_MODEL_EXAMPLE_INSTANCE,
    **MOCK_INTERNAL_MODEL_EXAMPLE_INSTANCE.model_dump(),
)

MOCK_MODEL_FIELDS = [field_name for field_name in MockModel.__fields__.keys()]

MOCK_MODEL_FIELD_COMBINATIONS = [
    set(s)
    for s in chain.from_iterable(
        combinations(MOCK_MODEL_FIELDS, r) for r in range(len(MOCK_MODEL_FIELDS) + 1)
    )
]

MOCK_EXISTING_FIELDS = list(MOCK_MODEL_EXAMPLE_INSTANCE.dict().items())

MOCK_EXISTING_COMBINATIONS = [
    dict(e)
    for e in chain.from_iterable(
        combinations(MOCK_EXISTING_FIELDS, r)
        for r in range(len(MOCK_EXISTING_FIELDS) + 1)
    )
]
