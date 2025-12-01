import pytest

from dbtogo.exceptions import (
    BindViolationError,
    DestructiveMigrationError,
    InvalidMigrationError,
    NoBindError,
    UnboundDeleteError,
)


def test_exceptions():
    with pytest.raises(BindViolationError):
        raise BindViolationError

    with pytest.raises(DestructiveMigrationError):
        raise DestructiveMigrationError

    with pytest.raises(InvalidMigrationError):
        raise InvalidMigrationError

    with pytest.raises(NoBindError):
        raise NoBindError

    with pytest.raises(UnboundDeleteError):
        raise UnboundDeleteError
