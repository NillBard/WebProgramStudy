from http import HTTPStatus
from typing import Any, Mapping

import pytest

from analyzer.utils.testing import (
    generate_citizen, get_citizens_birthdays, import_data,
)


def make_response(values: Mapping[str, Any] = None):
    return {
        str(month): values.get(str(month), []) if values else []
        for month in range(1, 13)
    }


datasets = [
    {
        'citizens': [
            generate_citizen(citizen_id=1, birth_date='31.12.2019',
                             relatives=[2, 3]),
            generate_citizen(citizen_id=2, birth_date='11.02.2020',
                             relatives=[1]),
            generate_citizen(citizen_id=3, birth_date='17.02.2020',
                             relatives=[1])
        ],
        'expected': make_response({
            '2': [
                {'citizen_id': 1, 'presents': 2}
            ],
            '12': [
                {'citizen_id': 2, 'presents': 1},
                {'citizen_id': 3, 'presents': 1}
            ]
        })
    },

    {
        'citizens': [
            generate_citizen(citizen_id=1, name='Джейн', gender='male',
                             birth_date='17.02.2020', relatives=[1])
        ],
        'expected': make_response({
            '2': [
                {'citizen_id': 1, 'presents': 1}
            ]
        })
    },

    {
        'citizens': [
            generate_citizen(relatives=[])
        ],
        'expected': make_response()
    },

    {
        'citizens': [],
        'expected': make_response()
    },
]


@pytest.mark.parametrize('dataset', datasets)
async def test_get_citizens_birthdays(api_client, dataset):
    await import_data(api_client, [
        generate_citizen(citizen_id=1, relatives=[2]),
        generate_citizen(citizen_id=2, relatives=[1])
    ])

    import_id = await import_data(api_client, dataset['citizens'])
    result = await get_citizens_birthdays(api_client, import_id)

    for month in dataset['expected']:
        assert month in result, f'Month {month} is missing'

        actual = {
            (citizen['citizen_id'], citizen['presents'])
            for citizen in result[month]
        }
        expected = {
            (citizen['citizen_id'], citizen['presents'])
            for citizen in dataset['expected'][month]
        }
        assert actual == expected


async def test_get_nonexistent_import_birthdays(api_client):
    await get_citizens_birthdays(api_client, 999, HTTPStatus.NOT_FOUND)
