from datetime import date, timedelta
from http import HTTPStatus

import pytest

from analyzer.api.schema import BIRTH_DATE_FORMAT
from analyzer.utils.pg import MAX_INTEGER
from analyzer.utils.testing import (
    compare_citizen_groups, generate_citizen, generate_citizens, get_citizens,
    import_data,
)


LONGEST_STR = 'ё' * 256
CASES = (
    (
        [
            generate_citizen(relatives=[])
        ],
        HTTPStatus.CREATED
    ),

    (
        [
            generate_citizen(citizen_id=1, relatives=[2, 3]),
            generate_citizen(citizen_id=2, relatives=[1]),
            generate_citizen(citizen_id=3, relatives=[1])
        ],
        HTTPStatus.CREATED
    ),

    (
        [
            generate_citizen(
                citizen_id=1, name='Джейн', gender='male',
                birth_date='13.09.1945', town='Нью-Йорк', relatives=[1]
            ),
        ],
        HTTPStatus.CREATED
    ),

    (
        generate_citizens(
            citizens_num=10000,
            relations_num=1000,
            start_citizen_id=MAX_INTEGER - 10000,
            gender='female',
            name=LONGEST_STR,
            town=LONGEST_STR,
            street=LONGEST_STR,
            building=LONGEST_STR,
            apartment=MAX_INTEGER
        ),
        HTTPStatus.CREATED
    ),

    (
        [],
        HTTPStatus.CREATED
    ),

    (
        [
            generate_citizen(
                birth_date=(date.today()).strftime(BIRTH_DATE_FORMAT)
            )
        ],
        HTTPStatus.CREATED
    ),

    (
        [
            generate_citizen(
                birth_date=(
                    date.today() + timedelta(days=1)
                ).strftime(BIRTH_DATE_FORMAT)
            )
        ],
        HTTPStatus.BAD_REQUEST
    ),

    (
        [
            generate_citizen(citizen_id=1),
            generate_citizen(citizen_id=1),
        ],
        HTTPStatus.BAD_REQUEST
    ),

    (
        [
            generate_citizen(citizen_id=1, relatives=[2]),
            generate_citizen(citizen_id=2, relatives=[]),
        ],
        HTTPStatus.BAD_REQUEST
    ),

    (
        [
            generate_citizen(citizen_id=1, relatives=[3])
        ],
        HTTPStatus.BAD_REQUEST
    ),

    (
        [
            generate_citizen(citizen_id=1, relatives=[2]),
            generate_citizen(citizen_id=2, relatives=[1, 1])
        ],
        HTTPStatus.BAD_REQUEST
    ),
)


@pytest.mark.parametrize('citizens,expected_status', CASES)
async def test_import(api_client, citizens, expected_status):
    import_id = await import_data(api_client, citizens, expected_status)

    if expected_status == HTTPStatus.CREATED:
        imported_citizens = await get_citizens(api_client, import_id)
        assert compare_citizen_groups(citizens, imported_citizens)
