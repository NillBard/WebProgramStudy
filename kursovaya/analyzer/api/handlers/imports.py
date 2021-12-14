from http import HTTPStatus
from typing import Generator

from aiohttp.web_response import Response
from aiohttp_apispec import docs, request_schema, response_schema
from aiomisc import chunk_list

from analyzer.api.schema import ImportResponseSchema, ImportSchema
from analyzer.db.schema import citizens_table, imports_table, relations_table
from analyzer.utils.pg import MAX_QUERY_ARGS

from .base import BaseView


class ImportsView(BaseView):
    URL_PATH = '/imports'
    MAX_CITIZENS_PER_INSERT = MAX_QUERY_ARGS // len(citizens_table.columns)
    MAX_RELATIONS_PER_INSERT = MAX_QUERY_ARGS // len(relations_table.columns)

    @classmethod
    def make_citizens_table_rows(cls, citizens, import_id) -> Generator:
        for citizen in citizens:
            yield {
                'import_id': import_id,
                'citizen_id': citizen['citizen_id'],
                'name': citizen['name'],
                'birth_date': citizen['birth_date'],
                'gender': citizen['gender'],
                'town': citizen['town'],
                'street': citizen['street'],
                'building': citizen['building'],
                'apartment': citizen['apartment'],
            }

    @classmethod
    def make_relations_table_rows(cls, citizens, import_id) -> Generator:
        for citizen in citizens:
            for relative_id in citizen['relatives']:
                yield {
                    'import_id': import_id,
                    'citizen_id': citizen['citizen_id'],
                    'relative_id': relative_id,
                }

    @docs(summary='add import')
    @request_schema(ImportSchema())
    @response_schema(ImportResponseSchema(), code=HTTPStatus.CREATED.value)
    async def post(self):
        async with self.pg.transaction() as conn:
            query = imports_table.insert().returning(imports_table.c.import_id)
            import_id = await conn.fetchval(query)

            citizens = self.request['data']['citizens']
            citizen_rows = self.make_citizens_table_rows(citizens, import_id)
            relation_rows = self.make_relations_table_rows(citizens, import_id)

            chunked_citizen_rows = chunk_list(citizen_rows,
                                              self.MAX_CITIZENS_PER_INSERT)
            chunked_relation_rows = chunk_list(relation_rows,
                                               self.MAX_RELATIONS_PER_INSERT)

            query = citizens_table.insert()
            for chunk in chunked_citizen_rows:
                await conn.execute(query.values(list(chunk)))

            query = relations_table.insert()
            for chunk in chunked_relation_rows:
                await conn.execute(query.values(list(chunk)))

        return Response(body={'data': {'import_id': import_id}},
                        status=HTTPStatus.CREATED)
