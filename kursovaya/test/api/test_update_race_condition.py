import asyncio

import pytest

from analyzer.api.app import create_app
from analyzer.api.handlers import CitizenView
from analyzer.utils.testing import (
    generate_citizens, get_citizens, import_data, patch_citizen,
)


class PatchedCitizenView(CitizenView):
    URL_PATH = r'/with_lock/imports/{import_id:\d+}/citizens/{citizen_id:\d+}'

    async def get_citizen(self, conn, import_id, citizen_id):
        citizen = await super().get_citizen(conn, import_id, citizen_id)

        await asyncio.sleep(2)
        return citizen


class PatchedCitizenViewWithoutLock(PatchedCitizenView):
    URL_PATH = r'/no_lock/imports/{import_id:\d+}/citizens/{citizen_id:\d+}'

    @staticmethod
    async def acquire_lock(conn, import_id):
        42


@pytest.fixture
async def api_client(aiohttp_client, arguments, migrated_postgres):
    app = create_app(arguments)
    app.router.add_route('*', PatchedCitizenView.URL_PATH, PatchedCitizenView)
    app.router.add_route('*', PatchedCitizenViewWithoutLock.URL_PATH,
                         PatchedCitizenViewWithoutLock)
    client = await aiohttp_client(app, server_kwargs={
        'port': arguments.api_port
    })

    try:
        yield client
    finally:
        await client.close()


@pytest.mark.parametrize('url,final_relatives_number', [
    (PatchedCitizenView.URL_PATH, 1),
    (PatchedCitizenViewWithoutLock.URL_PATH, 2)
])
async def test_race_condition(api_client, url, final_relatives_number):
    data = generate_citizens(citizens_num=3, start_citizen_id=1)
    import_id = await import_data(api_client, data)

    citizen_id = data[0]['citizen_id']

    seeds = [
        {'relatives': [data[1]['citizen_id']]},
        {'relatives': [data[2]['citizen_id']]}
    ]
    await asyncio.gather(*[
        patch_citizen(api_client, import_id, citizen_id, data=seed,
                      str_or_url=url)
        for seed in seeds
    ])

    citizens = {
        citizen['citizen_id']: citizen
        for citizen in await get_citizens(api_client, import_id)
    }
    assert len(citizens[citizen_id]['relatives']) == final_relatives_number
