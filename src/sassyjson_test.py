"""
   Copyright 2022 Ecodia GmbH & Co. KG

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from dataclasses import dataclass
from datetime import datetime

import pytest

import sassyjson


@dataclass
class LevelThree:
    other_string: str = ""
    some_integer: int = -1


@dataclass
class LevelTwo:
    level_three: LevelThree = None
    second_string: str = ""


@dataclass
class TopLevel:
    some_date: datetime = None
    some_string: str = ""
    level_two: LevelTwo = None


@dataclass
class NoDefaultConstructor:
    some_other_string: str = ""


@dataclass
class TopLevel:
    some_date: datetime = None
    some_string: str = ""
    level_two: LevelTwo = None


@dataclass
class TopLevelFaulty:
    no_default_def: NoDefaultConstructor
    some_date: datetime = None
    some_string: str = ""
    level_two: LevelTwo = None


TOP_LEVEL_TEST_CLASS = TopLevel(
    level_two=LevelTwo(
        level_three=LevelThree(
            other_string="a string",
            some_integer=123),
        second_string="but also here"),
    some_string="a string",
    some_date=datetime(2022, 6, 17))


def test_Should_convert_class_to_json_When_class_is_given():
    # GIVEN: A complex python class instance.

    # WHEN: The class instance is converted to json string.
    output = sassyjson.to_json(TOP_LEVEL_TEST_CLASS)

    # THEN: It should match the expected string.
    expected = '{"level_two": {"level_three": {"other_string": "a string", "some_integer": 123}, "second_string": "but also here"}, "some_date": "2022-06-17T00:00:00.000000", "some_string": "a string"}'
    assert output == expected


def test_Should_convert_json_string_to_class_When_string_is_given():
    # GIVEN: A json string which resembles a serialized complex python class.
    input = '{"level_two": {"level_three": {"other_string": "a string", "some_integer": 123}, "second_string": "but also here"}, "some_date": "2022-06-17T00:00:00.000000", "some_string": "a string"}'

    # WHEN: The json is unmarshalled into the corresponding python class.
    output = sassyjson.from_json(input, TopLevel)

    # THEN: After marshalling the python instance again to a json string, the new string must match the initial string.
    assert sassyjson.to_json(output) == input


def test_Should_raise_exception_When_some_parameters_are_omitted():
    # GIVEN: A json string which resembles a serialized complex python class, missing some attributes of the class.
    input = '{"level_two": {"level_three": {"some_integer": 123}, "second_string": "but also here"}, "some_date": "2022-06-17T00:00:00.000000", "some_string": "a string"}'

    # WHEN: The json is unmarshalled into the corresponding python class.
    # THEN: An attribute error should be raised.
    with pytest.raises(sassyjson.SassyJsonMissingAttributeError):
        sassyjson.from_json(input, TopLevel)


def test_Should_raise_exception_When_class_without_default_constructor_is_given():
    # GIVEN: A json string which resembles a serialized complex python class.
    input = '{"level_two": {"level_three": {"other_string": "a string", "some_integer": 123}, "second_string": "but also here"}, "some_date": "2022-06-17T00:00:00.000000", "some_string": "a string"}'

    # WHEN: A class is given which does not have a default constructor (itself or one of the nested classes).
    # THEN: A no default constructor error should be raised.
    with pytest.raises(sassyjson.SassyJsonNoDefaultConstructorError):
        sassyjson.from_json(input, TopLevelFaulty)
