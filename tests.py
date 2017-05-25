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


@pytest.fixture(scope='module')
def mutable_set_of_primitives(primitives):
    """
    Fixture that yields back :class:`~collections.MutableSet` instances that contain
    a single primitive value.
    """
    return {primitives}


def test_merge_primitives_overwrite_existing_value(primitives):
    """
    Assert that :func:`~map_merge.merge_objects` overwrites the original value when merging primitives.
    """
    assert map_merge.merge_objects(42, primitives) == primitives


def test_merge_mutable_sequence_appends_when_non_sequence(mutable_sequences_of_primitives):
    """
    Assert that :func:`~map_merge.merge_objects` appends to the original sequence when merging primitives.
    """
    initial = [42]
    expected = initial + mutable_sequences_of_primitives
    assert map_merge.merge_objects(initial, mutable_sequences_of_primitives) == expected


def test_merge_mutable_sequence_appends_when_sequence(mutable_sequences_of_multi_length_primitives):
    """
    Assert that :func:`~map_merge.merge_objects` extends the original sequence when merging two sequences.
    """
    initial = [42]
    expected = initial + mutable_sequences_of_multi_length_primitives
    assert map_merge.merge_objects(initial, mutable_sequences_of_multi_length_primitives) == expected


def test_merge_set_updates_when_given_primitives(mutable_set_of_primitives):
    """
    Assert that :func:`~map_merge.merge_objects` updates the original mutable set when merging primitives.
    """
    initial = {42}
    expected = initial.union(mutable_set_of_primitives)
    assert map_merge.merge_objects(initial, mutable_set_of_primitives) == expected


def test_merge_set_updates_when_given_sequence(mutable_sequences_of_multi_length_primitives):
    """
    Assert that :func:`~map_merge.merge_objects` updates the original mutable set when merging sequences.
    """
    initial = {42}
    expected = initial.union(mutable_sequences_of_multi_length_primitives)
    assert map_merge.merge_objects(initial, mutable_sequences_of_multi_length_primitives) == expected


def test_merge_mappings_overwrites_existing_value(primitives):
    """
    Assert that :func:`~map_merge.merge_objects` overwrites the original value when merging mappings
    that contain matching keys.
    """
    initial = dict(answer=42)
    expected = dict(answer=primitives)
    assert map_merge.merge_objects(initial, expected) == expected


def test_merge_mappings_includes_exclusive_keys():
    """
    Assert that :func:`~map_merge.merge_objects` includes keys that are exclusive to each mapping.
    """
    x = dict(name="foobar")
    y = dict(age=24)
    assert map_merge.merge_objects(x, y) == dict(name="foobar", age=24)


def test_merge_raises_on_custom_type(primitives):
    """
    Assert that :func:`~map_merge.merge_objects` raises a :class:`TypeError` when given two types that it
    cannot merge.
    """
    class CustomType:
        pass

    with pytest.raises(TypeError):
        assert map_merge.merge_objects(CustomType(), primitives)


def test_merge_raises_on_empty_sequence():
    """
    Assert that :func:`~map_merge.merge` raises a :class:`ValueError` when given an empty sequence
    of maps.
    """
    with pytest.raises(ValueError):
        map_merge.merge([])


def test_merge_mutates_first_map_when_toggled():
    """
    Assert that :func:`~map_merge.merge` returns a mutated instance of the first map it is given
    when configured to do so.
    """
    one = dict(x=1, y=2)
    two = dict(x=3, z=4)
    assert map_merge.merge([one, two], mutate=True) is one


def test_merge_returns_new_mapping_when_toggled():
    """
    Assert that :func:`~map_merge.merge` returns a new mapping instance containing the merged
    values when it is configured to do so.
    """
    one = dict(x=1, y=2)
    two = dict(x=3, z=4)
    assert map_merge.merge([one, two], mutate=False) is not one
