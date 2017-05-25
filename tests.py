"""
    tests
    ~~~~~

    Contains tests for the :mod:`~map_merge` module.
"""
from __future__ import unicode_literals

import pytest
import random

import map_merge


@pytest.fixture(scope='module', params=[
    12,
    24,
    3.1415,
    b"foo",
    u"bar",
    None
])
def primitives(request):
    """
    Fixture that yields back individual primitive values.
    """
    return request.param


@pytest.fixture(scope='module')
def mutable_sequences_of_primitives(primitives):
    """
    Fixture that yields back :class:`~collections.MutableSequence` instances that contain
    a single primitive value.
    """
    return [primitives]


@pytest.fixture(scope='module')
def mutable_sequences_of_multi_length_primitives(primitives):
    """
    Fixture that yields back :class:`~collections.MutableSequence` instances that contain
    a random number of primitive values.
    """
    return [primitives] * random.randint(1, 10)


def test_merge_primitives_overwrite_existing_value(primitives):
    """
    Assert that :func:`~map_merge._merge` overwrites the original value when merging primitives.
    """
    assert map_merge._merge(42, primitives) == primitives


def test_merge_mutable_sequence_appends_when_non_sequence(mutable_sequences_of_primitives):
    """
    Assert that :func:`~map_merge._merge` appends to the original sequence when merging primitives.
    """
    initial = [42]
    expected = initial + mutable_sequences_of_primitives
    assert map_merge._merge(initial, mutable_sequences_of_primitives) == expected


def test_merge_mutable_sequence_appends_when_sequence(mutable_sequences_of_multi_length_primitives):
    """
    Assert that :func:`~map_merge._merge` extends the original sequence when merging two sequences.
    """
    initial = [42]
    expected = initial + mutable_sequences_of_multi_length_primitives
    assert map_merge._merge(initial, mutable_sequences_of_multi_length_primitives) == expected
