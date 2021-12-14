from datetime import date, timedelta
from http import HTTPStatus

from analyzer.api.schema import BIRTH_DATE_FORMAT
from analyzer.db.schema import Gender
from analyzer.utils.testing import (
    compare_citizen_groups, compare_citizens, generate_citizen,
    generate_citizens, get_citizens, import_data, patch_citizen,
)


async def test_patch_citizen(api_client):
    side_dataset = [
        generate_citizen(citizen_id=1),
        generate_citizen(citizen_id=2),
        generate_citizen(citizen_id=3)
    ]
    side_dataset_id = await import_data(api_client, side_dataset)

    dataset = [
        generate_citizen(
            citizen_id=1,
            name='Иванов Иван Иванович',
            gender=Gender.male.value,
            birth_date='01.01.2000',
            town='Некий город',
            street='Некая улица',
            building='Некое строение',
            apartment=1,
            relatives=[2]
        ),
        generate_citizen(citizen_id=2, relatives=[1]),
        generate_citizen(citizen_id=3, relatives=[]),
    ]
    import_id = await import_data(api_client, dataset)

    dataset[0]['name'] = 'Иванова Иванна Ивановна'
    await patch_citizen(
        api_client, import_id, dataset[0]['citizen_id'],
        data={'name': dataset[0]['name']}
    )

    dataset[0]['gender'] = Gender.female.value
    dataset[0]['birth_date'] = '02.02.2002'
    dataset[0]['town'] = 'Другой город'
    dataset[0]['street'] = 'Другая улица'
    dataset[0]['building'] = 'Другое строение'
    dataset[0]['apartment'] += 1
    dataset[0]['relatives'] = [dataset[2]['citizen_id']]
    dataset[2]['relatives'].append(dataset[0]['citizen_id'])
    dataset[1]['relatives'].remove(dataset[0]['citizen_id'])

    actual = await patch_citizen(
        api_client, import_id, dataset[0]['citizen_id'], data={
            'gender': dataset[0]['gender'],
            'birth_date': dataset[0]['birth_date'],
            'town': dataset[0]['town'],
            'street': dataset[0]['street'],
            'building': dataset[0]['building'],
            'apartment': dataset[0]['apartment'],
            'relatives': dataset[0]['relatives'],
        }
    )

    assert compare_citizens(dataset[0], actual)

    actual_citizens = await get_citizens(api_client, import_id)
    assert compare_citizen_groups(actual_citizens, dataset)

    actual_citizens = await get_citizens(api_client, side_dataset_id)
    assert compare_citizen_groups(actual_citizens, side_dataset)


async def test_patch_self_relative(api_client):
    dataset = [
        generate_citizen(
            citizen_id=1, name='Джейн', gender='male',
            birth_date='13.09.1945', town='Нью-Йорк', relatives=[]
        ),
    ]
    import_id = await import_data(api_client, dataset)

    dataset[0]['relatives'] = [dataset[0]['citizen_id']]
    actual = await patch_citizen(
        api_client, import_id, dataset[0]['citizen_id'],
        data={k: v for k, v in dataset[0].items() if k != 'citizen_id'}
    )
    assert compare_citizens(dataset[0], actual)


async def test_patch_citizen_birthday_in_future(api_client):
    dataset = generate_citizens(citizens_num=1)
    import_id = await import_data(api_client, dataset)

    birth_date = (date.today() + timedelta(days=1)).strftime(BIRTH_DATE_FORMAT)
    await patch_citizen(api_client, import_id, dataset[0]['citizen_id'],
                        data={'birth_date': birth_date},
                        expected_status=HTTPStatus.BAD_REQUEST)


async def test_patch_citizen_add_nonexistent_relative(api_client):
    dataset = generate_citizens(citizens_num=1)
    import_id = await import_data(api_client, dataset)

    await patch_citizen(api_client, import_id, dataset[0]['citizen_id'],
                        data={'relatives': [999]},
                        expected_status=HTTPStatus.BAD_REQUEST)


async def test_patch_nonexistent(api_client):
    await patch_citizen(api_client, 999, 999, data={'name': 'Иван Иванов'},
                        expected_status=HTTPStatus.NOT_FOUND)

    import_id = await import_data(api_client, [])
    await patch_citizen(api_client, import_id, 999,
                        data={'name': 'Иван Иванов'},
                        expected_status=HTTPStatus.NOT_FOUND)
