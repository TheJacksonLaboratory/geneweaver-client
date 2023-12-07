"""Fixtures and mocks for the enum CLI prompt tests."""
from enum import Enum


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
