import unittest

from query_builder.universe.frontend_backend_converter import FrontendBackendConverter
from query_builder.universe.structure_generator import StructureGenerator
from query_builder.utils.data_types import FieldsFromFrontend


def create_structure_generator():
    table_structure = StructureGenerator(
        r"./../tests/test_db_structure/test_tables",
        r"./../tests/test_db_structure/test_joins",
        r"./../tests/test_db_structure/test_standard_filters",
    )
    return table_structure


class TestFrontendBackendConverter(unittest.TestCase):

    def test_convert_from_frontend_to_backend(self):
        table_structure = create_structure_generator()

        converter = FrontendBackendConverter(table_structure.get_fields(),
                                             table_structure.get_tables(),
                                             table_structure.get_where())

        frontend_fields = {
            'select': ['query_builder.public.dim_calendar.date', 'query_builder.public.dim_calendar.week_no',
                       'query_builder.public.dim_store.bk_address'], 'calculation': [], 'where': {
                'and': [{'filter_one': {'operator': 'predefined'}},
                        {'query_builder.public.dim_item.name': {'operator': '=', 'condition': ['111']}}]}}

        converted_fields = converter.convert_from_frontend_to_backend(frontend_fields)

        print(converted_fields)
